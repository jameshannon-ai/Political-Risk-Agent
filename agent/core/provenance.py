from datetime import datetime
from hashlib import sha256


FETCH_MODE_BY_STATUS = {
    "ok": "full_text",
    "snippet_used": "snippet_only",
    "failed": "snippet_only",
    "demo": "fallback",
    "pdf_metadata_only": "snippet_only",
}


PDF_STATUSES = {"pdf_text", "pdf_ok"}


def content_hash(text):
    if not text:
        return ""
    return sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def evidence_source_mode(fetch_status, fallback_demo_data_used=False, manual_input=False):
    if manual_input:
        return "manual_input"
    if fallback_demo_data_used:
        return "fallback"
    if fetch_status in PDF_STATUSES:
        return "pdf_text"
    return FETCH_MODE_BY_STATUS.get(fetch_status or "", "full_text")


def source_limitations(fetch_status, mode):
    if mode == "fallback":
        return "Fallback/demo evidence; use for reproducibility only and cap confidence."
    if mode == "manual_input":
        return "Manual analyst input; verify source URL, publisher and date before operational use."
    if mode == "snippet_only":
        return "Snippet-only or failed fetch; verify full source text before relying on the evidence."
    if mode == "pdf_text":
        return "PDF text extraction may omit tables, footnotes or formatting; analyst review required."
    return "Fetched text available; analyst should still verify context and recency."


def enrich_source_provenance(source, fallback_demo_data_used=False, retrieval_timestamp=None):
    retrieval_timestamp = retrieval_timestamp or datetime.now().isoformat(timespec="seconds")
    fetch_status = source.get("fetch_status", "")
    manual_input = source.get("manual_input", False) or source.get("source_mode") == "manual_input"
    mode = source.get("evidence_source_mode") or evidence_source_mode(
        fetch_status,
        fallback_demo_data_used=fallback_demo_data_used,
        manual_input=manual_input,
    )
    content = source.get("content") or source.get("summary") or source.get("snippet") or ""
    enriched = dict(source)
    enriched.setdefault("source_url", source.get("url", ""))
    enriched.setdefault("source_title", source.get("title", ""))
    enriched.setdefault("retrieval_timestamp", retrieval_timestamp)
    enriched.setdefault("evidence_source_mode", mode)
    enriched.setdefault("content_hash", content_hash(content) if content and mode in {"full_text", "pdf_text", "manual_input", "fallback"} else "")
    enriched.setdefault("source_excerpt_character_count", len(content))
    enriched.setdefault("source_limitations", source_limitations(fetch_status, mode))
    enriched.setdefault("why_source_was_selected", source.get("selection_reason", "Selected as the best available source for its requirement."))
    enriched.setdefault(
        "why_source_matters_for_decision",
        source.get("decision_use") or source.get("source_value_explanation") or "Supports the client decision by adding relevant evidence.",
    )
    return enriched


