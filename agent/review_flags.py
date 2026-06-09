from datetime import datetime

from agent.confidence_model import has_contrary_or_stabilising_evidence


def generate_review_flags(sources, today=None, evidence_pack=None):
    today = today or datetime.now().date()
    source_types = [source.get("source_type", source.get("inferred_source_type", "unknown")) for source in sources]
    live_source_types = [source.get("source_type", "") for source in sources]
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        return _critical_minerals_flags(evidence_pack, today) or ["No major evidence review flags identified."]
    if domain == "regulatory_carbon_shipping":
        return _uk_ets_flags(evidence_pack, today) or ["No major evidence review flags identified."]
    if domain == "maritime_trade":
        return _hormuz_flags(evidence_pack, today) or ["No major evidence review flags identified."]
    if domain == "uk_fiscal_procurement_risk":
        return _uk_fiscal_procurement_flags(evidence_pack, today) or ["No major evidence review flags identified."]

    flags = []

    if "official_primary" not in source_types:
        flags.append("Missing official_primary source.")
    if "company_update" not in source_types:
        flags.append("Missing company_update source.")
    if len(sources) < 3:
        flags.append("Fewer than three sources supplied.")
    if source_types.count("unknown") >= 2:
        flags.append("Too many unknown sources.")
    if sources and not has_contrary_or_stabilising_evidence(sources):
        flags.append("No contrary or stabilising evidence identified.")
    if any(_is_stale(source.get("date", ""), today) for source in sources):
        flags.append("One or more sources appear older than 90 days.")
    if evidence_pack:
        flags.extend(_live_evidence_flags(live_source_types, evidence_pack, today))

    return flags or ["No major evidence review flags identified."]


def _is_stale(date_value, today):
    if not date_value:
        return False
    try:
        source_date = datetime.strptime(date_value, "%Y-%m-%d").date()
    except ValueError:
        return False
    return (today - source_date).days > 90


def _live_evidence_flags(live_source_types, evidence_pack, today):
    domain = ((evidence_pack or {}).get("source_strategy") or {}).get("domain", "")
    if domain == "critical_minerals_supply_chain":
        return _critical_minerals_flags(evidence_pack, today)
    if domain == "regulatory_carbon_shipping":
        return _uk_ets_flags(evidence_pack, today)
    if domain == "maritime_trade":
        return _hormuz_flags(evidence_pack, today)
    if domain == "uk_fiscal_procurement_risk":
        return _uk_fiscal_procurement_flags(evidence_pack, today)
    flags = []
    if "official_primary" not in live_source_types:
        flags.append("Missing official source in live evidence.")
    if "company_update" not in live_source_types:
        flags.append("Missing company update in live evidence.")
    if "insurance_market_evidence" not in live_source_types:
        flags.append("Missing insurance evidence in live evidence.")
    if "energy_chokepoint_data" not in live_source_types:
        flags.append("Missing energy chokepoint evidence in live evidence.")
    if "contrary_or_stabilising_evidence" not in live_source_types:
        flags.append("Missing contrary evidence in live evidence.")
    if len(live_source_types) < 5:
        flags.append("Fewer than five total live sources selected.")
    if any(_is_stale(source.get("publication_date", ""), today) for source in evidence_pack.get("evidence", [])):
        flags.append("One or more live sources appear older than 90 days.")
    if evidence_pack.get("fetch_failures"):
        flags.append("One or more source fetch failures occurred.")
    if evidence_pack.get("fallback_demo_data_used"):
        flags.append("Curated local source pack used instead of live API search.")
    return flags


def _uk_ets_flags(evidence_pack, today):
    flags = []
    if any(_is_stale(source.get("publication_date", ""), today) for source in evidence_pack.get("evidence", [])):
        flags.append("One or more live sources appear older than 90 days.")
    if evidence_pack.get("fetch_failures"):
        flags.append("One or more source fetch failures occurred.")
    flags.extend(
        [
            "Live UKA price feed is not embedded; manual price input should be refreshed.",
            "Illustrative fuel-consumption assumption requires operator validation.",
            "Emissions factor requires methodology review against verified reporting approach.",
            "Operator-specific route and vessel data are required before final compliance costing.",
            "Future international scope should remain scenario-only unless confirmed.",
            "Reporting and surrender dates require monitoring against current guidance.",
        ]
    )
    return flags


def _hormuz_flags(evidence_pack, today):
    flags = []
    flags.extend(
        [
            "Live source refresh required before operational use.",
            "UK sanctions/OFSI review required for UK-controlled exposure.",
            "Legal review required for any safe-passage/toll/coordination/payment demand.",
            "War-risk cover and exclusions must be confirmed before sailing.",
            "Route-cost assumptions require operator validation.",
            "AIS/vessel-flow recovery must be refreshed before relaxing controls.",
        ]
    )
    if any(_is_stale(source.get("publication_date", ""), today) for source in evidence_pack.get("evidence", [])):
        flags.append("One or more live sources appear older than 90 days.")
    if evidence_pack.get("fetch_failures"):
        flags.append("Snippet-based or failed fetch evidence should be validated before operational use.")
    return flags


def _critical_minerals_flags(evidence_pack, today):
    flags = [
        "Live source refresh required before production or sourcing decisions.",
        "This is a client-type exposure screen, not a company-specific operational assessment.",
        "Bill of materials / input classification must be verified before using the recommendation commercially.",
        "Supplier country, ownership, purchase order and contract data are required for company-specific use.",
        "Inventory by input and customer delivery commitments must be validated before allocation or hold decisions.",
        "Alternative supplier qualification status and technical substitution feasibility require engineering and quality review.",
    ]
    if any(_is_stale(source.get("publication_date", ""), today) for source in evidence_pack.get("evidence", [])):
        flags.append("One or more live sources appear older than 90 days.")
    if evidence_pack.get("fetch_failures"):
        flags.append("Snippet-based or failed fetch evidence should be validated before operational use.")
    return flags


def _uk_fiscal_procurement_flags(evidence_pack, today):
    flags = [
        "Refresh OBR, ONS, HM Treasury and Bank of England evidence before board or bid-committee use.",
        "Verify snippet-only market, procurement and industry sources before operational decisions.",
        "Contractor-specific order book, customer mix, payment terms, margins and working-capital data are required.",
        "Departmental and programme-level bid pipeline exposure should be reviewed before changing bid/no-bid stance.",
        "Board monitoring should be refreshed after fiscal statements, gilt-market stress or material spending-policy updates.",
    ]
    if any(_is_stale(source.get("publication_date", ""), today) for source in evidence_pack.get("evidence", [])):
        flags.append("One or more live sources appear older than 90 days.")
    if evidence_pack.get("fetch_failures"):
        flags.append("One or more source fetch failures occurred; affected rows require manual verification.")
    if evidence_pack.get("fallback_demo_data_used"):
        flags.append("Fallback/demo evidence used; do not treat this as a live-source-backed portfolio case.")
    return flags
