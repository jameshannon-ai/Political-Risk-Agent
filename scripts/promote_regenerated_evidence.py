from copy import deepcopy
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent.brief_generator import _evidence_to_score_bridge
from agent.core.scoring import DIMENSIONS, build_traceable_scores


SHOWCASE = ROOT / "showcase"
REVIEW = ROOT / "outputs" / "tavily_regeneration_review_20260610-145056"
OUT = REVIEW / "candidate_promoted_showcase"


CASES = {
    "hormuz": {
        "active_pack": SHOWCASE / "hormuz_evidence_pack.json",
        "active_brief": SHOWCASE / "hormuz_shipping_operator_brief.md",
        "regen_pack": REVIEW / "20260610-145308-strait-of-hormuz-shipping-risk-evidence-pack.json",
        "bridge_heading": "10. Evidence-To-Score Bridge",
    },
    "sanctions": {
        "active_pack": SHOWCASE / "sanctions_evidence_pack.json",
        "active_brief": SHOWCASE / "sanctions_trade_finance_exposure_brief.md",
        "regen_pack": REVIEW / "20260610-145428-sanctions-trade-finance-exposure-evidence-pack.json",
        "bridge_heading": "12. Evidence-To-Score Bridge",
    },
    "uk_ets": {
        "active_pack": SHOWCASE / "uk_ets_evidence_pack.json",
        "active_brief": SHOWCASE / "uk_ets_shipping_operator_brief.md",
        "regen_pack": REVIEW / "20260610-145531-uk-ets-maritime-expansion-carbon-cost-evidence-pack.json",
        "bridge_heading": "7. Evidence-To-Score Bridge",
    },
    "critical_minerals": {
        "active_pack": SHOWCASE / "critical_minerals_evidence_pack.json",
        "active_brief": SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
        "regen_pack": REVIEW / "20260610-145646-critical-minerals-rare-earth-magnet-supply-risk-evidence-pack.json",
        "bridge_heading": "11. Evidence-To-Score Bridge",
    },
    "cyber": {
        "active_pack": SHOWCASE / "cyber_evidence_pack.json",
        "active_brief": SHOWCASE / "cyber_business_interruption_brief.md",
        "regen_pack": REVIEW / "20260610-145755-cyber-business-interruption-geopolitical-risk-evidence-pack.json",
        "bridge_heading": "13. Evidence-To-Score Bridge",
    },
    "fiscal": {
        "active_pack": SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json",
        "active_brief": SHOWCASE / "uk_fiscal_instability_procurement_brief.md",
        "regen_pack": REVIEW / "20260610-145924-uk-fiscal-instability-public-sector-procurement-risk-evidence-pack.json",
        "bridge_heading": "Evidence-To-Score Bridge",
    },
}


