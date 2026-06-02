import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dashboard_helpers import extract_markdown_section, load_markdown  # noqa: E402


SHOWCASE = ROOT / "showcase"
DASHBOARD = ROOT / "dashboard_app.py"

CASES = {
    "UK ETS": {
        "files": [
            SHOWCASE / "uk_ets_shipping_operator_brief.md",
            SHOWCASE / "uk_ets_source_audit.md",
            SHOWCASE / "uk_ets_evidence_pack.json",
        ],
        "brief": SHOWCASE / "uk_ets_shipping_operator_brief.md",
        "sections": [
            "1. Operator Stance",
            "2. Applicability Check",
            "4. Carbon Cost Estimate",
            "7. Evidence-To-Score Bridge",
            "14. Source Requirement Coverage",
        ],
    },
    "Hormuz": {
        "files": [
            SHOWCASE / "hormuz_shipping_operator_brief.md",
            SHOWCASE / "hormuz_source_audit.md",
            SHOWCASE / "hormuz_evidence_pack.json",
        ],
        "brief": SHOWCASE / "hormuz_shipping_operator_brief.md",
        "sections": [
            "Dashboard Summary",
            "1. Decision Recommendation",
            "4. Route Decision Optimiser",
            "5. Illustrative Route-Cost Scenario",
            "11. Source Requirement Coverage",
        ],
    },
    "Critical Minerals": {
        "files": [
            SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
            SHOWCASE / "critical_minerals_source_audit.md",
            SHOWCASE / "critical_minerals_evidence_pack.json",
        ],
        "brief": SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md",
        "sections": [
            "3. Dashboard Summary",
            "1. Decision Recommendation",
            "7. Production Continuity Model",
            "8. Inventory Runway vs Supplier Qualification Gap",
            "13. Source Quality Notes",
        ],
    },
}


def main():
    failures = []

    if not DASHBOARD.exists():
        failures.append("dashboard_app.py is missing")
    else:
        dashboard = DASHBOARD.read_text(encoding="utf-8")
        for forbidden in ["TavilyClient", "live_search_mode", ".env"]:
            if forbidden in dashboard:
                failures.append(f"dashboard_app.py contains forbidden live or secret reference: {forbidden}")

    for case_name, config in CASES.items():
        for path in config["files"]:
            if not path.exists():
                failures.append(f"{case_name} missing saved dashboard file: {path.relative_to(ROOT)}")
        if config["brief"].exists():
            brief = load_markdown(config["brief"])
            for section in config["sections"]:
                if not extract_markdown_section(brief, section):
                    failures.append(f"{case_name} brief missing dashboard section: {section}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)

    print("Dashboard file check passed.")


if __name__ == "__main__":
    main()