def normalize_evidence_record(evidence, source=None, fallback_demo_data_used=False, retrieval_timestamp=None):
    source = source or {}
    if evidence.get("fetch_status") in {"snippet_used", "failed", "pdf_metadata_only"} or source.get("fetch_status") in {"snippet_used", "failed", "pdf_metadata_only"}:
        source = {**source, "evidence_source_mode": evidence_source_mode(evidence.get("fetch_status") or source.get("fetch_status"), fallback_demo_data_used)}
    merged = enrich_source_provenance(
        {**source, **evidence},
        fallback_demo_data_used=fallback_demo_data_used,
        retrieval_timestamp=retrieval_timestamp,
    )
    if merged.get("fetch_status") in {"snippet_used", "failed", "pdf_metadata_only"}:
        merged["evidence_source_mode"] = evidence_source_mode(merged.get("fetch_status"), fallback_demo_data_used)
        merged["source_limitations"] = source_limitations(merged.get("fetch_status"), merged["evidence_source_mode"])
    source_text = source.get("content") or source.get("snippet") or source.get("summary") or evidence.get("content") or evidence.get("snippet") or ""
    claim = evidence.get("claim_supported") or evidence.get("extracted_claim") or evidence.get("summary", "")
    extracted = evidence.get("extracted_evidence") or evidence.get("supporting_detail") or _distinct_extracted_evidence(claim, source_text)
    caveat = evidence.get("caveat") or merged.get("source_limitations", "")
    mode = merged.get("evidence_source_mode", "")
    inference_strength = evidence.get("inference_strength") or _inference_strength(mode, evidence.get("source_type", ""))
    extraction_confidence = evidence.get("extraction_confidence") or _extraction_confidence(mode, claim)
    quoted_excerpt = evidence.get("quoted_excerpt_used") or _source_grounded_excerpt(source_text, claim)

    merged.update(
        {
            "source_claim": evidence.get("source_claim") or claim,
            "extracted_evidence": extracted,
            "analyst_inference": evidence.get("analyst_inference") or evidence.get("commercial_meaning") or evidence.get("decision_use", ""),
            "inference_strength": inference_strength,
            "caveat": caveat,
            "evidence_type": evidence.get("evidence_type") or _evidence_type(evidence.get("source_type", ""), evidence.get("source_role", "")),
            "quoted_excerpt_used": quoted_excerpt,
            "extraction_confidence": extraction_confidence,
            "requires_human_review": evidence.get("requires_human_review", _requires_human_review(mode, inference_strength)),
            "source_url": evidence.get("source_url") or evidence.get("url", ""),
            "source_title": evidence.get("source_title") or evidence.get("title", ""),
        }
    )
    return merged


def _short_excerpt(text):
    text = " ".join(str(text or "").split())
    return text[:240]


def _distinct_extracted_evidence(claim, source_text):
    source_text = " ".join(str(source_text or "").split())
    claim = " ".join(str(claim or "").split())
    if source_text:
        excerpt = _source_grounded_excerpt(source_text, claim)
        if excerpt and excerpt.lower() != claim.lower():
            return excerpt
    if claim:
        return "Source-grounded detail requires human verification beyond the claim summary."
    return ""


def _source_grounded_excerpt(source_text, claim=""):
    source_text = " ".join(str(source_text or "").split())
    if not source_text:
        return _short_excerpt(claim)
    sentences = [item.strip() for item in source_text.replace("?", ".").replace("!", ".").split(".") if len(item.strip()) > 30]
    claim_terms = {
        term.lower().strip(",:;()[]")
        for term in str(claim or "").split()
        if len(term.strip(",:;()[]")) > 5
    }
    best = ""
    best_score = -1
    for sentence in sentences[:60]:
        lowered = sentence.lower()
        if _looks_like_boilerplate(lowered):
            continue
        score = sum(1 for term in claim_terms if term in lowered)
        if score > best_score:
            best = sentence
            best_score = score
    return _short_excerpt(best or source_text)


def _looks_like_boilerplate(text):
    return any(
        fragment in text
        for fragment in [
            "cookie",
            "privacy policy",
            "accept recommended",
            "skip to main content",
            "javascript enabled",
            "download now",
        ]
    )


def _inference_strength(mode, source_type):
    if mode in {"snippet_only", "fallback", "manual_input"}:
        return "weak" if mode == "snippet_only" else "moderate"
    if source_type in {"official_primary", "official_anchor", "regulatory_guidance"}:
        return "direct"
    return "moderate"


def _extraction_confidence(mode, claim):
    if not claim:
        return "low"
    if mode == "snippet_only":
        return "low"
    if mode in {"fallback", "manual_input", "pdf_text"}:
        return "medium"
    return "high"


def _requires_human_review(mode, inference_strength):
    return mode in {"snippet_only", "fallback", "manual_input"} or inference_strength == "weak"


def _evidence_type(source_type, source_role):
    text = " ".join([source_type or "", source_role or ""]).lower()
    if "official" in text:
        return "official_statement"
    if "regulatory" in text or "guidance" in text:
        return "regulation"
    if "market" in text or "pricing" in text or "insurance" in text:
        return "market_data"
    if "specialist" in text or "analysis" in text:
        return "expert_analysis"
    if "news" in text or "reporting" in text:
        return "news_reporting"
    if "company" in text or "operator" in text:
        return "company_disclosure"
    return "other"
