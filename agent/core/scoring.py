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
    evidence_by_id = {item.get("source_id"): item for item in evidence if item.get("source_id")}
    missing_requirements = evidence_pack.get("requirements_missing", [])
    fallback = evidence_pack.get("fallback_demo_data_used", False)

    for dimension in DIMENSIONS:
        base = risk_scores.get(dimension) or _derived_dimension_score(dimension, risk_scores)
        score = base.get("score", "")
        supporting = _supporting_evidence(dimension, evidence)
        contrary = _contrary_evidence(evidence)
        quality_limits = _evidence_quality_limits(evidence)
        missing = _missing_evidence(dimension, missing_requirements, evidence_pack)
        score, discipline_reason = _apply_confidence_discipline(dimension, score, supporting, evidence_by_id, missing, fallback)
        cap_reason = _cap_reason(dimension, evidence_pack, fallback, missing, discipline_reason)
        cap_applied = bool(cap_reason)
        score_type = _score_type(base, supporting, fallback)
        traceable[dimension] = {
            "dimension": dimension,
            "score": score,
            "score_label": SCORE_LABELS.get(score, "Unscored") if isinstance(score, int) else "Unscored",
            "score_type": score_type,
            "supporting_evidence": supporting,
            "weakening_evidence": contrary,
            "contrary_evidence": contrary,
            "evidence_quality_limits": quality_limits,
            "missing_evidence": missing,
            "reason_for_score": base.get("rationale", "Structured analyst score based on available source evidence."),
            "reason_score_is_capped": cap_reason,
            "confidence_cap_applied": cap_applied,
            "confidence_cap_reason": cap_reason,
            "confidence": _dimension_confidence(dimension, evidence_pack, supporting, missing, fallback),
            "review_required": bool(missing or quality_limits or fallback or not supporting or cap_applied),
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
        if (
            item.get("contrary_signal")
            or item.get("source_type") in {"contrary_or_stabilising_evidence", "contrary_scope_limit"}
            or item.get("source_role") == "contrary_scope_limit"
        ):
            rows.append(item.get("source_id", ""))
    return rows[:5]


def _evidence_quality_limits(evidence):
    rows = []
    for item in evidence:
        mode = item.get("evidence_source_mode", "")
        if (
            mode in {"snippet_only", "fallback", "manual_input"}
            or mode == "metadata_only"
            or item.get("inference_strength") == "weak"
            or item.get("requires_human_review")
            or item.get("extraction_confidence") == "low"
        ):
            rows.append(item.get("source_id", ""))
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


def _cap_reason(dimension, evidence_pack, fallback, missing, discipline_reason=""):
    reasons = []
    if fallback:
        reasons.append("fallback/demo evidence is not live-source-backed")
    if discipline_reason:
        reasons.append(discipline_reason)
    if dimension == "confidence":
        stored = evidence_pack.get("confidence_cap_reason", "")
        if stored:
            reasons.append(stored)
    if missing:
        reasons.append("one or more source requirements or company-data inputs remain missing or weak")
    if any(item.get("evidence_source_mode") == "snippet_only" for item in evidence_pack.get("evidence", [])):
        reasons.append("at least one selected source used snippet-only evidence")
    if not reasons:
        return ""
    cleaned = []
    for reason in reasons:
        reason = str(reason).strip().rstrip(".")
        if reason and reason not in cleaned:
            cleaned.append(reason)
    return "Capped because " + "; ".join(cleaned) + "."


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
    return item.get("source_id", "")


def _score_type(base, supporting, fallback):
    if fallback:
        return "illustrative_fallback"
    explicit = base.get("score_type")
    if explicit in {"evidence_backed", "analyst_assumption", "illustrative_fallback"}:
        return explicit
    if supporting and base.get("derived_from_evidence"):
        return "evidence_backed"
    if supporting:
        return "analyst_assumption"
    return "illustrative_fallback"


def _apply_confidence_discipline(dimension, score, supporting_ids, evidence_by_id, missing, fallback):
    if dimension != "confidence" or not isinstance(score, int):
        return score, ""
    if fallback:
        return min(score, 2), "fallback/demo evidence caps confidence at 2"
    supporting = [evidence_by_id[source_id] for source_id in supporting_ids if source_id in evidence_by_id]
    if not supporting:
        return min(score, 2), "no supporting evidence rows were linked to the confidence score"
    modes = [item.get("evidence_source_mode", "") for item in supporting]
    if modes and sum(1 for mode in modes if mode == "metadata_only") >= len(modes) / 2:
        return min(score, 2), "metadata-only evidence cannot support confidence above 2"
    if modes and sum(1 for mode in modes if mode == "snippet_only") > len(modes) / 2:
        return min(score, 3), "most supporting evidence is snippet-only"
    if missing:
        return min(score, 3), "company-required or missing evidence caps confidence at 3"
    return score, ""
