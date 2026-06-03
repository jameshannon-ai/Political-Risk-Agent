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
                "URL": source.get("url", ""),
            }
        )
    return rows


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
