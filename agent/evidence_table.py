SPECIFICITY_TERMS = [
    "route",
    "avoid",
    "delay",
    "vessel",
    "premium",
    "freight",
    "port",
    "transit",
    "cargo",
    "insurance",
]


def build_evidence_table(sources):
    return [_source_to_evidence_row(source) for source in sources]


def assign_evidence_strength(source):
    source_type = source.get("source_type", source.get("inferred_source_type", "unknown"))
    summary = source.get("summary", "").lower()
    is_specific = any(term in summary for term in SPECIFICITY_TERMS)

    if source_type in {"official_primary", "company_update", "energy_chokepoint_data", "insurance_market_evidence"}:
        return "high"
    if source_type in {"market_indicator", "specialist_analysis", "vessel_flow_or_freight_market_evidence", "contrary_or_stabilising_evidence"}:
        return "high" if is_specific else "medium"
    if source_type == "reputable_news":
        return "medium"
    return "low"


def _source_to_evidence_row(source):
    source_type = source.get("source_type", source.get("inferred_source_type", "unknown"))
    summary = source.get("summary", "").strip()

    return {
        "claim": summary or "No claim summary provided.",
        "source_id": source.get("source_id", "S?"),
        "source_type": source_type,
        "evidence_strength": assign_evidence_strength(source),
        "commercial_relevance": source.get("commercial_relevance") or _commercial_relevance(summary, source_type),
        "caveat": source.get("caveat") or _caveat_for_source_type(source_type),
    }


def _commercial_relevance(summary, source_type):
    text = summary.lower()
    if any(term in text for term in ["route", "transit", "vessel", "port"]):
        return "Operational routing and access exposure."
    if any(term in text for term in ["freight", "premium", "insurance", "cost"]):
        return "Cost, insurance, and margin exposure."
    if any(term in text for term in ["stabil", "resume", "normal", "limited"]):
        return "Potentially reduces severity or supports scenario balance."
    if source_type == "company_update":
        return "Direct counterparty or carrier service exposure."
    return "Relevant context for analyst review."


def _caveat_for_source_type(source_type):
    caveats = {
        "official_primary": "May confirm incidents but not full commercial impact.",
        "company_update": "Reflects one firm's network and risk appetite.",
        "market_indicator": "Market moves can reflect several drivers, not only this topic.",
        "reputable_news": "Requires corroboration with primary or specialist sources.",
        "specialist_analysis": "Judgment-based; check assumptions and methodology.",
        "unknown": "Source quality unclear; use only as weak supporting context.",
    }
    return caveats.get(source_type, caveats["unknown"])
