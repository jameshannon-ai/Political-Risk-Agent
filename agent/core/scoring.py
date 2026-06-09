SCORE_LABELS = {
    1: "Low",
    2: "Guarded",
    3: "Moderate",
    4: "High",
    5: "Severe",
}


DIMENSIONS = ["likelihood", "impact", "immediacy", "exposure", "confidence", "decision_urgency"]


def build_traceable_scores(risk_scores, evidence_pack):
    traceable = {}
    evidence = evidence_pack.get("evidence", [])
    missing_requirements = evidence_pack.get("requirements_missing", [])
    fallback = evidence_pack.get("fallback_demo_data_used", False)

    for dimension in DIMENSIONS:
        base = risk_scores.get(dimension) or _derived_dimension_score(dimension, risk_scores)
        score = base.get("score", "")
        supporting = _supporting_evidence(dimension, evidence)
        contrary = _contrary_evidence(evidence)
        quality_limits = _evidence_quality_limits(evidence)
        missing = _missing_evidence(dimension, missing_requirements, evidence_pack)
        cap_reason = _cap_reason(dimension, evidence_pack, fallback, missing)
        traceable[dimension] = {
            "score": score,
            "score_label": SCORE_LABELS.get(score, "Unscored") if isinstance(score, int) else "Unscored",
            "score_type": "Evidence-backed decision-support score",
            "supporting_evidence": supporting,
            "contrary_evidence": contrary,
            "evidence_quality_limits": quality_limits,
            "missing_evidence": missing,
            "reason_for_score": base.get("rationale", "Structured analyst score based on available source evidence."),
            "reason_score_is_capped": cap_reason,
            "confidence": _dimension_confidence(dimension, evidence_pack, supporting, missing, fallback),
            "review_required": bool(missing or quality_limits or fallback or not supporting),
            # Backwards-compatible aliases for older renderers/tests.
            "evidence_supporting_score": supporting,
            "evidence_weakening_score": contrary,
        }
    return traceable


def _derived_dimension_score(dimension, risk_scores):
    if dimension == "exposure":
        impact = risk_scores.get("impact", {})
        return {"score": impact.get("score", ""), "rationale": "Exposure is proxied from impact where no separate exposure model is available."}
    if dimension == "decision_urgency":
        immediacy = risk_scores.get("immediacy", {})
        return {"score": immediacy.get("score", ""), "rationale": "Decision urgency is proxied from immediacy where no separate urgency model is available."}
    return {}


def _supporting_evidence(dimension, evidence):
    rows = []
    for item in evidence:
        risk_dimension = item.get("risk_dimension", "")
        if risk_dimension == dimension or _dimension_keyword_match(dimension, item):
            rows.append(_evidence_ref(item))
    if not rows:
        rows = [_evidence_ref(item) for item in evidence[:3]]
    return rows


def _contrary_evidence(evidence):
    rows = []
    for item in evidence:
        if item.get("contrary_signal") or item.get("source_type") in {"contrary_or_stabilising_evidence", "contrary_scope_limit"}:
            rows.append(_evidence_ref(item))
    return rows[:5]


def _evidence_quality_limits(evidence):
    rows = []
    for item in evidence:
        mode = item.get("evidence_source_mode", "")
        if (
            mode in {"snippet_only", "fallback", "manual_input"}
            or item.get("inference_strength") == "weak"
            or item.get("requires_human_review")
            or item.get("extraction_confidence") == "low"
        ):
            rows.append(_evidence_ref(item))
    return rows[:8]


def _missing_evidence(dimension, missing_requirements, evidence_pack):
    missing = list(missing_requirements or [])
    if dimension == "confidence":
        missing.extend(evidence_pack.get("source_categories_missing", []))
        domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
        if domain == "uk_fiscal_procurement_risk":
            missing.extend(
                [
                    "contractor order book by public-sector customer",
                    "departmental bid pipeline and award timing",
                    "payment terms, retentions and aged receivables",
                    "margin and working-capital sensitivity",
                ]
            )
    return sorted(set(item for item in missing if item))


def _cap_reason(dimension, evidence_pack, fallback, missing):
    if fallback:
        return "Capped because fallback/demo evidence is not live-source-backed."
    if dimension == "confidence":
        return evidence_pack.get("confidence_cap_reason", "Capped where source coverage, freshness or company data is incomplete.")
    if missing:
        return "Capped because one or more source requirements remain missing or weak."
    if any(item.get("evidence_source_mode") == "snippet_only" for item in evidence_pack.get("evidence", [])):
        return "Capped because at least one selected source used snippet-only evidence."
    return "No explicit cap beyond normal analyst review discipline."


def _dimension_confidence(dimension, evidence_pack, supporting, missing, fallback):
    if fallback or missing:
        return "low" if dimension == "confidence" else "medium"
    if not supporting:
        return "low"
    if any(item.get("evidence_source_mode") == "snippet_only" for item in evidence_pack.get("evidence", [])):
        return "medium"
    return "high"


def _dimension_keyword_match(dimension, item):
    text = " ".join(
        [
            item.get("claim_supported", ""),
            item.get("source_claim", ""),
            item.get("analyst_inference", ""),
            item.get("decision_use", ""),
            " ".join(item.get("quantified_facts", [])),
        ]
    ).lower()
    keywords = {
        "likelihood": ["confirm", "policy", "official", "reported", "trigger"],
        "impact": ["cost", "revenue", "premium", "delay", "exposure", "interruption"],
        "immediacy": ["current", "near-term", "deadline", "days", "months", "active"],
        "exposure": ["route", "supplier", "transaction", "operator", "customer", "voyage", "public-sector", "order book", "working capital", "payment"],
        "confidence": ["caveat", "snippet", "official", "source", "requires"],
        "decision_urgency": ["deadline", "hold", "escalate", "notify", "prepare", "activate"],
    }
    return any(keyword in text for keyword in keywords.get(dimension, []))


def _evidence_ref(item):
    return {
        "source_id": item.get("source_id", ""),
        "source_title": item.get("source_title") or item.get("title", ""),
        "evidence_type": item.get("evidence_type", ""),
        "inference_strength": item.get("inference_strength", ""),
        "claim": item.get("source_claim") or item.get("claim_supported", ""),
    }
