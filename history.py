import json
import streamlit as st
from html import escape
from components.ui import header, md, card, h3, html_table, badge, empty_state, pills
from utils import database


def _detail(r):
    p = json.loads(r["payload"] or "{}")
    if not p:
        st.info("No details were stored for this entry.")
        return
    act = r["action"]
    if act == "Verification":
        st.write(f"**{p.get('label')}** – {p.get('score')}% complete. {p.get('explanation', '')}")
        html_table(["Field", "Status", "Details"], [[c["field"], badge(c["status"]), c["detail"]] for c in p.get("checklist", [])], raw_cols=(1,))
        for i in p.get("issues", []):
            md(f'<div class="dc-ins warn"><span>{escape(i)}</span></div>')
    elif act == "Analysis":
        st.write(p.get("summary", ""))
        st.caption("Stats: " + ", ".join(f"{k}: {v}" for k, v in p.get("stats", {}).items()))
        md(pills(p.get("keywords", [])))
        for k, v in p.get("entities", {}).items():
            if v:
                md(f'<div class="dc-muted">{k.title()}</div>{pills(v[:8])}')
    elif act == "Comparison":
        st.write(f"Similarity **{p.get('similarity')}%** – {p.get('changed')} changed, {p.get('added')} added, {p.get('removed')} removed lines.")
    else:
        st.write(p.get("summary", ""))
        for x in p.get("inconsistencies", []):
            md(f'<div class="dc-ins warn"><span>{escape(x)}</span></div>')
        for x in p.get("differences", []):
            md(f'<div class="dc-ins"><span>{escape(x)}</span></div>')


def render():
    header("Document History", "View and manage your previously processed documents.")
    rows = database.list_history()
    if not rows:
        empty_state("No history yet", "Documents you analyze, verify or compare will appear here.", "clock")
        return
    f1, f2, _ = st.columns([1.3, 1.3, 3])
    act = f1.selectbox("Action", ["All", "Analysis", "Verification", "Multi-Document", "Comparison"])
    stat = f2.selectbox("Status", ["All", "Verified", "Needs Attention", "Failed", "Completed"])
    rows = [r for r in rows if (act == "All" or r["action"] == act) and (stat == "All" or r["status"] == stat)]
    with card("hist"):
        if rows:
            html_table(["Document", "Type", "Action", "Status", "Date"],
                       [[r["document"], r["doc_type"], r["action"], badge(r["status"]), r["created"]] for r in rows[:100]], raw_cols=(3,))
        else:
            st.info("No entries match these filters.")
    if rows:
        st.write("")
        with card("hist_view"):
            h3("View previous result")
            opts = {f"#{r['id']} • {r['document']} • {r['action']} • {r['created']}": r for r in rows[:100]}
            sel = st.selectbox("Entry", list(opts), label_visibility="collapsed")
            _detail(opts[sel])
            c1, c2, _ = st.columns([1.2, 1.2, 4])
            if c1.button("Delete entry", key="del_one"):
                database.delete_history(opts[sel]["id"])
                st.rerun()
            if c2.button("Clear all history", key="del_all"):
                database.delete_history()
                st.session_state.logged = set()
                st.rerun()
