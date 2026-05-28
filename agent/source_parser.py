def parse_source_notes(source_notes):
    """Parse semi-structured pasted source notes into normalized dictionaries."""
    blocks = _split_source_blocks(source_notes)
    return [_parse_source_block(index + 1, block) for index, block in enumerate(blocks)]


def infer_source_type(publisher="", raw_type="", summary=""):
    text = " ".join([publisher, raw_type, summary]).lower()

    if any(term in text for term in ["ukmto", "government", "official", "navy", "maritime advisory", "security advisory"]):
        return "official_primary"
    if any(term in text for term in ["maersk", "msc", "cma cgm", "hapag", "carrier", "company update"]):
        return "company_update"
    if any(term in text for term in ["freight", "index", "premium", "insurance", "market indicator", "rate"]):
        return "market_indicator"
    if any(term in text for term in ["reuters", "ap", "financial times", "bbc", "news"]):
        return "reputable_news"
    if any(term in text for term in ["analysis", "think tank", "risk consultancy", "specialist", "analyst"]):
        return "specialist_analysis"
    return "unknown"


def _split_source_blocks(source_notes):
    blocks = []
    current = []

    for line in source_notes.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("source ") and current:
            blocks.append("\n".join(current).strip())
            current = [line]
        elif stripped:
            current.append(line)

    if current:
        blocks.append("\n".join(current).strip())

    return blocks


def _parse_source_block(source_number, block):
    fields = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()

    publisher = fields.get("publisher", "Unknown")
    raw_type = fields.get("type", "unknown")
    summary = fields.get("summary", "")

    return {
        "source_id": fields.get("source", f"S{source_number}") if fields.get("source", "").startswith("S") else f"S{source_number}",
        "publisher": publisher,
        "date": fields.get("date", ""),
        "raw_type": raw_type,
        "inferred_source_type": infer_source_type(publisher, raw_type, summary),
        "summary": summary,
    }
