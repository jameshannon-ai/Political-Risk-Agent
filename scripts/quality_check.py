import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHOWCASE = ROOT / "showcase"


def main():
    checks = [
        _files_exist,
        _brief_sections,
        _evidence_packs,
        _dashboard_checks,
        _source_audits,
        _confidence_caps,
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
    for path in [ROOT / "README.md", ROOT / "dashboard_app.py"]:
        if not path.exists():
            failures.append(f"Missing {path.name}")
    for name in [
        "hormuz_shipping_operator_brief.md",
        "hormuz_source_audit.md",
        "hormuz_evidence_pack.json",
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


def _brief_sections():
    failures = []
    hormuz = _read("hormuz_shipping_operator_brief.md")
    uk_ets = _read("uk_ets_shipping_operator_brief.md")
    sanctions = _read("sanctions_trade_finance_sample.md")
    for phrase in ["Operator Decision Stance", "Voyage Decision Matrix", "Sanctions and Safe-Passage Risk", "Dynamic Route-Cost Assessment"]:
        if phrase not in hormuz:
            failures.append(f"Hormuz brief missing {phrase}")
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
    return failures


def _source_audits():
    failures = []
    for name in ["hormuz_source_audit.md", "uk_ets_source_audit.md", "sanctions_source_audit.md"]:
        text = _read(name)
        for phrase in ["Research Plan", "Source Requirement Coverage", "Quantified Evidence Summary"]:
            if phrase not in text:
                failures.append(f"{name} missing {phrase}")
    uk_ets_audit = _read("uk_ets_source_audit.md")
    for phrase in [
        "Refresh UKA price before pricing or contract decisions.",
        "Refresh UK ETS Authority guidance if maritime scope, reporting or surrender deadlines change.",
        "Validate operator-specific fuel burn and route classification before using the cost estimate commercially.",
        "Refresh future-scope assumptions if UK-international maritime expansion policy changes.",
        "Review emissions factor methodology with verifier / MRV process.",
    ]:
        if phrase not in uk_ets_audit:
            failures.append(f"UK ETS audit missing refresh priority: {phrase}")
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
    for phrase in [
        'SHOWCASE / "uk_ets_evidence_pack.json"',
        'SHOWCASE / "uk_ets_shipping_operator_brief.md"',
        'SHOWCASE / "uk_ets_source_audit.md"',
    ]:
        if phrase not in dashboard:
            failures.append(f"dashboard_app.py does not read the expected showcase file: {phrase}")
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
