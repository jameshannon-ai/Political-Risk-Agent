import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase"


def main():
    checks = [
        _files_exist,
        _framework_guidance,
        _brief_sections,
        _evidence_packs,
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
        "sanctions_trade_finance_sample.md",
        "sanctions_source_audit.md",
        "sanctions_evidence_pack.json",
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
    ]:
        if not path.exists():
            failures.append(f"Missing {path.relative_to(ROOT)}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in ["## Agent / Codex instructions", "AGENTS.md", "docs/FRAMEWORK_PRINCIPLES.md", "docs/TASK_BRIEF_TEMPLATE.md"]:
        if phrase not in readme:
            failures.append(f"README.md missing framework guidance reference: {phrase}")
    return failures


def _brief_sections():
    failures = []
    hormuz = _read("hormuz_shipping_operator_brief.md")
    critical_minerals = _read("critical_minerals_advanced_manufacturer_brief.md")
    uk_ets = _read("uk_ets_shipping_operator_brief.md")
    sanctions = _read("sanctions_trade_finance_sample.md")
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
    for phrase in ["Transaction Stance", "Quantified Evidence Readout", "Evidence-To-Score Bridge", "Payment and Documentation Risk"]:
        if phrase not in sanctions:
            failures.append(f"Sanctions brief missing {phrase}")
    for phrase in ["Operator Stance", "Applicability Check", "Carbon Cost Estimate"]:
        if phrase not in uk_ets:
            failures.append(f"UK ETS brief missing {phrase}")
    for phrase in [
        "Start date: 1 July 2026",
        "Vessel threshold: 5,000 GT",
        "Estimated cost: £2,770 per voyage",
        "Refresh UKA price before pricing or contract decisions.",
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
    return failures


def _evidence_packs():
    failures = []
    for name in ["hormuz_evidence_pack.json", "uk_ets_evidence_pack.json", "sanctions_evidence_pack.json"]:
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


def _source_audits():
    failures = []
    for name in ["hormuz_source_audit.md", "uk_ets_source_audit.md", "sanctions_source_audit.md"]:
        text = _read(name)
        for phrase in ["Research Plan", "Source Requirement Coverage", "Quantified Evidence Summary"]:
            if phrase not in text:
                failures.append(f"{name} missing {phrase}")
    uk_ets_audit = _read("uk_ets_source_audit.md")
    hormuz_audit = _read("hormuz_source_audit.md")
    critical_audit = _read("critical_minerals_source_audit.md")
    for phrase in [
        "Refresh UKA price before pricing or contract decisions.",
        "Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
        "Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
        "Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
        "Review emissions factor methodology with verifier / MRV process.",
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
        'st.sidebar.radio("Cases"',
        "Hormuz Route Decision Engine",
        "Critical Minerals Exposure Engine",
        "saved showcase artefacts only",
        "UK ETS Maritime Expansion: Carbon Cost Exposure",
        "Production continuity gap",
        "substitution feasibility needs stronger magnet-specific engineering",
        "company BOM, supplier ownership/country, inventory, contracts and qualification data are required before operational use",
    ]:
        if phrase not in dashboard:
            failures.append(f"dashboard_app.py does not read the expected showcase file: {phrase}")
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
    for phrase in [".env", ".venv/", ".DS_Store", "*.zip", "outputs/*.md", "outputs/*.json", "!outputs/.gitkeep"]:
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
        except Exception:
            failures.append("Unable to verify whether .env is tracked")
    export_script = (ROOT / "scripts" / "create_clean_project_zip.py").read_text(encoding="utf-8")
    for phrase in [".env", ".venv", ".git", "outputs", "political-risk-agent-clean.zip"]:
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
        ROOT / "showcase" / "sanctions_trade_finance_sample.md",
        ROOT / "showcase" / "sanctions_source_audit.md",
        ROOT / "showcase" / "sanctions_evidence_pack.json",
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
