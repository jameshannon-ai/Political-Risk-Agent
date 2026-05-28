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
