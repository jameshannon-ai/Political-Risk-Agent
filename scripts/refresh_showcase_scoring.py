import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent.brief_generator import _evidence_to_score_bridge
from agent.core.scoring import build_traceable_scores
from agent.quantitative_assessment import build_evidence_to_score_bridge
from agent.source_audit import generate_source_audit


SHOWCASE = ROOT / "showcase"

CASES = [
    ("UK ETS", SHOWCASE / "uk_ets_shipping_operator_brief.md", SHOWCASE / "uk_ets_source_audit.md", SHOWCASE / "uk_ets_evidence_pack.json", "7. Evidence-To-Score Bridge"),
    ("Hormuz", SHOWCASE / "hormuz_shipping_operator_brief.md", SHOWCASE / "hormuz_source_audit.md", SHOWCASE / "hormuz_evidence_pack.json", "10. Evidence-To-Score Bridge"),
    ("Critical Minerals", SHOWCASE / "critical_minerals_advanced_manufacturer_brief.md", SHOWCASE / "critical_minerals_source_audit.md", SHOWCASE / "critical_minerals_evidence_pack.json", "11. Evidence-To-Score Bridge"),
    ("Sanctions", SHOWCASE / "sanctions_trade_finance_exposure_brief.md", SHOWCASE / "sanctions_source_audit.md", SHOWCASE / "sanctions_evidence_pack.json", "12. Evidence-To-Score Bridge"),
    ("Cyber", SHOWCASE / "cyber_business_interruption_brief.md", SHOWCASE / "cyber_source_audit.md", SHOWCASE / "cyber_evidence_pack.json", "13. Evidence-To-Score Bridge"),
    ("Fiscal", SHOWCASE / "uk_fiscal_instability_procurement_brief.md", SHOWCASE / "uk_fiscal_instability_procurement_source_audit.md", SHOWCASE / "uk_fiscal_instability_procurement_evidence_pack.json", "Evidence-To-Score Bridge"),
]


def main():
    for label, brief_path, audit_path, pack_path, bridge_heading in CASES:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        risk_scores = _risk_scores_from_pack(pack)
        pack["traceable_scores"] = build_traceable_scores(risk_scores, pack)
        pack["evidence_to_score_bridge"] = build_evidence_to_score_bridge(pack, risk_scores)
        pack["scoring_method_note"] = (
            "Structured analyst score with traceable evidence support; score_type distinguishes evidence-backed, "
            "analyst-assumption and illustrative-fallback scoring."
        )
        pack_path.write_text(json.dumps(pack, indent=2), encoding="utf-8")

        _replace_bridge_section(brief_path, bridge_heading, _evidence_to_score_bridge(pack, risk_scores))
        audit_path.write_text(generate_source_audit(pack), encoding="utf-8")
        print(f"refreshed {label}")


def _risk_scores_from_pack(pack):
    source = pack.get("traceable_scores") or pack.get("evidence_to_score_bridge") or {}
    scores = {}
    for dimension in ["likelihood", "impact", "immediacy", "exposure", "confidence", "decision_urgency"]:
        item = source.get(dimension, {})
        if not item:
            continue
        scores[dimension] = {
            "score": item.get("score", ""),
            "score_type": item.get("score_type")
            if item.get("score_type") in {"evidence_backed", "analyst_assumption", "illustrative_fallback"}
            else "analyst_assumption",
            "rationale": item.get("reason_for_score")
            or item.get("evidence_basis")
            or item.get("basis")
            or "Structured analyst score based on saved source evidence.",
        }
    return scores


def _replace_bridge_section(brief_path, heading, bridge_markdown):
    text = brief_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(^##\s+" + re.escape(heading) + r"\s*$\n)(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    replacement = lambda match: match.group(1) + "\n" + bridge_markdown.strip() + "\n\n"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace {heading} in {brief_path}")
    brief_path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
