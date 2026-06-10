import json
import re
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_markdown(path):
    return Path(path).read_text(encoding="utf-8")


def extract_markdown_section(markdown, heading):
    pattern = re.compile(
        r"^##\s+" + re.escape(heading) + r"\s*$\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def extract_markdown_table(section):
    lines = [line.rstrip() for line in section.splitlines() if line.strip()]
    tables = []
    current = []

    for line in lines:
        if line.startswith("|"):
            current.append(line)
        elif current:
            tables.append(_parse_table(current))
            current = []

    if current:
        tables.append(_parse_table(current))

    return tables


def get_nested_value(data, possible_keys, default=None):
    for key_path in possible_keys:
        current = data
        found = True
        for key in key_path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                found = False
                break
        if found:
            return current
    return default


def parse_first_number(text, default=0.0):
    match = re.search(r"[-+]?\d[\d,]*(?:\.\d+)?", str(text))
    if not match:
        return default
    return float(match.group(0).replace(",", ""))


def build_selected_source_rows(pack):
    rows = []
    for source in pack.get("selected_sources", []):
        source_type = _display_source_type(source)
        rows.append(
            {
                "Source ID": source.get("source_id", ""),
                "Title": source.get("title", ""),
                "Publisher": source.get("publisher") or _publisher_from_url(source.get("url", "")),
                "Source role": _display_source_role(source, source_type),
                "Source type": source_type,
                "Requirement": source.get("requirement_name") or source.get("source_requirement", ""),
                "Weight": source.get("evidence_weight", ""),
                "Decision use": source.get("decision_use", ""),
                "Source quality": source.get("source_quality_status", "not_assessed"),
                "URL": source.get("url", ""),
            }
        )
    return rows


def build_decision_panel_rows(pack):
    traceable = pack.get("traceable_scores") or {}
    confidence = traceable.get("confidence", {})
    supporting = _source_ids(confidence.get("supporting_evidence", []))
    missing = confidence.get("missing_evidence") or pack.get("requirements_missing") or []
    quality = build_evidence_quality_summary(pack)
    return [
        {"Item": "Current recommendation", "Value": _decision_recommendation(pack)},
        {"Item": "Confidence score", "Value": _score_display(confidence)},
        {"Item": "Evidence quality summary", "Value": _quality_sentence(quality)},
        {"Item": "Main supporting evidence", "Value": ", ".join(supporting[:3]) or "Not linked"},
        {"Item": "Main missing evidence", "Value": ", ".join(missing[:3]) or "No explicit missing-evidence field"},
        {"Item": "Human review required", "Value": "Yes" if quality["review_required"] or confidence.get("review_required") else "No"},
        {"Item": "Company data required", "Value": "Yes" if quality["company_data_gaps"] or missing else "Review case controls"},
    ]


def build_evidence_quality_summary(pack):
    evidence = pack.get("evidence", [])
    selected = pack.get("selected_sources", [])
    rejected = pack.get("rejected_regenerated_sources", []) or [
        source for source in pack.get("rejected_sources", []) if source.get("source_quality_status") in {"reject", "downgrade", "needs_targeted_rerun"}
    ]
    modes = [
        item.get("evidence_source_mode")
        or _source_for_item(selected, item).get("evidence_source_mode")
        or "not_recorded"
        for item in evidence
    ]
    weak_statuses = {"downgrade", "reject", "needs_targeted_rerun", "not_assessed"}
    confidence_cap = _first_confidence_cap(pack)
    return {
        "full_text": modes.count("full_text"),
        "snippet_only": modes.count("snippet_only"),
        "metadata_only": modes.count("metadata_only"),
        "fallback_manual": sum(1 for mode in modes if mode in {"fallback", "manual_input"}),
        "not_recorded": modes.count("not_recorded"),
        "rejected_or_weak": len(rejected) + sum(1 for item in evidence if item.get("source_quality_status") in weak_statuses),
        "review_required": sum(
            1 for item, mode in zip(evidence, modes)
            if item.get("requires_human_review") or item.get("review_required") or mode in {"snippet_only", "metadata_only", "fallback", "manual_input"}
        ),
        "company_data_gaps": _company_data_gap_count(pack),
        "confidence_cap_reason": confidence_cap,
    }


def build_evidence_quality_rows(pack):
    summary = build_evidence_quality_summary(pack)
    labels = {
        "full_text": "Full-text sources",
        "snippet_only": "Snippet-only sources",
        "metadata_only": "Metadata-only sources",
        "fallback_manual": "Fallback/manual sources",
        "not_recorded": "Mode not recorded",
        "rejected_or_weak": "Rejected or weak sources",
        "review_required": "Review-required sources",
        "company_data_gaps": "Company-data gaps",
        "confidence_cap_reason": "Confidence cap reason",
    }
    return [{"Metric": labels[key], "Value": value} for key, value in summary.items()]


def build_evidence_card_rows(pack, limit=8):
    rows = []
    selected_by_id = {
        source.get("source_id"): source for source in pack.get("selected_sources", []) if source.get("source_id")
    }
    for item in pack.get("evidence", [])[:limit]:
        source = selected_by_id.get(item.get("source_id"), {})
        mode = item.get("evidence_source_mode") or source.get("evidence_source_mode") or "not_recorded"
        rows.append(
            {
                "Source ID": item.get("source_id", ""),
                "Title": item.get("source_title") or item.get("title") or source.get("title", ""),
                "Publisher": item.get("publisher") or source.get("publisher") or _publisher_from_url(source.get("url", "")),
                "Mode": mode,
                "Quality": item.get("source_quality_status") or source.get("source_quality_status") or "not_assessed",
                "Claim": item.get("extracted_claim") or item.get("claim_supported") or item.get("snippet", ""),
                "Commercial relevance": item.get("commercial_relevance") or item.get("commercial_meaning") or item.get("business_user_implication", ""),
                "Confidence effect": item.get("confidence_effect", ""),
                "Review required": bool(item.get("requires_human_review") or item.get("review_required") or mode in {"snippet_only", "metadata_only", "fallback", "manual_input"}),
                "URL": item.get("source_url") or item.get("url") or source.get("url", ""),
            }
        )
    return rows


def build_requirement_coverage_quality_rows(pack):
    evidence_by_req = {}
    for item in pack.get("evidence", []):
        requirement = item.get("requirement_name")
        if requirement and requirement not in evidence_by_req:
            evidence_by_req[requirement] = item
    rows = []
    for requirement in pack.get("requirement_coverage", []):
        name = requirement.get("requirement_name", "")
        evidence = evidence_by_req.get(name, {})
        source_id = (requirement.get("covered_by") or [evidence.get("source_id", "")])[0] if (requirement.get("covered_by") or evidence) else ""
        mode = evidence.get("evidence_source_mode", "not_recorded")
        quality = evidence.get("source_quality_status", "not_assessed")
        covered_count = requirement.get("covered_by_count", len(requirement.get("covered_by", [])))
        coverage_status = _coverage_status(requirement, quality, mode, covered_count)
        rows.append(
            {
                "Requirement": name,
                "Best source": source_id,
                "Evidence mode": mode,
                "Source quality": quality,
                "Coverage status": coverage_status,
                "Confidence impact": evidence.get("confidence_effect") or requirement.get("remaining_gap", ""),
            }
        )
    return rows


def build_evidence_trace_rows(pack):
    rows = []
    selected_by_id = {
        source.get("source_id"): source for source in pack.get("selected_sources", []) if source.get("source_id")
    }
    review_modes = {"snippet_only", "metadata_only", "fallback", "manual_input"}

    for item in pack.get("evidence", []):
        source = selected_by_id.get(item.get("source_id"), {})
        mode = item.get("evidence_source_mode") or source.get("evidence_source_mode") or "not_recorded"
        claim = item.get("extracted_claim") or item.get("claim_supported") or item.get("snippet", "")
        relevance = (
            item.get("commercial_relevance")
            or item.get("commercial_meaning")
            or item.get("business_user_implication")
            or ""
        )
        rows.append(
            {
                "source_id": item.get("source_id", ""),
                "source_title": item.get("source_title") or source.get("source_title") or source.get("title", ""),
                "publisher": item.get("publisher") or source.get("publisher") or _publisher_from_url(source.get("url", "")),
                "evidence_source_mode": mode,
                "source_role": item.get("source_role") or source.get("source_role", ""),
                "source_quality_status": item.get("source_quality_status") or source.get("source_quality_status") or "not_assessed",
                "extracted_claim": claim,
                "commercial_relevance": relevance,
                "confidence_effect": item.get("confidence_effect", ""),
                "review_required": mode in review_modes,
                "url": item.get("source_url") or item.get("url") or source.get("url", ""),
            }
        )
    return rows


def build_traceable_score_rows(pack):
    rows = []
    for dimension, item in (pack.get("traceable_scores") or {}).items():
        supporting = _source_ids(item.get("supporting_evidence", item.get("evidence_supporting_score", [])))
        rows.append(
            {
                "Dimension": item.get("dimension", dimension),
                "Score": item.get("score", ""),
                "Label": item.get("score_label", ""),
                "Score type": item.get("score_type", ""),
                "Supporting sources": ", ".join(supporting[:2]),
                "Weakening evidence": ", ".join(_source_ids(item.get("weakening_evidence", []))[:2]),
                "Missing evidence": ", ".join((item.get("missing_evidence") or [])[:2]),
                "Review required": bool(item.get("review_required")),
                "Confidence cap": item.get("confidence_cap_reason", "") if item.get("confidence_cap_applied") else "",
            }
        )
    return rows


def _source_ids(rows):
    ids = []
    for row in rows:
        if isinstance(row, str) and row:
            ids.append(row)
        elif isinstance(row, dict) and row.get("source_id"):
            ids.append(row["source_id"])
    return ids


def _parse_table(lines):
    if len(lines) < 2:
        return []
    headers = [_clean_cell(cell) for cell in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [_clean_cell(cell) for cell in line.strip("|").split("|")]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append(dict(zip(headers, cells)))
    return rows


def _clean_cell(value):
    return value.replace("\\|", "|").strip()


def _display_source_type(source):
    source_type = source.get("source_type", "")
    title = source.get("title", "").lower()
    url = source.get("url", "").lower()
    publisher = source.get("publisher", "").lower()

    if source_type in {"contrary_or_stabilising_evidence", "contrary_scope_limit"}:
        return source_type
    if "icct" in title or "theicct.org" in url:
        return "specialist_analysis"
    if "stephenson harwood" in title or "shlegal.com" in url:
        return "specialist_analysis"
    if "azolla" in title or "azolla" in publisher or "azolla" in url:
        return "specialist_analysis"
    if source_type == "official_primary" and not _is_official_source(publisher, url, title):
        return "specialist_analysis"
    return source_type


def _display_source_role(source, source_type):
    if source.get("source_role"):
        return source["source_role"]
    requirement = source.get("requirement_name") or source.get("source_requirement", "")
    title = source.get("title", "").lower()
    url = source.get("url", "").lower()

    if source_type == "official_primary":
        return "official_anchor"
    if "emissions_factor" in requirement or "icct" in title or "theicct.org" in url:
        return "data_or_indicator_source"
    if "legal" in requirement or "stephenson harwood" in title or "hfw" in title:
        return "specialist_interpretation"
    if "operator" in requirement or source_type == "company_update":
        return "operator_or_industry_guidance"
    if "contrary" in requirement or "scope" in requirement:
        return "contrary_scope_limit"
    if "price" in requirement or "market" in requirement:
        return "market_pricing"
    if source_type in {"specialist_analysis", "reputable_news"}:
        return "specialist_interpretation"
    return "source_role_unclassified"


def _is_official_source(publisher, url, title):
    official_markers = [
        "gov.uk",
        "uk ets authority",
        "ofgem",
        "environment-agency",
        "legislation.gov.uk",
    ]
    value = " ".join([publisher, url, title])
    return any(marker in value for marker in official_markers)


def _publisher_from_url(url):
    match = re.search(r"https?://(?:www\.)?([^/]+)", url or "")
    return match.group(1) if match else ""


def _source_for_item(selected, item):
    source_id = item.get("source_id")
    return next((source for source in selected if source.get("source_id") == source_id), {})


def _decision_recommendation(pack):
    topic = pack.get("topic", "")
    business_user = pack.get("business_user", "")
    domain = ((pack.get("source_strategy") or {}).get("domain") or "").replace("_", " ")
    if "hormuz" in topic.lower():
        return "Transit, delay, reroute or legal hold based on sanctions, insurance and vessel-flow triggers."
    if "sanctions" in topic.lower():
        return "Approve, escalate, legal hold or reject based on transaction red flags."
    if "uk ets" in topic.lower() or "carbon" in topic.lower():
        return "Assess route applicability and carbon cost exposure."
    if "critical minerals" in topic.lower():
        return "Stockpile, qualify supplier, redesign input, allocate inventory or prepare hold."
    if "cyber" in topic.lower():
        return "Activate resilience controls when recovery, notification or insurance triggers appear."
    if "fiscal" in topic.lower() or "procurement" in topic.lower():
        return "Review bid pipeline, delay contingency, repricing, payment risk and board exposure."
    return f"Decision-support screen for {business_user or domain}."


def _score_display(score):
    if not score:
        return "Not scored"
    value = score.get("score", "")
    label = score.get("score_label", "")
    return f"{value}/5 {label}".strip()


def _quality_sentence(summary):
    return (
        f"{summary['full_text']} full_text, {summary['snippet_only']} snippet_only, "
        f"{summary['review_required']} review-required, {summary['rejected_or_weak']} weak/rejected."
    )


def _first_confidence_cap(pack):
    traceable = pack.get("traceable_scores") or {}
    confidence = traceable.get("confidence", {})
    if confidence.get("confidence_cap_reason"):
        return confidence["confidence_cap_reason"]
    for item in traceable.values():
        if item.get("confidence_cap_reason"):
            return item["confidence_cap_reason"]
    return pack.get("confidence_cap_reason", "")


def _company_data_gap_count(pack):
    count = 0
    for item in pack.get("source_requirements", []) + pack.get("requirement_coverage", []):
        text = " ".join([item.get("requirement_name", ""), item.get("why_required", ""), item.get("remaining_gap", "")]).lower()
        if "company" in text or "operator-specific" in text or "transaction-specific" in text:
            count += 1
    for item in pack.get("evidence", []):
        if item.get("source_role") == "company_required_data":
            count += 1
    return count


def _coverage_status(requirement, quality, mode, covered_count):
    if quality == "needs_targeted_rerun":
        return "missing"
    if "company" in requirement.get("requirement_name", ""):
        return "company_data_required"
    if not covered_count:
        return "missing"
    if quality in {"downgrade", "reject"} or mode in {"snippet_only", "metadata_only"}:
        return "partial"
    return "covered"
