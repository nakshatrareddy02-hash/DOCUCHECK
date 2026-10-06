"""Session-state helpers, navigation and shared pipelines."""
from __future__ import annotations
import streamlit as st
from utils import ai, database, reports
from utils.text_analysis import analyse_text, timeline, insights
from utils.verification import verify


def init():
    defaults = {"page": "home", "doc": None, "store": {}, "upload_key": 0, "custom_rules": [], "cache": {}, "logged": set(),
                "mdocs": [], "multi_key": 0, "multi_result": None, "cmp_a": None, "cmp_b": None, "cmp_result": None, "cmp_key": 0,
                "chat": {}, "pending_q": None}
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def go(page: str):
    st.session_state.page = page


def reset_doc():
    st.session_state.doc = None
    st.session_state.upload_key += 1


def need_doc() -> dict | None:
    """Return the active document or render a friendly empty state."""
    doc = st.session_state.doc
    if doc:
        return doc
    from components.ui import empty_state
    empty_state("No document uploaded yet", "Please upload a document to continue.", "upload")
    st.write("")
    st.button("Go to Upload", type="primary", on_click=go, args=("upload",), key=f"goup_{st.session_state.page}")
    return None


def log_once(key, document, doc_type, action, status, score=None, payload=None):
    if key in st.session_state.logged:
        return
    st.session_state.logged.add(key)
    try:
        database.add_history(document, doc_type, action, status, score, payload)
    except Exception as exc:
        st.toast(f"Could not save history: {exc}")


def save_report_file(key, filename, document, rtype, status, data: bytes):
    st.session_state.cache[key] = data
    try:
        database.save_report(filename, document, rtype, status, data)
    except Exception as exc:
        st.toast(f"Could not save report: {exc}")


def get_analysis(doc: dict) -> dict:
    ck = ("analysis", doc["id"])
    c = st.session_state.cache
    if ck not in c:
        with st.spinner("Analyzing document..."):
            a = analyse_text(doc)
            ai_sum = None
            if ai.available():
                ai_sum = ai.ai_summary(doc["text"])
            tl = timeline(doc["text"], a["entities"]["dates"])
            c[ck] = {"a": a, "ai_summary": ai_sum, "timeline": tl, "insights": insights(a, doc)}
    return c[ck]


def rules_sig() -> str:
    return "|".join(f"{r['field']}:{','.join(r['keywords'])}" for r in st.session_state.custom_rules)


def get_verification(doc: dict) -> dict:
    ck = ("verify", doc["id"], rules_sig())
    c = st.session_state.cache
    if ck not in c:
        a = get_analysis(doc)["a"]
        c[ck] = verify(doc, a, st.session_state.custom_rules or None)
    return c[ck]
