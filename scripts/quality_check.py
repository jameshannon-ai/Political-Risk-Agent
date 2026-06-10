import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase"
sys.path.insert(0, str(ROOT))

from dashboard_helpers import build_selected_source_rows  # noqa: E402


def main():
    checks = [
        _files_exist,
        _framework_guidance,
        _brief_sections,
        _evidence_packs,
        _selected_source_display_checks,
        _dashboard_checks,
        _dashboard_file_check,
        _source_audits,
        _confidence_caps,
        _repo_hygiene,
        _no_api_keys,
    ]
    failures = []
    for check in checks:
        failures.extend(check())
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("Quality check passed.")


def _files_exist():
    failures = []
    for path in [ROOT / "README.md", ROOT / "dashboard_app.py", ROOT / "AGENTS.md"]:
        if not path.exists():
            failures.append(f"Missing {path.name}")
    for name in [
        "hormuz_shipping_operator_brief.md",
        "hormuz_source_audit.md",
        "hormuz_evidence_pack.json",
        "critical_minerals_advanced_manufacturer_brief.md",
        "critical_minerals_source_audit.md",
        "critical_minerals_evidence_pack.json",
        "uk_ets_shipping_operator_brief.md",
        "uk_ets_source_audit.md",
        "uk_ets_evidence_pack.json",
        "sanctions_trade_finance_exposure_brief.md",
        "sanctions_trade_finance_sample.md",
        "sanctions_source_audit.md",
        "sanctions_evidence_pack.json",
        "cyber_business_interruption_brief.md",
        "cyber_source_audit.md",
        "cyber_evidence_pack.json",
        "uk_fiscal_instability_procurement_brief.md",
        "uk_fiscal_instability_procurement_source_audit.md",
        "uk_fiscal_instability_procurement_evidence_pack.json",
    ]:
        if not (SHOWCASE / name).exists():
            failures.append(f"Missing showcase/{name}")
    return failures


