def fetch_selected_sources(selected_sources, fallback_demo_data_used=False):
    fetched = []
    failures = []

    for source in selected_sources:
        if fallback_demo_data_used:
            fetched.append({**source, "content": source.get("claim_supported") or source.get("snippet", ""), "fetch_status": "demo"})
            continue

        try:
            import requests

            response = requests.get(
                source["url"],
                timeout=15,
                headers={"User-Agent": "MarineTradeRiskAgent/0.1 portfolio demo"},
            )
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()
            if _is_pdf(source.get("url", ""), content_type):
                pdf_text, status = _pdf_to_text(response.content)
                content, final_status = _usable_content(pdf_text, source, status)
                fetched.append({**source, "content": content, "fetch_status": final_status})
            else:
                content, status = _usable_content(_html_to_text(response.text), source, "ok")
                fetched.append({**source, "content": content, "fetch_status": status})
        except Exception as exc:
            fetched.append({**source, "content": source.get("snippet", ""), "fetch_status": "failed"})
            failures.append({"url": source.get("url", ""), "error": str(exc)})

    return {"fetched_sources": fetched, "fetch_failures": failures}


def _is_pdf(url, content_type=""):
    return url.lower().split("?", 1)[0].endswith(".pdf") or "application/pdf" in content_type


def _pdf_to_text(content):
    try:
        from io import BytesIO
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(content))
        text = " ".join((page.extract_text() or "") for page in reader.pages)
        text = " ".join(text.split())[:5000]
        return text, "ok" if text else "pdf_metadata_only"
    except Exception:
        return "", "pdf_metadata_only"


def _html_to_text(html):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return _strip_raw_html(html)

    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "form", "aside"]):
        element.decompose()
    for element in soup.select(
        "[class*='cookie'], [id*='cookie'], [class*='banner'], [id*='banner'], "
        "[class*='navigation'], [id*='navigation'], [class*='menu'], [id*='menu'], "
        "[class*='tracking'], [id*='tracking']"
    ):
        element.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return _strip_raw_html(text)


def _strip_raw_html(text):
    import re

    text = re.sub(r"(?is)<(script|style|nav|footer|header|noscript|form|aside)\b.*?</\1>", " ", text or "")
    text = re.sub(r"(?is)<!doctype[^>]*>|<html\b[^>]*>|</html>|<head\b.*?</head>|<[^>]+>", " ", text)
    text = re.sub(r"\b(cookie|cookies|privacy policy|accept all|skip to content|tracking)\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    fragments = [fragment.strip() for fragment in re.split(r"(?<=[.!?])\s+|\s{2,}", text) if len(fragment.strip()) >= 30]
    return " ".join(fragments)[:5000]


def _usable_content(content, source, status):
    cleaned = _strip_raw_html(content)
    if _looks_unusable(cleaned):
        snippet = _strip_raw_html(source.get("snippet", "") or source.get("claim_supported", ""))
        if snippet:
            return snippet, "snippet_used"
    return cleaned, status


def _looks_unusable(text):
    lowered = (text or "").strip().lower()
    if len(lowered) < 30:
        return True
    bad_prefixes = ("<script", "<!doctype", "<html", "data-", "var ", "function ", "cookie")
    return lowered.startswith(bad_prefixes) or any(token in lowered for token in ["<!doctype", "<script", "<html", "window.datalayer"])
