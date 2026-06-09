from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.core.provenance import normalize_evidence_record


DEFAULT_OUTPUT_DIR = Path("outputs/backfilled_evidence")


def backfill_evidence_pack(pack_path: Path, output_dir: Path = DEFAULT_OUTPUT_DIR, overwrite: bool = False) -> dict:
    pack_path = Path(pack_path)
    output_dir = Path(output_dir)
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    selected_by_id = {
        source.get("source_id"): source
        for source in pack.get("selected_sources", [])
        if source.get("source_id")
    }

    enriched_rows = []
    report_rows = []
    for row in pack.get("evidence", []):
        source = selected_by_id.get(row.get("source_id"), {})
        enriched = normalize_evidence_record(
            row,
            source={**source, **_stored_source_material(row, source)},
            fallback_demo_data_used=pack.get("fallback_demo_data_used", False),
            retrieval_timestamp=pack.get("retrieval_timestamp"),
        )
        enriched_rows.append(enriched)
        report_rows.append(_report_row(row, enriched))

    enriched_pack = dict(pack)
    enriched_pack["evidence"] = enriched_rows
    enriched_pack["backfill_report"] = {
        "source_pack": str(pack_path),
        "live_retrieval_used": False,
        "rows_total": len(enriched_rows),
        "rows_requiring_human_review": sum(1 for row in enriched_rows if row.get("requires_human_review")),
        "rows_snippet_only": sum(1 for row in enriched_rows if row.get("evidence_source_mode") == "snippet_only"),
        "rows_enriched_from_stored_material": sum(1 for row in report_rows if row["status"] == "enriched_from_stored_material"),
        "rows_limited": sum(1 for row in report_rows if row["status"] != "enriched_from_stored_material"),
        "rows": report_rows,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = pack_path if overwrite else output_dir / f"{pack_path.stem}-backfilled.json"
    output_path.write_text(json.dumps(enriched_pack, indent=2, ensure_ascii=False), encoding="utf-8")
    report_path = output_dir / f"{pack_path.stem}-backfill-report.md"
    report_path.write_text(_markdown_report(enriched_pack["backfill_report"]), encoding="utf-8")
    return {"pack_path": output_path, "report_path": report_path, "pack": enriched_pack}


def _stored_source_material(row: dict, source: dict) -> dict:
    content = row.get("content") or source.get("content") or ""
    snippet = row.get("snippet") or source.get("snippet") or row.get("summary") or source.get("summary") or ""
    if content:
        return {"content": content}
    if snippet:
        return {"content": snippet, "snippet": snippet, "fetch_status": row.get("fetch_status") or source.get("fetch_status") or "snippet_used"}
    return {"fetch_status": row.get("fetch_status") or source.get("fetch_status") or "snippet_used"}


def _report_row(before: dict, after: dict) -> dict:
    has_material = bool(before.get("content") or before.get("snippet") or after.get("quoted_excerpt_used"))
    limited = after.get("requires_human_review") or after.get("evidence_source_mode") in {"snippet_only", "fallback", "manual_input"}
    return {
        "source_id": after.get("source_id", ""),
        "mode": after.get("evidence_source_mode", ""),
        "status": "limited_requires_review" if limited else "enriched_from_stored_material" if has_material else "insufficient_stored_material",
        "requires_human_review": bool(after.get("requires_human_review")),
        "extraction_confidence": after.get("extraction_confidence", ""),
        "limitation": after.get("source_limitations", ""),
    }


def _markdown_report(report: dict) -> str:
    rows = [
        "# Evidence Backfill Report",
        "",
        f"- Source pack: {report['source_pack']}",
        "- Live retrieval used: false",
        f"- Rows total: {report['rows_total']}",
        f"- Rows enriched from stored material: {report['rows_enriched_from_stored_material']}",
        f"- Rows limited: {report['rows_limited']}",
        f"- Rows requiring human review: {report['rows_requiring_human_review']}",
        f"- Rows snippet-only: {report['rows_snippet_only']}",
        "",
        "| Source ID | Mode | Status | Human review | Extraction confidence | Limitation |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        rows.append(
            "| {source_id} | {mode} | {status} | {review} | {confidence} | {limit} |".format(
                source_id=row["source_id"],
                mode=row["mode"],
                status=row["status"],
                review=str(row["requires_human_review"]).lower(),
                confidence=row["extraction_confidence"],
                limit=str(row["limitation"]).replace("|", "\\|"),
            )
        )
    return "\n".join(rows) + "\n"


def _parse_args():
    parser = argparse.ArgumentParser(description="Backfill evidence extraction from stored pack material only.")
    parser.add_argument("pack_path", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the input pack instead of writing to outputs/backfilled_evidence.")
    return parser.parse_args()


def main():
    args = _parse_args()
    result = backfill_evidence_pack(args.pack_path, args.output_dir, overwrite=args.overwrite)
    print(result["pack_path"])
    print(result["report_path"])


if __name__ == "__main__":
    main()