REVIEW_MODES = {"snippet_only", "metadata_only", "fallback", "manual_input"}
BAD_TITLE_PATTERNS = ["sitemap", "xml", "search results", "tag archive", "page not found"]
HIGH_AUTHORITY_ROLES = {
    "official_anchor",
    "regulatory_guidance",
    "data_or_indicator_source",
    "insurance_market_evidence",
    "financial_sector_guidance",
    "enforcement_evidence",
    "live_event_reporting",
    "market_pricing",
    "operator_or_industry_guidance",
    "specialist_interpretation",
}
HIGH_AUTHORITY_TYPES = {
    "official_primary",
    "regulatory_guidance",
    "economic_data",
    "market_indicator",
    "industry_guidance",
    "insurance_market_evidence",
    "reputable_news",
    "specialist_analysis",
    "contrary_or_stabilising_evidence",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    all_reports = []
    for case_id, paths in CASES.items():
        result = build_candidate(case_id, paths)
        all_reports.extend(result["report_rows"])
    (OUT / "source_promotion_report.md").write_text(_promotion_markdown(all_reports), encoding="utf-8")
    print(OUT)


def build_candidate(case_id, paths):
    active = _load_json(paths["active_pack"])
    regen = _load_json(paths["regen_pack"])
    source_by_id = {source.get("source_id"): source for source in regen.get("selected_sources", [])}
    report_rows = []
    pending = []
    promoted_sources = []
    promoted_evidence = []
    rejected_sources = []
    downgraded_sources = []

    for evidence in regen.get("evidence", []):
        source = source_by_id.get(evidence.get("source_id"), {})
        decision = classify_source(source, evidence)
        enriched_source = _enrich_source(source, evidence, decision)
        enriched_evidence = _enrich_evidence(evidence, source, decision)
        pending.append((enriched_source, enriched_evidence, decision))

    accepted_requirements = {
        evidence.get("requirement_name") or source.get("requirement_name")
        for source, evidence, decision in pending
        if decision["promotion_decision"] in {"promote", "promote_with_review", "downgrade"}
    }

    for enriched_source, enriched_evidence, decision in pending:
        requirement = enriched_evidence.get("requirement_name") or enriched_source.get("requirement_name")
        if decision["promotion_decision"] == "reject" and requirement and requirement not in accepted_requirements:
            decision = _decision(
                "needs_targeted_rerun",
                decision["source_quality_reason"] + " No acceptable promoted source remains for this requirement.",
                "requires_targeted_refresh",
                True,
            )
            enriched_source.update(
                {
                    "source_quality_status": decision["source_quality_status"],
                    "source_quality_reason": decision["source_quality_reason"],
                    "review_required": True,
                    "confidence_impact": decision["confidence_impact"],
                }
            )
            enriched_evidence.update(
                {
                    "source_quality_status": decision["source_quality_status"],
                    "source_quality_reason": decision["source_quality_reason"],
                    "promotion_decision": decision["promotion_decision"],
                    "review_required": True,
                    "requires_human_review": True,
                    "confidence_effect": decision["confidence_impact"],
                }
            )
        row = _report_row(case_id, enriched_source, enriched_evidence, decision)
        report_rows.append(row)
        if decision["promotion_decision"] in {"reject", "needs_targeted_rerun"}:
            rejected_sources.append(enriched_source)
            continue
        if decision["promotion_decision"] == "downgrade":
            downgraded_sources.append(enriched_source)
        promoted_sources.append(enriched_source)
        promoted_evidence.append(enriched_evidence)

    candidate = deepcopy(active)
    candidate["selected_sources"] = promoted_sources
    candidate["evidence"] = promoted_evidence
    candidate["selected_count"] = len(promoted_sources)
    candidate["rejected_regenerated_sources"] = rejected_sources
    candidate["downgraded_regenerated_sources"] = downgraded_sources
    candidate["source_promotion_report"] = report_rows
    candidate["source_quality_summary"] = _source_quality_summary(promoted_evidence, rejected_sources, downgraded_sources)
    candidate["candidate_upgrade_note"] = (
        "Candidate pack created offline from staged Tavily regeneration. Active showcase artefacts were not replaced automatically."
    )
    candidate["traceable_scores"] = _rebuild_scores(candidate, active)
    candidate["evidence_to_score_bridge"] = _bridge_from_scores(candidate["traceable_scores"])

    for item in candidate["traceable_scores"].values():
        rejected_ids = {source.get("source_id") for source in rejected_sources}
        item["supporting_evidence"] = [source_id for source_id in item.get("supporting_evidence", []) if source_id not in rejected_ids]
        item["evidence_supporting_score"] = item["supporting_evidence"]

    _write_json(OUT / f"{case_id}_candidate_evidence_pack.json", candidate)
    _write_json(OUT / f"{case_id}_source_promotion_report.json", report_rows)
    candidate_brief = _candidate_brief(paths["active_brief"], paths["bridge_heading"], candidate)
    (OUT / f"{case_id}_candidate_brief.md").write_text(candidate_brief, encoding="utf-8")
    return {"candidate": candidate, "report_rows": report_rows}


def classify_source(source, evidence):
    title = (source.get("title") or evidence.get("source_title") or evidence.get("title") or "").lower()
    url = (source.get("url") or evidence.get("source_url") or evidence.get("url") or "").lower()
    mode = evidence.get("evidence_source_mode") or source.get("evidence_source_mode") or "not_recorded"
    claim = evidence.get("extracted_claim") or evidence.get("claim_supported") or evidence.get("source_claim") or ""
    requirement = evidence.get("requirement_name") or source.get("requirement_name") or ""
    source_role = source.get("source_role") or evidence.get("source_role") or ""
    source_type = source.get("source_type") or evidence.get("source_type") or ""
    direct = _directly_supports_requirement(claim, requirement, title)

    if _is_bad_source(title, url):
        return _decision("reject", "Rejected because the source is a sitemap, generic index or non-content page.", "not_supporting", False)
    if not claim.strip() or not direct:
        return _decision("reject", "Rejected because the extracted claim is missing or does not directly support the mapped requirement.", "not_supporting", False)
    if mode == "metadata_only":
        return _decision("downgrade", "Metadata-only evidence is not strong enough to support high-confidence scoring.", "caps_confidence", False)
    if mode in REVIEW_MODES:
        return _decision("promote_with_review", "Relevant source, but snippet/manual/fallback evidence requires human verification and should cap confidence.", "supports_score_with_cap", True)
    if source_role in HIGH_AUTHORITY_ROLES or source_type in HIGH_AUTHORITY_TYPES or _authority_url(url):
        return _decision("promote", "Directly relevant high-authority source with source-grounded evidence and improved provenance.", "supports_score", False)
    return _decision("downgrade", "Broadly relevant evidence, but source authority or specificity is not strong enough for high-confidence scoring.", "caps_confidence", True)


def _decision(status, reason, confidence_impact, review_required):
    return {
        "source_quality_status": status,
        "promotion_decision": status,
        "source_quality_reason": reason,
        "confidence_impact": confidence_impact,
        "supporting_evidence_candidate": status in {"promote", "promote_with_review"},
        "review_required": review_required,
    }


def _is_bad_source(title, url):
    if any(pattern in title for pattern in BAD_TITLE_PATTERNS):
        return True
    if any(pattern in url for pattern in ["sitemap", ".xml", "/tag/", "/search?"]):
        return True
    return False


def _directly_supports_requirement(claim, requirement, title):
    text = f"{claim} {title}".lower()
    if len(claim.strip()) < 35:
        return False
    tokens = [token for token in re.split(r"[^a-z0-9]+", requirement.lower()) if len(token) > 4]
    if not tokens:
        return True
    return bool(set(tokens[:6]) & set(re.split(r"[^a-z0-9]+", text)))


def _authority_url(url):
    return any(
        marker in url
        for marker in [
            "gov.uk",
            "ofsi",
            "ncsc.gov.uk",
            "ico.org.uk",
            "bankofengland.co.uk",
            "ons.gov.uk",
            "obr.uk",
            "nao.org.uk",
            "ukmto.org",
            "imo.org",
            "reuters.com",
            "apnews.com",
            "eia.gov",
            "usgs.gov",
            "iea.org",
            "oecd.org",
            "iccwbo.org",
            "wolfsberg-principles.com",
        ]
    )


def _enrich_source(source, evidence, decision):
    enriched = deepcopy(source)
    enriched.update(
        {
            "source_quality_status": decision["source_quality_status"],
            "source_quality_reason": decision["source_quality_reason"],
            "review_required": decision["review_required"] or evidence.get("requires_human_review", False),
            "evidence_source_mode": evidence.get("evidence_source_mode") or source.get("evidence_source_mode") or "not_recorded",
            "source_excerpt": _source_excerpt(evidence, source),
            "extracted_claim": evidence.get("extracted_claim") or evidence.get("claim_supported") or evidence.get("snippet", ""),
            "confidence_impact": decision["confidence_impact"],
        }
    )
    return enriched


def _enrich_evidence(evidence, source, decision):
    enriched = deepcopy(evidence)
    mode = enriched.get("evidence_source_mode") or source.get("evidence_source_mode") or "not_recorded"
    enriched.update(
        {
            "source_quality_status": decision["source_quality_status"],
            "source_quality_reason": decision["source_quality_reason"],
            "promotion_decision": decision["promotion_decision"],
            "review_required": decision["review_required"] or mode in REVIEW_MODES or evidence.get("requires_human_review", False),
            "requires_human_review": decision["review_required"] or mode in REVIEW_MODES or evidence.get("requires_human_review", False),
            "evidence_source_mode": mode,
            "source_excerpt": _source_excerpt(evidence, source),
            "extracted_claim": evidence.get("extracted_claim") or evidence.get("claim_supported") or evidence.get("snippet", ""),
            "confidence_effect": evidence.get("confidence_effect") or decision["confidence_impact"],
        }
    )
    return enriched


def _source_excerpt(evidence, source):
    return (
        evidence.get("quoted_excerpt_used")
        or evidence.get("source_excerpt")
        or evidence.get("snippet")
        or source.get("source_excerpt")
        or source.get("snippet")
        or ""
    )


def _report_row(case_id, source, evidence, decision):
    return {
        "case_id": case_id,
        "source_id": source.get("source_id") or evidence.get("source_id", ""),
        "title": source.get("title") or evidence.get("source_title") or evidence.get("title", ""),
        "publisher": source.get("publisher") or evidence.get("publisher", ""),
        "url": source.get("url") or evidence.get("source_url") or evidence.get("url", ""),
        "source_requirement": source.get("requirement_name") or evidence.get("requirement_name", ""),
        "evidence_source_mode": evidence.get("evidence_source_mode", "not_recorded"),
        "source_quality_status": decision["source_quality_status"],
        "promotion_decision": decision["promotion_decision"],
        "reason": decision["source_quality_reason"],
        "confidence_impact": decision["confidence_impact"],
        "should_appear_in_supporting_evidence": decision["supporting_evidence_candidate"],
    }


def _source_quality_summary(evidence, rejected, downgraded):
    modes = [item.get("evidence_source_mode") or "not_recorded" for item in evidence]
    company_gaps = sum(1 for item in evidence if item.get("source_role") == "company_required_data" or "company" in item.get("requirement_name", ""))
    return {
        "full_text": modes.count("full_text"),
        "snippet_only": modes.count("snippet_only"),
        "metadata_only": modes.count("metadata_only"),
        "fallback_or_manual": sum(1 for mode in modes if mode in {"fallback", "manual_input"}),
        "not_recorded": modes.count("not_recorded"),
        "rejected_or_weak": len(rejected) + len(downgraded),
        "review_required": sum(1 for item in evidence if item.get("requires_human_review") or item.get("review_required")),
        "company_data_gaps": company_gaps,
    }


def _rebuild_scores(candidate, active):
    risk_scores = {}
    for dimension, item in (active.get("traceable_scores") or {}).items():
        risk_scores[dimension] = {
            "score": item.get("score"),
            "rationale": item.get("reason_for_score", ""),
            "score_type": item.get("score_type", "analyst_assumption"),
        }
    return build_traceable_scores(risk_scores, candidate)


def _bridge_from_scores(traceable_scores):
    bridge = {}
    for dimension in DIMENSIONS:
        item = traceable_scores.get(dimension, {})
        bridge[dimension] = {
            "dimension": dimension,
            "score": item.get("score", ""),
            "score_type": item.get("score_type", ""),
            "evidence_basis": item.get("reason_for_score", ""),
            "supporting_evidence": item.get("supporting_evidence", []),
            "weakening_evidence": item.get("weakening_evidence", []),
            "missing_evidence": item.get("missing_evidence", []),
            "confidence_cap_applied": item.get("confidence_cap_applied", False),
            "confidence_cap_reason": item.get("confidence_cap_reason", ""),
            "review_required": item.get("review_required", False),
        }
    return bridge


def _candidate_brief(active_brief_path, bridge_heading, candidate):
    text = active_brief_path.read_text(encoding="utf-8")
    scores = {
        dimension: {
            "score": item.get("score"),
            "rationale": item.get("reason_for_score", ""),
            "score_type": item.get("score_type", "analyst_assumption"),
        }
        for dimension, item in candidate.get("traceable_scores", {}).items()
    }
    bridge = _evidence_to_score_bridge(candidate, scores)
    text = _replace_section(text, bridge_heading, bridge)
    if "Source Quality Notes" not in text:
        text = _insert_before_late_section(text, _source_quality_notes(candidate))
    return text


def _replace_section(markdown, heading, body):
    pattern = re.compile(
        r"(^##\s+" + re.escape(heading) + r"\s*\n)(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        return markdown + f"\n\n## {heading}\n\n{body}\n"
    return markdown[: match.start()] + match.group(1) + "\n" + body.strip() + "\n\n" + markdown[match.end() :]


def _insert_before_late_section(markdown, section):
    for heading in ["Source Audit Summary", "Methodology and Review Controls", "Human Review And Company Data Required"]:
        pattern = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$", re.MULTILINE)
        match = pattern.search(markdown)
        if match:
            return markdown[: match.start()] + section.strip() + "\n\n" + markdown[match.start() :]
    return markdown.rstrip() + "\n\n" + section.strip() + "\n"


def _source_quality_notes(candidate):
    summary = candidate.get("source_quality_summary", {})
    rows = [
        ("Full-text promoted evidence", summary.get("full_text", 0), "Use only where the extracted claim directly supports the requirement."),
        ("Snippet-only evidence", summary.get("snippet_only", 0), "Promoted only with review flags and confidence caps."),
        ("Rejected or weak regenerated sources", summary.get("rejected_or_weak", 0), "Excluded from supporting evidence and listed in the promotion report."),
        ("Review-required evidence", summary.get("review_required", 0), "Requires source verification before operational use."),
        ("Company-data gaps", summary.get("company_data_gaps", 0), "Private company or transaction data is required before operational use."),
    ]
    lines = [
        "## Source Quality Notes",
        "",
        "| Evidence area | Current source quality | Action before operational use |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| {_cell(area)} | {_cell(value)} | {_cell(action)} |" for area, value, action in rows)
    return "\n".join(lines)


def _promotion_markdown(rows):
    lines = [
        "# Source Promotion Report",
        "",
        "| Case | Source ID | Title | Publisher | Requirement | Mode | Decision | Confidence impact | Supporting evidence | Reason | URL |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {case_id} | {source_id} | {title} | {publisher} | {requirement} | {mode} | {decision} | {impact} | {supporting} | {reason} | {url} |".format(
                case_id=_cell(row["case_id"]),
                source_id=_cell(row["source_id"]),
                title=_cell(row["title"]),
                publisher=_cell(row["publisher"]),
                requirement=_cell(row["source_requirement"]),
                mode=_cell(row["evidence_source_mode"]),
                decision=_cell(row["promotion_decision"]),
                impact=_cell(row["confidence_impact"]),
                supporting="yes" if row["should_appear_in_supporting_evidence"] else "no",
                reason=_cell(row["reason"]),
                url=_cell(row["url"]),
            )
        )
    return "\n".join(lines) + "\n"


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
