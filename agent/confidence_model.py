def calculate_confidence(sources):
    if not sources:
        return {
            "confidence_score": 2,
            "confidence_rationale": "No source evidence was supplied, so confidence falls back to sparse-input judgment.",
        }

    source_types = [source.get("source_type", source.get("inferred_source_type", "unknown")) for source in sources]
    unique_types = set(source_types)
    unknown_count = source_types.count("unknown")

    score = 1
    reasons = []

    if len(sources) >= 3:
        score += 1
        reasons.append("at least three sources were supplied")
    if len(unique_types) >= 3:
        score += 1
        reasons.append("source types are diverse")
    if "official_primary" in unique_types:
        score += 1
        reasons.append("official primary evidence is present")
    if "company_update" in unique_types:
        score += 1
        reasons.append("company or carrier evidence is present")
    if has_contrary_or_stabilising_evidence(sources):
        reasons.append("contrary or stabilising evidence is present")
    else:
        score -= 1
        reasons.append("no contrary or stabilising evidence was identified")
    if unknown_count >= 2:
        score -= 1
        reasons.append("multiple unknown source types reduce confidence")

    score = max(1, min(5, score))
    rationale = "; ".join(reasons) if reasons else "Confidence reflects limited supplied evidence."

    return {
        "confidence_score": score,
        "confidence_rationale": rationale + ".",
    }


def has_contrary_or_stabilising_evidence(sources):
    stabilising_terms = ["contrary", "stabil", "resume", "normal", "limited", "de-escalat", "improv"]
    return any(
        source.get("source_type") == "contrary_or_stabilising_evidence"
        or any(term in source.get("summary", "").lower() for term in stabilising_terms)
        for source in sources
    )
