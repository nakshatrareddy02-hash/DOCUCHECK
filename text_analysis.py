"""Statistics, keywords, sections, document type, summary and insights (local, no AI needed)."""
from __future__ import annotations
import re
from collections import Counter

STOP = set("""a about above after again all also am an and any are as at be because been before being below between both but by
can could did do does doing down during each few for from further had has have having he her here hers him his how i if in into is
it its just me more most my no nor not now of off on once only or other our out over own same she should so some such than that the
their them then there these they this those through to too under until up very was we were what when where which while who whom why
will with would you your yours etc using use used per via able new""".split())

SECTION_WORDS = {"education", "experience", "work experience", "skills", "projects", "summary", "objective", "profile",
                 "certifications", "certificates", "references", "achievements", "awards", "contact", "introduction",
                 "conclusion", "abstract", "methodology", "results", "findings", "recommendations", "background",
                 "personal details", "declaration", "technical skills", "professional experience", "interests",
                 "languages", "publications", "employment history", "academic background", "overview", "scope"}

DOC_TYPES = {
    "Resume": ["resume", "curriculum vitae", "objective", "education", "skills", "experience", "projects", "references", "linkedin"],
    "Certificate": ["certificate", "certify", "certified", "awarded", "completion", "successfully completed", "this is to certify", "presented to"],
    "Application": ["application", "applicant", "apply", "applying", "signature", "declaration", "form", "date of birth", "father's name"],
    "Report": ["report", "findings", "conclusion", "abstract", "methodology", "analysis", "results", "recommendations", "introduction"],
}


def words_of(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'\-+#.]*[A-Za-z+#]|[A-Za-z]", text)


def detect_language(text: str) -> str:
    toks = [w.lower() for w in re.findall(r"[^\W\d_]+", text)][:3000]
    if not toks:
        return "Unknown"
    markers = {
        "English": {"the", "and", "of", "to", "in", "is", "for", "with", "that"},
        "Spanish": {"el", "la", "de", "que", "y", "en", "los", "para", "con"},
        "French": {"le", "la", "les", "des", "et", "est", "pour", "dans", "une"},
        "German": {"der", "die", "und", "das", "ist", "mit", "nicht", "von", "für"},
    }
    scores = {k: sum(1 for t in toks if t in v) for k, v in markers.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] >= max(3, len(toks) * 0.02) else "Unknown"


def is_heading(line: str, hints: set[str]) -> bool:
    s = line.strip()
    if not s or len(s) > 60 or "@" in s or re.search(r"https?://", s):
        return False
    if s in hints:
        return True
    low = s.lower().rstrip(":").strip()
    if low in SECTION_WORDS:
        return True
    if s.startswith("#"):
        return True
    letters = [c for c in s if c.isalpha()]
    if len(letters) >= 4 and s.isupper() and len(s.split()) <= 6:
        return True
    return s.endswith(":") and len(s.split()) <= 5


def split_sections(text: str, hints: set[str] | None = None) -> list[dict]:
    hints = hints or set()
    sections, cur = [], {"title": "Introduction", "lines": []}
    for ln in text.splitlines():
        if is_heading(ln, hints):
            if cur["lines"] or cur["title"] != "Introduction":
                sections.append(cur)
            cur = {"title": ln.strip().lstrip("#").strip().rstrip(":"), "lines": []}
        elif ln.strip():
            cur["lines"].append(ln.strip())
    if cur["lines"] or not sections:
        sections.append(cur)
    return [s for s in sections if s["lines"] or s["title"] != "Introduction"]


def keywords(text: str, n: int = 10) -> list[str]:
    toks = [w.lower() for w in words_of(text) if len(w) > 2]
    toks = [w for w in toks if w not in STOP and not w.isdigit()]
    return [w for w, _ in Counter(toks).most_common(n)]


def classify(text: str, name: str = "") -> str:
    low = (text[:6000] + " " + name).lower()
    scores = {k: sum(low.count(w) for w in v) for k, v in DOC_TYPES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] >= 3 else "Other"


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", flat) if len(s.split()) >= 4]


def local_summary(text: str, doc_type: str, kw: list[str], max_sent: int = 4) -> str:
    sents = sentences(text)
    if len(sents) < 2:
        lines = [l.strip() for l in text.splitlines() if len(l.split()) >= 3][:5]
        base = " ".join(lines)[:600]
        return f"This looks like a {doc_type.lower()} document. Key content: {base}" if base else "Not enough text to summarise."
    freq = Counter(kw_ for kw_ in [w.lower() for w in words_of(text) if w.lower() not in STOP])
    scored = []
    for i, s in enumerate(sents):
        ws = [w.lower() for w in words_of(s)]
        sc = sum(freq[w] for w in ws) / (len(ws) ** 0.7 + 1)
        scored.append((sc + (1.5 if i < 2 else 0), i, s))
    top = sorted(sorted(scored, reverse=True)[:max_sent], key=lambda x: x[1])
    return " ".join(s for _, _, s in top)


def analyse_text(doc: dict) -> dict:
    """Core numbers + structure for one parsed document."""
    from utils.entity_extraction import extract_entities
    text = doc["text"]
    hints = set(doc.get("headings", []))
    lines = [l for l in text.splitlines() if l.strip()]
    heads = [l.strip() for l in lines if is_heading(l, hints)]
    head_set = set(heads)
    bullets = [l for l in lines if re.match(r"^\s*([•\-\*▪●◦·]|\d+[.)])\s+", l)]
    n_words = len(words_of(text))
    head_words = sum(len(words_of(h)) for h in heads)
    list_words = sum(len(words_of(b)) for b in bullets if b.strip() not in head_set)
    body_words = max(n_words - head_words - list_words, 0)
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()] or lines
    sections = split_sections(text, hints)
    kw = keywords(text, 10)
    dtype = classify(text, doc["name"])
    ents = extract_entities(text, sections)
    sents = sentences(text)
    return {
        "doc_type": dtype, "pages": doc["pages"], "words": n_words, "characters": len(text),
        "paragraphs": len(paragraphs), "lines": len(lines), "sentences": len(sents),
        "headings": heads, "sections": sections, "images": doc["images"], "language": detect_language(text),
        "keywords": kw, "entities": ents, "head_words": head_words, "list_words": list_words, "body_words": body_words,
        "avg_sentence": round(n_words / max(len(sents), 1), 1),
        "summary": local_summary(text, dtype, kw),
    }


