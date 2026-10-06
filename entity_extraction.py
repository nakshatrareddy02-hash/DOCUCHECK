"""Rule-based entity extraction. Pattern matching only: results are best-effort, not perfect."""
from __future__ import annotations
import re

EMAIL_RE = r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
PHONE_RE = r"(?<![\w/])(?:\+?\d{1,3}[\s\-.]?)?(?:\(\d{2,4}\)[\s\-.]?)?\d{3,5}[\s\-.]?\d{3,5}(?:[\s\-.]?\d{2,4})?(?![\w/])"
URL_RE = r"(?:https?://|www\.)[^\s)>\]]+|(?:linkedin\.com|github\.com)/[^\s)>\]]+"

SKILL_LIST = sorted("""python java javascript typescript c++ c# sql mysql postgresql mongodb html css react angular vue node.js django flask
fastapi streamlit pandas numpy matplotlib scikit-learn tensorflow pytorch keras tableau excel git github docker kubernetes aws azure gcp
linux bash php ruby rust kotlin swift flutter figma photoshop scrum jira selenium devops opencv matlab hadoop spark firebase graphql
tailwind bootstrap""".split() + ["machine learning", "deep learning", "nlp", "data analysis", "data science", "data visualization",
    "power bi", "rest api", "spring boot", "project management", "agile", "problem solving", "communication", "leadership",
    "teamwork", "computer vision", "statistics", "ci/cd"], key=lambda s: (-len(s), s))
UPPER = {"sql", "css", "html", "aws", "gcp", "nlp", "php", "api", "ci/cd"}
KEEP = {"node.js", "scikit-learn", "c++", "c#"}

QUAL_RE = (r"\b(?:B\.?\s?Tech|M\.?\s?Tech|B\.?E\.?|M\.?E\.?|B\.?Sc\.?|M\.?Sc\.?|B\.?Com\.?|M\.?Com\.?|B\.?A\.?|M\.?A\.?|BCA|MCA|MBA|BBA|"
           r"Ph\.?D\.?|Diploma|Bachelor(?:'s)?(?: of [A-Z][a-z]+(?: [A-Za-z]+)?)?|Master(?:'s)?(?: of [A-Z][a-z]+(?: [A-Za-z]+)?)?|"
           r"High School|Secondary School|Intermediate|SSC|HSC|CBSE|Associate Degree)\b")
ORG_RE = (r"\b(?:[A-Z][A-Za-z&]+\s){1,4}(?:Inc\.?|Ltd\.?|LLC|LLP|Corp(?:oration)?\.?|Company|Technologies|Technology|Solutions|Systems|"
          r"University|College|Institute|School|Academy|Bank|Foundation|Labs|Group|Consulting|Services|Pvt\.?)\b(?:\s(?:Ltd\.?|Limited|Pvt\.?))?")
LOCATIONS = """Hyderabad Bangalore Bengaluru Chennai Mumbai Delhi New Delhi Pune Kolkata Ahmedabad Jaipur Noida Gurgaon Gurugram Kochi
Visakhapatnam Telangana Karnataka Maharashtra Tamil Nadu Andhra Pradesh Kerala India London Manchester Birmingham Paris Berlin Munich
Madrid Rome Amsterdam Dublin Zurich Dubai Singapore Tokyo Beijing Shanghai Sydney Melbourne Toronto Vancouver New York San Francisco
Los Angeles Chicago Boston Seattle Austin Houston Dallas Atlanta Washington California Texas Florida Canada Australia Germany France
Spain Italy Japan China USA United States United Kingdom UK UAE""".split()
LOC_MULTI = ["New Delhi", "Tamil Nadu", "Andhra Pradesh", "New York", "San Francisco", "Los Angeles", "United States", "United Kingdom"]
NOT_NAMES = set("""Resume Curriculum Vitae Education Experience Skills Projects Summary Objective Profile Contact References Declaration
Certificate Application Report Page Date Name Email Phone Address Mobile Dear Sir Madam The This That Computer Science Engineering
Technical Software Developer Engineer Intern Manager University College Institute School Bachelor Master Data Analysis Machine Learning
Project Management Work History Personal Details Achievements Awards Certifications Languages Interests Introduction Conclusion
Abstract Table Contents Version Document Confidential Form Signature Place Year""".split())

NAME_RE = r"[A-Z][a-z]{1,}(?:\s[A-Z]\.)?(?:\s[A-Z][a-z]{1,}){0,2}"


def _uniq(items):
    seen, out = set(), []
    for i in items:
        k = i.strip().lower()
        if k and k not in seen:
            seen.add(k)
            out.append(i.strip())
    return out


def find_phones(text):
    out = []
    for m in re.finditer(PHONE_RE, text):
        s = m.group().strip()
        digits = re.sub(r"\D", "", s)
        if 10 <= len(digits) <= 13 and not re.fullmatch(r"(?:19|20)\d{2}\D*(?:19|20)\d{2}", s):
            out.append(s)
    return _uniq(out)


def find_persons(text):
    labeled, titled, cue, first_line = [], [], [], []
    for m in re.finditer(rf"(?im)^\s*(?:full\s+)?name\s*[:\-]\s*({NAME_RE})", text):
        labeled.append(m.group(1))
    for m in re.finditer(rf"\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Shri|Smt)\.?\s+({NAME_RE})", text):
        titled.append(m.group(1))
    for m in re.finditer(rf"(?i:certify that|presented to|awarded to|issued to|submitted by|prepared by|signed by|applicant)\s*[:\-]?\s*({NAME_RE})", text):
        cue.append(m.group(1))
    for l in [l.strip() for l in text.splitlines() if l.strip()][:3]:
        cl = re.sub(r"[^A-Za-z.\s]", "", l).strip()
        cand = cl.title() if cl.isupper() else cl
        if re.fullmatch(NAME_RE, cand) and 2 <= len(cand.split()) <= 4 and "@" not in l \
                and not any(w.capitalize() in NOT_NAMES for w in cand.split()):
            first_line.append(cand)
            break
    people = labeled + first_line + cue + titled
    return _uniq(p for p in people if not any(w in NOT_NAMES for w in p.split()))[:8]


def find_locations(text):
    found = []
    for loc in sorted(set(LOCATIONS) | set(LOC_MULTI), key=lambda x: -len(x)):
        if re.search(rf"\b{re.escape(loc)}\b", text):
            found.append(loc)
    # drop parts of longer matches (e.g. "York" inside "New York")
    return [l for l in found if not any(l != o and l in o for o in found)]


def find_skills(text):
    low = text.lower()
    out = []
    for sk in SKILL_LIST:
        if re.search(rf"(?<![\w+#]){re.escape(sk)}(?![\w+#])", low):
            out.append(sk.upper() if sk in UPPER else sk if sk in KEEP else sk.title())
    return out


def extract_entities(text: str, sections=None) -> dict:
    from utils.text_analysis import DATE_RE
    emails = _uniq(re.findall(EMAIL_RE, text))
    phones = find_phones(text)
    urls = _uniq(u.rstrip(".,;") for u in re.findall(URL_RE, text) if "@" not in u)
    dates = _uniq(m.group() for m in re.finditer(DATE_RE, text))
    orgs = _uniq(m.group().strip() for m in re.finditer(ORG_RE, text))
    quals = _uniq(m.group().strip() for m in re.finditer(QUAL_RE, text))
    return {"persons": find_persons(text), "locations": find_locations(text), "dates": dates, "organizations": orgs,
            "emails": emails, "phones": phones, "urls": urls, "qualifications": quals, "skills": find_skills(text)}