def _framework_guidance():
    failures = []
    for path in [
        ROOT / "AGENTS.md",
        ROOT / "docs" / "FRAMEWORK_PRINCIPLES.md",
        ROOT / "docs" / "TASK_BRIEF_TEMPLATE.md",
        ROOT / "scripts" / "create_clean_project_zip.py",
        ROOT / "agent" / "core" / "workflow.py",
        ROOT / "agent" / "core" / "provenance.py",
        ROOT / "agent" / "core" / "scoring.py",
    ]:
        if not path.exists():
            failures.append(f"Missing {path.relative_to(ROOT)}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in ["## Agent / Codex instructions", "AGENTS.md", "docs/FRAMEWORK_PRINCIPLES.md", "docs/TASK_BRIEF_TEMPLATE.md"]:
        if phrase not in readme:
            failures.append(f"README.md missing framework guidance reference: {phrase}")
    for phrase in [
        "A political-risk-to-business-decision framework.",
        "The active dashboard cases are saved Tavily-backed showcase outputs.",
        "fallback_used/fallback_demo_data_used: false",
        "It does not call Tavily, run `live_search_mode`, require `.env`, or spend live-search credits when viewed.",
        "Fallback/demo evidence is not used in the active dashboard cases",
        "Current Evidence Status",
        "Recent Improvements",
        "Known Limitations",
        "How To Review This Project",
        "New Case Workflow",
        "reusable, governed political risk decision-support prototype",
        "not a fully autonomous risk oracle",
        "python3 main.py run-topic",
        "traceable scoring fields",
        "active showcase cases remain curated saved outputs",
        "regenerated Tavily outputs are staged for source-quality review",
        "weak sources are downgraded or rejected",
        "Evidence Trace tabs",
        "Decision Panel",
    ]:
        if phrase not in readme:
            failures.append(f"README.md missing public-readiness phrase: {phrase}")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for phrase in [
        "Current public showcase standard",
        "active dashboard cases are saved Tavily-backed showcase outputs",
        "dashboard must not call Tavily",
        "fallback_used` and `fallback_demo_data_used` should be false",
        "New case lifecycle",
        "business decision",
        "political-risk trigger",
    ]:
        if phrase not in agents:
            failures.append(f"AGENTS.md missing current active-case standard phrase: {phrase}")
    principles = (ROOT / "docs" / "FRAMEWORK_PRINCIPLES.md").read_text(encoding="utf-8")
    for phrase in [
        "Repeatable Case Lifecycle",
        "Political-Risk Trigger To Business Decision",
        "Source Requirement Design",
        "Evidence-To-Score Bridge",
        "Assumption Provenance",
        "Dashboard As Saved-Showcase Presentation Layer",
        "The active showcase cases are saved Tavily-backed outputs.",
        "Fallback/demo evidence is not part of the current active dashboard evidence base.",
    ]:
        if phrase not in principles:
            failures.append(f"FRAMEWORK_PRINCIPLES.md missing framework principle phrase: {phrase}")
    template = (ROOT / "docs" / "TASK_BRIEF_TEMPLATE.md").read_text(encoding="utf-8")
    for phrase in [
        "## Political Risk Trigger",
        "## Business Decision",
        "## Source Requirements",
        "requirement_id",
        "question it answers",
        "preferred source role",
        "decision use",
        "## Evidence-To-Score Logic",
        "## Company Data Required",
        "## Anti-Overclaiming Controls",
    ]:
        if phrase not in template:
            failures.append(f"TASK_BRIEF_TEMPLATE.md missing reusable case-template phrase: {phrase}")
    showcase_readme = (ROOT / "showcase" / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "six active cases are saved Tavily-backed outputs",
        "fallback_used/fallback_demo_data_used: false",
        "does not call Tavily, run `live_search_mode` or spend live-search credits",
    ]:
        if phrase not in showcase_readme:
            failures.append(f"showcase/README.md missing active showcase phrase: {phrase}")
    return failures


def _brief_sections():
    failures = []
    hormuz = _read("hormuz_shipping_operator_brief.md")
    critical_minerals = _read("critical_minerals_advanced_manufacturer_brief.md")
    uk_ets = _read("uk_ets_shipping_operator_brief.md")
    sanctions = _read("sanctions_trade_finance_exposure_brief.md")
    cyber = _read("cyber_business_interruption_brief.md")
    fiscal = _read("uk_fiscal_instability_procurement_brief.md")
    for phrase in ["Operator Decision Stance", "Voyage Decision Matrix", "Sanctions and Safe-Passage Risk", "Dynamic Route-Cost Assessment"]:
        if phrase in hormuz:
            failures.append(f"Hormuz brief still contains old section {phrase}")
    for phrase in [
        "Route Decision Engine",
        "Decision Recommendation",
        "Dashboard Summary",
        "Illustrative Route-Cost Scenario",
        "not company-specific figures",
        "Replace with",
        "Assumption Confidence",
        "Route Decision Optimiser",
        "Sanctions Red-Flag Assessment",
        "Insurance Break-Even Analysis",
        "AIS and Vessel-Flow Signals",
        "Legal hold trigger",
    ]:
        if phrase not in hormuz:
            failures.append(f"Hormuz brief missing {phrase}")
    for phrase in ["Search IndexBox", "Hot Topics Strait of Hormuz crisis", "Skip to main content Iran sets up new mechanism"]:
        if phrase in hormuz:
            failures.append(f"Hormuz brief still contains boilerplate evidence text: {phrase}")
    for phrase in ["Supports operator review and control decisions."]:
        if phrase in hormuz:
            failures.append(f"Hormuz brief contains generic decision-use wording: {phrase}")
    for phrase in [
        "Live source refresh required before operational use.",
        "UK sanctions/OFSI review required for UK-controlled exposure.",
        "Legal review required for any safe-passage/toll/coordination/payment demand.",
        "War-risk cover and exclusions must be confirmed before sailing.",
        "Route-cost assumptions require operator validation.",
        "AIS/vessel-flow recovery must be refreshed before relaxing controls.",
    ]:
        if phrase not in hormuz:
            failures.append(f"Hormuz brief missing review flag: {phrase}")
    if "Preferred option | Legal hold if any sanctions/payment trigger is present; otherwise delay or reroute until insurance, AIS/vessel-flow and official guidance conditions support conditional transit." not in hormuz:
        failures.append("Hormuz preferred option wording is not trigger-based")
    for phrase in [
        "Sanctions Trade Finance Exposure Engine",
        "Decision Recommendation",
        "Dashboard Summary",
        "Transaction Exposure Summary",
        "Goods and End-Use Risk Assessment",
        "Counterparty and Ownership Risk Assessment",
        "Jurisdiction, Route and Payment Risk Assessment",
        "Documentation Quality Assessment",
        "Transaction Decision Engine",
        "Due Diligence Actions",
        "Risk Scorecard",
        "Evidence-To-Score Bridge",
        "Source Requirement Coverage",
        "Source Quality Notes",
        "Selected Sources",
        "Evidence Appendix",
        "Source Audit Summary",
        "Methodology and Review Controls",
        "This is a client-type sanctions and trade-finance exposure screen, not legal advice and not a transaction clearance decision.",
        "Transaction-specific use requires",
    ]:
        if phrase not in sanctions:
            failures.append(f"Sanctions brief missing {phrase}")
    for phrase in ["We use some essential", "cookie", "<script", "<html", "Supports transaction review and compliance controls."]:
        if phrase in sanctions:
            failures.append(f"Sanctions brief contains boilerplate or generic wording: {phrase}")
    for phrase in ["Operator Stance", "Applicability Check", "Carbon Cost Estimate"]:
        if phrase not in uk_ets:
            failures.append(f"UK ETS brief missing {phrase}")
    for phrase in [
        "Start date: 1 July 2026",
        "Vessel threshold: 5,000 GT",
        "Estimated cost: £2,770 per voyage",
        "Refresh UKA price before pricing or contract decisions.",
        "Source Quality Notes",
        "Legal / compliance interpretation",
        "International-route exposure",
    ]:
        if phrase not in uk_ets:
            failures.append(f"UK ETS brief missing polished phrase: {phrase}")
    for phrase in [
        "<script",
        "<!doctype",
        "<html",
        "This sample shows how the agent",
        "Missing insurance evidence",
        "Missing energy chokepoint evidence",
        "Underwriting sign-off",
        "De-escalation update",
    ]:
        if phrase in uk_ets:
            failures.append(f"UK ETS brief contains forbidden fragment: {phrase}")
    if re.search(r"\|\s*Strongest source\s*\|\s*None\s*\|", uk_ets):
        failures.append("UK ETS source requirement coverage has None as strongest source")
    if "Manual fallback" in uk_ets or "Illustrative fuel" in uk_ets:
        confidence_match = re.search(r"\|\s*Confidence\s*\|\s*(\d)/5\s*\|", uk_ets)
        if confidence_match and int(confidence_match.group(1)) >= 5:
            failures.append("UK ETS confidence is 5 despite manual or illustrative inputs")
    for phrase in ["Hull war", "Cargo war", "Marine Insurance Implications"]:
        if phrase in hormuz:
            failures.append(f"Hormuz brief contains marine-insurance-only phrase: {phrase}")
    for phrase in [
        "Critical Minerals Exposure Engine",
        "Decision Recommendation",
        "Dashboard Summary",
        "Exposure Summary",
        "Controlled Input Assessment",
        "Supplier Concentration Assessment",
        "Production Continuity Model",
        "Inventory Runway vs Supplier Qualification Gap",
        "Mitigation Options",
        "Risk Scorecard",
        "Evidence-To-Score Bridge",
        "Source Requirement Coverage",
        "Evidence Appendix",
        "Source Audit Summary",
        "Methodology and Review Controls",
        "production continuity gap",
        "This is a client-type exposure screen, not a company-specific operational assessment.",
        "bill of materials / input classification",
        "supplier country and ownership data",
        "inventory by input",
        "Source Quality Notes",
        "The continuity gap is positive where alternative supplier qualification takes longer than available inventory.",
        "snippet/metadata-supported",
        "illustrative",
        "derived",
    ]:
        if phrase not in critical_minerals:
            failures.append(f"Critical minerals brief missing {phrase}")
    for phrase in [
        "We use some essential",
        "cookie",
        "cargo",
        "collateral",
        "underwriting",
        "demurrage",
        "voyage",
    ]:
        if phrase in critical_minerals:
            failures.append(f"Critical minerals brief contains forbidden cross-domain or boilerplate wording: {phrase}")
    if "company-specific operational assessment" in critical_minerals and "not a company-specific operational assessment" not in critical_minerals:
        failures.append("Critical minerals brief risks claiming company-specific precision")
    for phrase in ["Hull war", "Cargo war", "War-risk premium", "Marine Insurance Implications"]:
        if phrase in sanctions:
            failures.append(f"Sanctions brief contains marine-insurance-only phrase: {phrase}")
    for phrase in [
        "Cyber Business Interruption Engine",
        "Decision Recommendation",
        "Scope and Specificity",
        "Dashboard Summary",
        "Incident Exposure Summary",
        "Operational Dependency Assessment",
        "Business Interruption Model",
        "Downtime / Revenue-at-Risk Assessment",
        "Regulatory Notification Assessment",
        "Insurance and Claims Readiness Assessment",
        "Supplier / MSP Dependency Risk",
        "Mitigation Options",
        "Risk Scorecard",
        "Evidence-To-Score Bridge",
        "Source Requirement Coverage",
        "Source Quality Notes",
        "Selected Sources",
        "Evidence Appendix",
        "Source Audit Summary",
        "Methodology and Review Controls",
        "resilience gap",
        "business interruption exposure",
        "This is a client-type cyber business interruption exposure screen, not technical cybersecurity advice, legal advice or an insurance coverage determination.",
        "Company-specific use requires",
        "affected systems and process map",
        "daily revenue by channel / service",
        "RTO / RPO",
        "cyber insurance policy wording",
        "supplier / MSP dependency map",
        "negative three-day resilience gap",
    ]:
        if phrase not in cyber:
            failures.append(f"Cyber brief missing {phrase}")
    for phrase in [
        "firewall configuration",
        "malware reverse engineering",
        "exploit remediation",
        "network hardening",
        "technical cybersecurity advice:",
        "voyage",
        "demurrage",
        "vessel",
        "charter",
        "cargo",
        "trade finance",
    ]:
        if phrase in cyber:
            failures.append(f"Cyber brief contains technical or cross-domain wording: {phrase}")
    for phrase in [
        "UK fiscal instability and public-sector procurement delay risk",
        "UK infrastructure contractor",
        "political-economy risk",
        "bid pipeline",
        "payment-risk monitoring",
        "contract repricing",
        "working-capital exposure",
        "Scoring Traceability",
        "Source Governance",
        "Human Review And Company Data Required",
    ]:
        if phrase not in fiscal:
            failures.append(f"Fiscal procurement brief missing {phrase}")
    for phrase in [
        "Missing insurance evidence",
        "energy chokepoint",
        "underwriting",
        "carrier/company updates",
        "Illustrative Route-Cost Scenario",
        "voyage",
        "cargo",
        "We use some essential",
        "<script",
    ]:
        if phrase in fiscal:
            failures.append(f"Fiscal procurement brief contains irrelevant or raw wording: {phrase}")
    if "| Confidence | 4/5" in fiscal or "| Confidence score | 4/5 |" in fiscal:
        failures.append("Fiscal procurement confidence should remain capped at 3/5")
    return failures


def _evidence_packs():
    failures = []
    for name in ["hormuz_evidence_pack.json", "uk_ets_evidence_pack.json", "sanctions_evidence_pack.json", "cyber_evidence_pack.json"]:
        pack = json.loads((SHOWCASE / name).read_text(encoding="utf-8"))
        for key in ["source_plan", "source_requirements", "requirement_coverage", "quantified_evidence_readout"]:
            if key not in pack:
                failures.append(f"{name} missing {key}")
    critical_pack = json.loads((SHOWCASE / "critical_minerals_evidence_pack.json").read_text(encoding="utf-8"))
    if critical_pack.get("search_provider") != "tavily" or critical_pack.get("source_provider") != "tavily":
        failures.append("Critical minerals showcase pack is not marked as tavily/tavily")
    if critical_pack.get("fallback_used") or critical_pack.get("fallback_demo_data_used"):
        failures.append("Critical minerals showcase pack incorrectly shows fallback data")
    if critical_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("Critical minerals showcase pack is not marked as live source retrieval")
    labels = json.dumps(critical_pack.get("scenario_inputs", {}))
    for phrase in ['"label": "illustrative"', '"label": "derived"']:
        if phrase not in labels:
            failures.append(f"Critical minerals scenario inputs missing label {phrase}")
    confidence_score = critical_pack.get("evidence_to_score_bridge", {}).get("confidence", {}).get("score")
    if confidence_score is not None and confidence_score >= 5:
        failures.append("Critical minerals confidence should remain below 5")
    for evidence in critical_pack.get("evidence", []):
        claim = evidence.get("claim_supported", "")
        if not claim or len(claim.split()) < 8:
            failures.append(f"Critical minerals evidence claim is not readable for {evidence.get('source_id')}")
        if any(fragment in claim for fragment in ["We use some essential", "cookie", "<script", "<html", "2019; 0"]):
            failures.append(f"Critical minerals evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if evidence.get("decision_use") in ("Supports operator review and control decisions.", "", None):
            failures.append(f"Critical minerals evidence needs specific decision use for {evidence.get('source_id')}")
        refresh = evidence.get("refresh_requirement", "")
        if any(term in refresh for term in ["cargo", "collateral", "underwriting", "demurrage", "voyage"]):
            failures.append(f"Critical minerals refresh trigger contains irrelevant wording for {evidence.get('source_id')}")
    uk_ets_pack = json.loads((SHOWCASE / "uk_ets_evidence_pack.json").read_text(encoding="utf-8"))
    if uk_ets_pack.get("search_provider") != "tavily" or uk_ets_pack.get("source_provider") != "tavily":
        failures.append("UK ETS showcase pack is not marked as tavily/tavily")
    if uk_ets_pack.get("fallback_used") or uk_ets_pack.get("fallback_demo_data_used"):
        failures.append("UK ETS showcase pack incorrectly shows fallback data")
    if uk_ets_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("UK ETS showcase pack is not marked as live source retrieval")
    if uk_ets_pack.get("quantified_evidence_readout", {}).get("high_weight_source_count", 0) < 1:
        failures.append("UK ETS showcase pack should show at least one high-weight source")
    for evidence in uk_ets_pack.get("evidence", []):
        claim = evidence.get("claim_supported", "")
        if claim.startswith(("Hot Topics", "Open search bar", "on GOV.UK")):
            failures.append(f"UK ETS evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if any(fragment in claim for fragment in ["<script", "<!doctype", "<html"]):
            failures.append(f"UK ETS evidence claim contains raw HTML for {evidence.get('source_id')}")
        if not any(":" in fact for fact in evidence.get("quantified_facts", [])):
            failures.append(f"UK ETS quantified facts are not labelled for {evidence.get('source_id')}")
    for source in uk_ets_pack.get("selected_sources", []):
        title = source.get("title", "")
        if ("ICCT" in title or "Stephenson Harwood" in title or "Azolla" in title) and source.get("source_type") == "official_primary":
            failures.append(f"UK ETS selected source taxonomy overstates specialist source as official_primary: {title}")
        for field in ["source_role", "source_value_explanation", "decision_use", "evidence_weight", "requirement_name", "url"]:
            if not source.get(field):
                failures.append(f"UK ETS selected source missing {field}: {source.get('source_id')}")
    sanctions_pack = json.loads((SHOWCASE / "sanctions_evidence_pack.json").read_text(encoding="utf-8"))
    if sanctions_pack.get("search_provider") != "tavily" or sanctions_pack.get("source_provider") != "tavily":
        failures.append("Sanctions showcase pack is not marked as tavily/tavily")
    if sanctions_pack.get("fallback_used") or sanctions_pack.get("fallback_demo_data_used"):
        failures.append("Sanctions showcase pack incorrectly shows fallback data")
    if sanctions_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("Sanctions showcase pack is not marked as live source retrieval")
    if len(sanctions_pack.get("source_requirements", [])) < 9:
        failures.append("Sanctions showcase pack should include nine source requirements")
    if not sanctions_pack.get("transaction_decision_model"):
        failures.append("Sanctions showcase pack missing transaction decision model")
    confidence_score = sanctions_pack.get("evidence_to_score_bridge", {}).get("confidence", {}).get("score")
    if confidence_score is not None and confidence_score >= 5:
        failures.append("Sanctions confidence should remain below 5")
    for source in sanctions_pack.get("selected_sources", []):
        for field in ["source_role", "source_value_explanation", "decision_use", "evidence_weight", "requirement_name", "url"]:
            if not source.get(field):
                failures.append(f"Sanctions selected source missing {field}: {source.get('source_id')}")
        if source.get("publisher") in {"Skadden", "Baker McKenzie Global Sanctions and Export Controls Blog"} and source.get("source_type") == "official_primary":
            failures.append(f"Sanctions specialist source is incorrectly official_primary: {source.get('title')}")
    for evidence in sanctions_pack.get("evidence", []):
        claim = evidence.get("claim_supported", "")
        if not claim or len(claim.split()) < 8:
            failures.append(f"Sanctions evidence claim is not readable for {evidence.get('source_id')}")
        if any(fragment in claim for fragment in ["We use some essential", "cookie", "<script", "<html", "Skip to main content"]):
            failures.append(f"Sanctions evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if evidence.get("decision_use") in ("Supports transaction review and compliance controls.", "", None):
            failures.append(f"Sanctions evidence needs specific decision use for {evidence.get('source_id')}")
    cyber_pack = json.loads((SHOWCASE / "cyber_evidence_pack.json").read_text(encoding="utf-8"))
    if cyber_pack.get("search_provider") != "tavily" or cyber_pack.get("source_provider") != "tavily":
        failures.append("Cyber showcase pack is not marked as tavily/tavily")
    if cyber_pack.get("fallback_used") or cyber_pack.get("fallback_demo_data_used"):
        failures.append("Cyber showcase pack incorrectly shows fallback data")
    if cyber_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("Cyber showcase pack is not marked as live source retrieval")
    if len(cyber_pack.get("source_requirements", [])) < 9:
        failures.append("Cyber showcase pack should include nine source requirements")
    model = cyber_pack.get("cyber_business_interruption_model", {})
    if model.get("business_interruption_exposure") != 10000000:
        failures.append("Cyber business interruption exposure should be 10,000,000 in the illustrative scenario")
    if model.get("resilience_gap_days") != -3:
        failures.append("Cyber resilience gap should be -3 days in the illustrative scenario")
    labels = json.dumps(cyber_pack.get("scenario_inputs", {}))
    for phrase in ['"label": "illustrative"', '"label": "derived"', '"label": "source-supported"', '"label": "company-provided"']:
        if phrase not in labels:
            failures.append(f"Cyber scenario inputs missing label {phrase}")
    confidence_score = cyber_pack.get("evidence_to_score_bridge", {}).get("confidence", {}).get("score")
    if confidence_score is not None and confidence_score >= 5:
        failures.append("Cyber confidence should remain below 5")
    for source in cyber_pack.get("selected_sources", []):
        for field in ["source_role", "source_value_explanation", "decision_use", "evidence_weight", "requirement_name", "url"]:
            if not source.get(field):
                failures.append(f"Cyber selected source missing {field}: {source.get('source_id')}")
    for evidence in cyber_pack.get("evidence", []):
        claim = evidence.get("claim_supported", "")
        if not claim or len(claim.split()) < 8:
            failures.append(f"Cyber evidence claim is not readable for {evidence.get('source_id')}")
        if any(fragment in claim for fragment in ["We use some essential", "cookie", "<script", "<html", "Skip to main content"]):
            failures.append(f"Cyber evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if evidence.get("decision_use") in ("Supports exposure review, control adjustment and monitoring triggers.", "", None):
            failures.append(f"Cyber evidence needs specific decision use for {evidence.get('source_id')}")
    for source in cyber_pack.get("selected_sources", []):
        publisher = source.get("publisher", "")
        if publisher in {"Marsh", "Aon", "WTW", "Allianz", "Howden"} and source.get("source_role") == "official_anchor":
            failures.append(f"Cyber insurer/broker source is overstated as official anchor: {source.get('source_id')}")
        if publisher in {"National Cyber Security Centre", "GOV.UK / Department for Science, Innovation and Technology", "Information Commissioner’s Office", "Financial Conduct Authority"}:
            if source.get("source_role") not in {"official_anchor", "regulatory_guidance", "data_or_indicator_source", "contrary_scope_limit"}:
                failures.append(f"Cyber official/regulator source has overstated or inaccurate role: {source.get('source_id')}")
    fiscal_pack = json.loads((SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json").read_text(encoding="utf-8"))
    if fiscal_pack.get("search_provider") != "tavily" or fiscal_pack.get("source_provider") != "tavily":
        failures.append("Fiscal procurement showcase pack is not marked as tavily/tavily")
    if fiscal_pack.get("fallback_used") or fiscal_pack.get("fallback_demo_data_used"):
        failures.append("Fiscal procurement showcase pack incorrectly shows fallback data")
    if fiscal_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("Fiscal procurement showcase pack is not marked as live source retrieval")
    if fiscal_pack.get("traceable_scores", {}).get("confidence", {}).get("score", 5) > 3:
        failures.append("Fiscal procurement confidence should remain capped at 3/5")
    l6 = next((source for source in fiscal_pack.get("selected_sources", []) if source.get("source_id") == "L6"), {})
    if l6.get("source_type") != "official_primary" or "nao.org.uk" not in l6.get("url", ""):
        failures.append("Fiscal procurement programme-delay source should be NAO official evidence")
    l9 = next((source for source in fiscal_pack.get("selected_sources", []) if source.get("source_id") == "L9"), {})
    if l9.get("source_type") == "official_primary":
        failures.append("Fiscal procurement industry/payment source is overstated as official_primary")
    if not any(item.get("coverage_grade") in {"direct_snippet_only", "partial_or_indirect", "historical_context_only"} for item in fiscal_pack.get("requirement_coverage", [])):
        failures.append("Fiscal procurement coverage should be graded beyond binary full coverage")
    for source in fiscal_pack.get("selected_sources", []):
        for field in ["source_role", "source_value_explanation", "decision_use", "evidence_weight", "requirement_name", "url"]:
            if not source.get(field):
                failures.append(f"Fiscal procurement selected source missing {field}: {source.get('source_id')}")
    for evidence in fiscal_pack.get("evidence", []):
        for field in [
            "source_claim",
            "extracted_evidence",
            "analyst_inference",
            "inference_strength",
            "evidence_type",
            "quoted_excerpt_used",
            "extraction_confidence",
            "evidence_source_mode",
            "source_limitations",
            "why_source_was_selected",
            "why_source_matters_for_decision",
        ]:
            if not evidence.get(field):
                failures.append(f"Fiscal procurement evidence missing {field}: {evidence.get('source_id')}")
        claim = " ".join([evidence.get("source_claim", ""), evidence.get("extracted_evidence", ""), evidence.get("analyst_inference", "")])
        if any(fragment in claim for fragment in ["We use some essential", "cookie", "<script", "<html"]):
            failures.append(f"Fiscal procurement evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if evidence.get("evidence_source_mode") == "snippet_only" and not evidence.get("requires_human_review"):
            failures.append(f"Fiscal procurement snippet-only evidence should require review: {evidence.get('source_id')}")
        refresh = evidence.get("refresh_trigger") or evidence.get("refresh_requirement", "")
        if any(term in refresh for term in ["underwriting", "voyage", "cargo", "chokepoint"]):
            failures.append(f"Fiscal procurement refresh trigger contains irrelevant wording for {evidence.get('source_id')}")
    for dimension, score in fiscal_pack.get("traceable_scores", {}).items():
        if not score.get("evidence_supporting_score"):
            failures.append(f"Fiscal procurement traceable score missing supporting evidence: {dimension}")
        if not score.get("reason_score_is_capped"):
            failures.append(f"Fiscal procurement traceable score missing cap reason: {dimension}")
    hormuz_pack = json.loads((SHOWCASE / "hormuz_evidence_pack.json").read_text(encoding="utf-8"))
    if hormuz_pack.get("search_provider") != "tavily" or hormuz_pack.get("source_provider") != "tavily":
        failures.append("Hormuz showcase pack is not marked as tavily/tavily")
    if hormuz_pack.get("fallback_used") or hormuz_pack.get("fallback_demo_data_used"):
        failures.append("Hormuz showcase pack incorrectly shows fallback data")
    if hormuz_pack.get("evidence_mode") != "Live source retrieval":
        failures.append("Hormuz showcase pack is not marked as live source retrieval")
    if any(item.get("decision_use") == "Supports operator review and control decisions." for item in hormuz_pack.get("selected_sources", [])):
        failures.append("Hormuz selected sources still contain generic decision use")
    if len(hormuz_pack.get("source_plan", {}).get("decision_questions", [])) != 6:
        failures.append("Hormuz source plan should contain exactly six core decision questions")
    for source in hormuz_pack.get("selected_sources", []):
        if source.get("publisher") == "indexbox.io" and source.get("source_type") == "official_primary":
            failures.append("Hormuz evidence pack incorrectly classifies indexbox.io as official_primary")
    official_cov = next((item for item in hormuz_pack.get("requirement_coverage", []) if item.get("requirement_name") == "official_maritime_security"), None)
    if official_cov:
        if official_cov.get("coverage_status") == "covered":
            failures.append("official_maritime_security should not be fully covered without a true official maritime/security source")
        if "Requires UKMTO, IMO, ICS, BIMCO, INTERTANKO, OCIMF or government advisory refresh before operational use." not in official_cov.get("remaining_gap", ""):
            failures.append("official_maritime_security gap wording is not specific enough")
    for evidence in hormuz_pack.get("evidence", []):
        claim = evidence.get("claim_supported", "")
        if any(fragment in claim for fragment in ["Search IndexBox", "Hot Topics Strait of Hormuz crisis", "Skip to main content", "<script", "<html"]):
            failures.append(f"Hormuz evidence claim still looks like boilerplate for {evidence.get('source_id')}")
        if not any(":" in fact for fact in evidence.get("quantified_facts", [])):
            failures.append(f"Hormuz quantified facts are not labelled for {evidence.get('source_id')}")
        if evidence.get("decision_use") == "Supports operator review and control decisions.":
            failures.append(f"Hormuz evidence uses generic decision-use wording for {evidence.get('source_id')}")
    return failures


def _selected_source_display_checks():
    failures = []
    for label, name in [
        ("UK ETS", "uk_ets_evidence_pack.json"),
        ("Hormuz", "hormuz_evidence_pack.json"),
        ("Critical minerals", "critical_minerals_evidence_pack.json"),
        ("Sanctions", "sanctions_evidence_pack.json"),
        ("Cyber", "cyber_evidence_pack.json"),
        ("Fiscal", "uk_fiscal_instability_procurement_evidence_pack.json"),
    ]:
        pack = json.loads((SHOWCASE / name).read_text(encoding="utf-8"))
        rows = build_selected_source_rows(pack)
        if not rows:
            failures.append(f"{label} selected source dashboard table has no rows")
            continue
        for row in rows:
            if not row.get("URL"):
                failures.append(f"{label} selected source missing URL: {row.get('Source ID')}")
            if not row.get("Source role") or row.get("Source role") == "source_role_unclassified":
                failures.append(f"{label} selected source missing conservative source role: {row.get('Source ID')}")
            if not row.get("Source type"):
                failures.append(f"{label} selected source missing source type: {row.get('Source ID')}")
            if label == "UK ETS" and ("ICCT" in row.get("Title", "") or "Stephenson Harwood" in row.get("Title", "")):
                if row.get("Source type") == "official_primary":
                    failures.append(f"UK ETS display taxonomy overstates specialist source as official_primary: {row.get('Title')}")
    return failures


def _source_audits():
    failures = []
    for name in ["hormuz_source_audit.md", "uk_ets_source_audit.md", "sanctions_source_audit.md", "uk_fiscal_instability_procurement_source_audit.md"]:
        text = _read(name)
        for phrase in ["Research Plan", "Source Requirement Coverage", "Quantified Evidence Summary"]:
            if phrase not in text:
                failures.append(f"{name} missing {phrase}")
    uk_ets_audit = _read("uk_ets_source_audit.md")
    hormuz_audit = _read("hormuz_source_audit.md")
    critical_audit = _read("critical_minerals_source_audit.md")
    sanctions_audit = _read("sanctions_source_audit.md")
    cyber_audit = _read("cyber_source_audit.md")
    fiscal_audit = _read("uk_fiscal_instability_procurement_source_audit.md")
    for phrase in [
        "Refresh UKA price before pricing or contract decisions.",
        "Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
        "Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
        "Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
        "Review emissions factor methodology with verifier / MRV process.",
        "Source Quality Notes",
    ]:
        if phrase not in uk_ets_audit:
            failures.append(f"UK ETS audit missing refresh priority: {phrase}")
    if "Strongest evidence category: contrary_or_stabilising_evidence" in hormuz_audit or "Strongest sources | L7 — STL.News" in hormuz_audit:
        failures.append("Hormuz source audit overstates weak de-escalation evidence as strongest source")
    for phrase in [
        "Source Quality Notes",
        "Refresh if export-control rules or licensing practice changes.",
        "Refresh if China-linked export licences tighten or ease.",
        "Refresh if rare earth magnet shortage or price signals change.",
        "Refresh if alternative supplier qualification assumptions change.",
        "Refresh when company BOM, supplier, inventory or contract data becomes available.",
    ]:
        if phrase not in critical_audit:
            failures.append(f"Critical minerals audit missing phrase: {phrase}")
    for phrase in ["carrier/company updates", "underwriting", "cargo", "voyage", "demurrage"]:
        if phrase in critical_audit:
            failures.append(f"Critical minerals audit contains irrelevant wording: {phrase}")
    for phrase in [
        "Source Quality Notes",
        "Evidence-To-Score Bridge",
        "Selected Sources",
        "Transaction-specific use requires",
        "Refresh if sanctions designations, OFSI guidance or export-control rules change.",
    ]:
        if phrase not in sanctions_audit:
            failures.append(f"Sanctions audit missing phrase: {phrase}")
    for phrase in [
        "Research Plan",
        "Source Requirement Coverage",
        "Quantified Evidence Summary",
        "Source Quality Notes",
        "Business interruption exposure",
        "Resilience gap",
        "Refresh if cyber insurance waiting periods, exclusions or claims conditions change.",
        "Refresh if NCSC threat posture or ransomware reporting changes.",
        "Refresh when company systems map, revenue exposure, policy wording, recovery time or supplier/MSP dependency data becomes available.",
    ]:
        if phrase not in cyber_audit:
            failures.append(f"Cyber audit missing phrase: {phrase}")
    for phrase in [
        "Provenance And Extraction Limits",
        "Scoring Traceability",
        "Scenario And Exposure Limits",
        "Refresh OBR outlook and ONS public-finance data after new releases.",
        "Replace public evidence with contractor order book, customer mix, payment terms, margin and working-capital data before operational use.",
        "Validate payment terms, retentions, aged receivables, margins and working-capital exposure with company data.",
    ]:
        if phrase not in fiscal_audit:
            failures.append(f"Fiscal procurement audit missing phrase: {phrase}")
    for phrase in ["underwriting", "cargo", "voyage", "carrier/company updates", "Illustrative Route-Cost Scenario"]:
        if phrase in fiscal_audit:
            failures.append(f"Fiscal procurement audit contains irrelevant wording: {phrase}")
    return failures


def _dashboard_checks():
    failures = []
    dashboard_path = ROOT / "dashboard_app.py"
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    dashboard = dashboard_path.read_text(encoding="utf-8") if dashboard_path.exists() else ""

    if "streamlit" not in requirements:
        failures.append("requirements.txt missing streamlit")
    if "TavilyClient" in dashboard or "live_search_mode" in dashboard:
        failures.append("dashboard_app.py contains live retrieval references")
    if ".env" in dashboard:
        failures.append("dashboard_app.py should not read or reference .env")
    for phrase in [
        'SHOWCASE / "uk_ets_evidence_pack.json"',
        'SHOWCASE / "uk_ets_shipping_operator_brief.md"',
        'SHOWCASE / "uk_ets_source_audit.md"',
        'SHOWCASE / "hormuz_evidence_pack.json"',
        'SHOWCASE / "hormuz_shipping_operator_brief.md"',
        'SHOWCASE / "hormuz_source_audit.md"',
        'SHOWCASE / "critical_minerals_evidence_pack.json"',
        'SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md"',
        'SHOWCASE / "critical_minerals_source_audit.md"',
        'SHOWCASE / "sanctions_evidence_pack.json"',
        'SHOWCASE / "sanctions_trade_finance_exposure_brief.md"',
        'SHOWCASE / "sanctions_source_audit.md"',
        'SHOWCASE / "cyber_evidence_pack.json"',
        'SHOWCASE / "cyber_business_interruption_brief.md"',
        'SHOWCASE / "cyber_source_audit.md"',
        'SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json"',
        'SHOWCASE / "uk_fiscal_instability_procurement_brief.md"',
        'SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md"',
        'st.sidebar.radio("Cases"',
        "Hormuz Route Decision Engine",
        "Critical Minerals Exposure Engine",
        "Sanctions Trade Finance Exposure Engine",
        "Cyber Business Interruption Engine",
        "UK Fiscal Instability & Procurement Delay Risk",
        "Political economy risk for a UK infrastructure contractor bidding for government-funded transport and energy projects.",
        "Activate controls",
        "£2,770 per voyage",
        "£866,562 annualised",
        "£48/tCO2e",
        "57.71 tCO2e",
        "£2,769.98",
        "£16,619.90",
        "£72,213.48",
        "£866,561.79",
        "Manual fallback used because no live UKA price feed is embedded.",
        "Scenario",
        "UKA price",
        "Estimated cost per voyage",
        "£38.40/tCO2e",
        "£48.00/tCO2e",
        "£57.60/tCO2e",
        "£2,215.99",
        "£3,323.98",
        "saved showcase artefacts only",
        "UK ETS Maritime Expansion: Carbon Cost Exposure",
        "Current showcase cases:",
        "The dashboard is designed as an expandable case portfolio.",
        "This dashboard demonstrates a reusable political-risk workflow: identify a political, geopolitical, regulatory or state-linked trigger; map it to business exposure; assess the evidence base; and convert it into a decision-support output with source caveats and company-data requirements.",
        "Each case starts with the business decision, then shows the model output, evidence base, source caveats and company-data needed for operational use.",
        "UK ETS: regulatory policy into route-level carbon cost exposure",
        "Hormuz: geopolitical/security risk into transit, delay, reroute or legal-hold decision",
        "Critical Minerals: strategic competition into production-continuity risk",
        "Sanctions Trade Finance: sanctions/export controls into transaction approval, escalation, legal hold or rejection",
        "Cyber Business Interruption: geopolitical cyber and ransomware risk into downtime, notification, insurance and recovery decisions",
        "UK Fiscal: political economy risk into bid pipeline review, delay contingency, repricing and board exposure reporting",
        "Decision Summary",
        "First-Reader Summary",
        "Business problem",
        "Political risk trigger",
        "UK carbon regulation is expanding into maritime emissions, creating new compliance and cost exposure for in-scope shipping routes.",
        "State-linked disruption, transit-control threats, sanctions/payment risk and regional security escalation can change whether a voyage remains commercially and legally viable.",
        "Export controls, strategic competition and concentration of rare earth magnet supply can interrupt production-critical inputs for UK manufacturers.",
        "Government sanctions, end-use controls and enforcement expectations can turn transaction exposure into approval, escalation, legal-hold or rejection risk.",
        "State-linked cyber activity, ransomware ecosystems, national resilience policy and supplier/MSP dependency can turn cyber disruption into business interruption, notification and insurance-response risk.",
        "UK fiscal pressure, public spending trade-offs, gilt-market sensitivity and political budget choices can change procurement confidence and programme timing.",
        "Decision supported",
        "Evidence-to-output logic",
        "Company data needed",
        "Evidence Category Guide",
        "Political/regulatory trigger evidence",
        "Business exposure evidence",
        "Illustrative scenario assumptions",
        "Company-required data",
        "UK ETS maritime expansion turns carbon policy into a route-level operating cost for in-scope UK voyages.",
        "Strait of Hormuz disruption can turn a voyage decision into a combined sanctions, insurance, detention and route-cost problem.",
        "A UK manufacturer may lose access to rare earth magnet inputs before an alternative supplier can be qualified.",
        "A trade finance transaction can become unacceptable where goods, counterparties, ownership, route, payment or documentation create sanctions/export-control exposure.",
        "Cyber disruption can turn digital trading, payment, fulfilment or service dependency into downtime, customer harm and revenue loss.",
        "Fiscal credibility, gilt-market sensitivity and departmental budget uncertainty can affect public-sector infrastructure awards, payment assumptions and working-capital exposure.",
        "Resilience Gap Summary",
        "Requirement Coverage Summary",
        "Scoring Traceability",
        "Source Governance Summary",
        "Traceable Scorecard",
        "build_traceable_score_rows",
        "Decision Panel",
        "build_decision_panel_rows",
        "Evidence Quality Summary",
        "build_evidence_quality_rows",
        "Key Judgements / Evidence Cards",
        "build_evidence_card_rows",
        "build_requirement_coverage_quality_rows",
        "Evidence Trace",
        "build_evidence_trace_rows",
        "Selected Sources",
        "build_selected_source_rows",
        "LinkColumn",
        "Continuity Summary",
        "Risk",
        "Confidence",
        "Cost/voyage",
        "Annual cost",
        "Break-even",
        "Gap",
        "Inventory",
        "Qualification",
        "Legal hold",
        "Missing data",
        "Resilience gap",
        "Revenue at risk",
        "Expected outage",
        "Production continuity gap",
        "substitution feasibility needs stronger magnet-specific engineering",
        "company BOM, supplier ownership/country, inventory, contracts and qualification data are required before operational use",
        "This is a client-type cyber business interruption exposure screen, not technical cybersecurity advice, legal advice or an insurance coverage determination.",
    ]:
        if phrase not in dashboard:
            failures.append(f"dashboard_app.py does not read the expected showcase file: {phrase}")
    for phrase in ["TavilyClient", "live_search_mode", 'st.json', 'st.write(pack)', 'st.markdown("empty', "st.markdown('empty"]:
        if phrase in dashboard:
            failures.append(f"dashboard_app.py contains forbidden dashboard presentation fragment: {phrase}")
    for phrase in [
        "How to read this dashboard",
        "Start with the decision recommendation.",
        "Check the model output and key trigger.",
        "Review source caveats and company-data requirements before treating the result as operational.",
    ]:
        if phrase in dashboard:
            failures.append(f"dashboard_app.py still contains old reading guidance phrase: {phrase}")
    if '"Decision": "Resilience controls"' in dashboard:
        failures.append("Cyber decision metric should use short display text, not Resilience controls")
    if "def _build_cyber_overview_metrics" in dashboard:
        cyber_metric_block = dashboard.split("def _build_cyber_overview_metrics", 1)[1].split("def _build_carbon_cost_metrics", 1)[0]
        if '"Risk": _extract_field_value(brief, "Overall risk level")' in cyber_metric_block:
            failures.append("Cyber risk metric should not render an empty unsupported risk card")
    return failures


def _dashboard_file_check():
    failures = []
    script = ROOT / "scripts" / "check_dashboard_files.py"
    if not script.exists():
        return ["Missing scripts/check_dashboard_files.py"]
    try:
        import subprocess

        result = subprocess.run(
            ["python3", str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        return [f"Unable to run dashboard file check: {exc}"]
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        failures.append(f"Dashboard file check failed: {output}")
    return failures


def _repo_hygiene():
    failures = []
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for phrase in [".env", ".venv/", ".DS_Store", "*.zip", "outputs/*.md", "outputs/*.json", "!outputs/.gitkeep", "dist/"]:
        if phrase not in gitignore:
            failures.append(f".gitignore missing {phrase}")
    tracked = (ROOT / ".git").exists()
    if tracked:
        git_info = (ROOT / ".git").resolve()
        if not git_info.exists():
            failures.append(".git metadata is not accessible for hygiene checks")
    env_path = ROOT / ".env"
    if env_path.exists():
        try:
            import subprocess

            result = subprocess.run(
                ["git", "ls-files", ".env"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.stdout.strip():
                failures.append(".env is tracked by git and should remain untracked")
            generated = subprocess.run(
                ["git", "ls-files", "outputs/*.md", "outputs/*.json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            tracked_generated = [line for line in generated.stdout.splitlines() if line.strip()]
            if tracked_generated:
                failures.append("Generated output files are tracked by git and should remain untracked")
        except Exception:
            failures.append("Unable to verify whether .env is tracked")
    export_script = (ROOT / "scripts" / "create_clean_project_zip.py").read_text(encoding="utf-8")
    for phrase in [".env", ".venv", ".git", "outputs", "dist", "political-risk-agent-clean.zip"]:
        if phrase not in export_script:
            failures.append(f"create_clean_project_zip.py missing export exclusion or output reference: {phrase}")
    return failures


def _confidence_caps():
    failures = []
    for name in ["hormuz_evidence_pack.json", "uk_ets_evidence_pack.json", "sanctions_evidence_pack.json"]:
        pack = json.loads((SHOWCASE / name).read_text(encoding="utf-8"))
        if pack.get("fallback_demo_data_used"):
            confidence = pack.get("quantified_evidence_readout", {}).get("confidence_cap", "")
            if "capped" not in confidence.lower():
                failures.append(f"{name} does not explain fallback confidence cap")
    uk_ets_pack = json.loads((SHOWCASE / "uk_ets_evidence_pack.json").read_text(encoding="utf-8"))
    if "manual UKA price" in json.dumps(uk_ets_pack) or uk_ets_pack.get("calculator_assumptions"):
        confidence = uk_ets_pack.get("quantified_evidence_readout", {}).get("confidence_cap", "")
        if "capped below 5" not in confidence:
            failures.append("UK ETS confidence is not capped below 5 with manual/illustrative inputs")
    return failures


def _no_api_keys():
    failures = []
    paths = [
        ROOT / "README.md",
        ROOT / "showcase" / "README.md",
        ROOT / "showcase" / "hormuz_shipping_operator_brief.md",
        ROOT / "showcase" / "hormuz_source_audit.md",
        ROOT / "showcase" / "hormuz_evidence_pack.json",
        ROOT / "showcase" / "critical_minerals_advanced_manufacturer_brief.md",
        ROOT / "showcase" / "critical_minerals_source_audit.md",
        ROOT / "showcase" / "critical_minerals_evidence_pack.json",
        ROOT / "showcase" / "uk_ets_shipping_operator_brief.md",
        ROOT / "showcase" / "uk_ets_source_audit.md",
        ROOT / "showcase" / "uk_ets_evidence_pack.json",
        ROOT / "showcase" / "sanctions_trade_finance_exposure_brief.md",
        ROOT / "showcase" / "sanctions_trade_finance_sample.md",
        ROOT / "showcase" / "sanctions_source_audit.md",
        ROOT / "showcase" / "sanctions_evidence_pack.json",
        ROOT / "showcase" / "cyber_business_interruption_brief.md",
        ROOT / "showcase" / "cyber_source_audit.md",
        ROOT / "showcase" / "cyber_evidence_pack.json",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if re.search(r"sk-[A-Za-z0-9]{10,}", text):
            failures.append(f"{path.name} appears to expose an API key")
        if re.search(r"tvly(?:-dev)?-[A-Za-z0-9]{10,}", text):
            failures.append(f"{path.name} appears to expose a Tavily API key")
        if re.search(r"TAVILY_API_KEY=(?!your_key_here)[^\s]+", text):
            failures.append(f"{path.name} appears to expose a non-placeholder TAVILY_API_KEY")
    return failures


def _read(name):
    return (SHOWCASE / name).read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