def timeline(text: str, dates: list[str]) -> list[dict]:
    """Dates with the line they were found on, sorted by year when possible."""
    rows = []
    for ln in text.splitlines():
        for d in re.finditer(DATE_RE, ln):
            ys = re.findall(r"(?:19|20)\d{2}", d.group())
            rows.append({"date": d.group().strip(), "context": ln.strip()[:140], "year": int(ys[0]) if ys else 0})
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: (r["year"] == 0, r["year"])):
        k = (r["date"], r["context"])
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


MONTHS = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
DATE_RE = (rf"\b(?:(?:19|20)\d{{2}}\s*[-–—to]+\s*(?:(?:19|20)\d{{2}}|Present|Current|Now)|\d{{1,2}}[/\-.]\d{{1,2}}[/\-.]\d{{2,4}}|\d{{4}}[/\-]\d{{1,2}}[/\-]\d{{1,2}}|"
           rf"\d{{1,2}}(?:st|nd|rd|th)?\s+{MONTHS}\.?,?\s+\d{{4}}|{MONTHS}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}}|"
           rf"{MONTHS}\.?\s+\d{{4}})\b")


def insights(a: dict, doc: dict) -> list[dict]:
    """Insights derived from the actual analysis. Each: {level, title, text}."""
    out, e = [], a["entities"]
    out.append({"level": "info", "title": "Document type",
                "text": f"Looks like a {a['doc_type'].lower()} ({a['words']} words, {a['pages']} page(s), language: {a['language']})."})
    if a["avg_sentence"] > 28:
        out.append({"level": "warn", "title": "Long sentences", "text": f"Average sentence length is {a['avg_sentence']} words, which can hurt readability."})
    elif a["sentences"]:
        out.append({"level": "ok", "title": "Readable length", "text": f"Average sentence length is {a['avg_sentence']} words."})
    if a["doc_type"] == "Resume":
        miss = [k for k, lab in (("emails", "email"), ("phones", "phone number"), ("skills", "skills")) if not e[k]]
        out.append({"level": "warn" if miss else "ok", "title": "Contact & skills",
                    "text": ("Missing: " + ", ".join(m.replace('emails', 'email').replace('phones', 'phone') for m in miss) + ".") if miss
                    else "Email, phone and skills were all detected."})
    if len(set(e["emails"])) > 1:
        out.append({"level": "warn", "title": "Multiple emails", "text": f"{len(set(e['emails']))} different email addresses appear in this document."})
    if not a["headings"]:
        out.append({"level": "warn", "title": "No clear sections", "text": "No headings were detected; structuring the document with headings makes it easier to process."})
    else:
        out.append({"level": "ok", "title": "Structured", "text": f"{len(a['headings'])} headings / {len(a['sections'])} sections detected."})
    if a["words"] < 80:
        out.append({"level": "warn", "title": "Very short document", "text": "The document has little text, so results may be limited."})
    if doc.get("ocr"):
        out.append({"level": "warn", "title": "OCR used", "text": "Text came from OCR, so recognition errors are possible."})
    if a["keywords"]:
        out.append({"level": "info", "title": "Top keywords", "text": ", ".join(a["keywords"][:6])})
    return out
