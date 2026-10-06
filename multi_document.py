import streamlit as st
from html import escape
from components.state import log_once, save_report_file
from components.ui import header, md, card, h3, doc_html, html_table, badge, pills
from utils.multi_document import analyse_many
from utils.parser import parse_document
from utils import reports

TYPES = ["pdf", "docx", "txt", "jpg", "jpeg", "png"]


def render():
    ss = st.session_state
    header("Multi-Document Analysis", "Upload multiple documents to analyze them together and get combined insights.")
    l, r = st.columns([1, 1])
    with l, card("multi_up"):
        files = st.file_uploader("Add documents", type=TYPES, accept_multiple_files=True, key=f"up_multi_{ss.multi_key}", label_visibility="collapsed")
        md('<div class="dc-muted" style="text-align:center">Supports multiple files (PDF, DOCX, TXT, JPG, PNG)</div>')
        if files:
            with st.spinner("Processing document..."):
                for f in files:
                    d = parse_document(f.name, f.getvalue())
                    if d["error"]:
                        st.error(f"{f.name}: {d['error']}")
                    elif any(x["id"] == d["id"] for x in ss.mdocs):
                        st.info(f"{f.name} was already added.")
                    else:
                        ss.mdocs.append(d)
                        ss.multi_result = None
            ss.multi_key += 1
            st.rerun()
    with r:
        if not ss.mdocs:
            md('<div class="dc-empty" style="padding:2rem 1rem"><b>No documents added yet</b>Add two or more documents to analyze them together.</div>')
        for i, d in enumerate(ss.mdocs):
            with card(f"mdoc_{i}"):
                a, b = st.columns([6, 1], vertical_alignment="center")
                a.markdown(doc_html(d), unsafe_allow_html=True)
                if b.button("✕", key=f"rm_m_{i}", help="Remove"):
                    ss.mdocs.pop(i)
                    ss.multi_result = None
                    st.rerun()
        if st.button("Analyze All", type="primary", width="stretch", key="analyze_all"):
            if len(ss.mdocs) < 2:
                st.warning("Please add at least two documents to run a multi-document analysis.")
            else:
                with st.spinner("Analyzing document..."):
                    ss.multi_result = analyse_many(ss.mdocs)
                m = ss.multi_result
                with st.spinner("Generating report..."):
                    save_report_file(("report", "multi"), "Multi_Document_Report.pdf", f"{len(ss.mdocs)} documents", "Multi-Document",
                                     "Needs Attention" if m["inconsistencies"] else "Completed", reports.multi_report(m))
                st.session_state.logged.discard(("hist", "multi"))
                log_once(("hist", "multi", tuple(d["id"] for d in ss.mdocs)), ", ".join(m["names"])[:80], "Multiple", "Multi-Document",
                         "Needs Attention" if m["inconsistencies"] else "Completed", m["avg_score"],
                         payload={"summary": m["summary"], "differences": m["differences"], "inconsistencies": m["inconsistencies"], "documents": m["names"]})
    m = ss.multi_result
    if not m:
        return
    st.write("")
    with card("multi_sum"):
        h3("Combined Summary")
        st.write(m["summary"])
    with card("multi_ov"):
        h3("Document Overview")
        html_table(list(m["overview"][0].keys()), [list(x.values()) for x in m["overview"]])
    c1, c2 = st.columns(2)
    with c1, card("multi_sim"):
        h3("Similarities")
        html_table(["Documents", "Vocabulary overlap"], [[x["pair"], f"{x['similarity']}%"] for x in m["similarities"]])
        md(f'<div class="dc-muted" style="margin:.8rem 0 .3rem 0">Keywords common to all documents</div>{pills(m["common_keywords"])}')
    with c2, card("multi_ent"):
        h3("Common Entities")
        if m["common_entities"]:
            for k, v in m["common_entities"].items():
                md(f'<div class="dc-muted">{k.title()}</div>{pills(v[:10])}')
        else:
            st.info("No entities are shared by all documents.")
    c3, c4 = st.columns(2)
    with c3, card("multi_diff"):
        h3("Differences")
        for x in m["differences"] or ["No notable differences."]:
            md(f'<div class="dc-ins"><span>{escape(x)}</span></div>')
    with c4, card("multi_inc"):
        h3("Inconsistencies")
        for x in m["inconsistencies"] or ["No inconsistencies detected."]:
            md(f'<div class="dc-ins {"warn" if m["inconsistencies"] else "ok"}"><span>{escape(x)}</span></div>')
    with card("multi_miss"):
        h3("Missing Information")
        for x in m["missing"] or ["Nothing is missing in any document."]:
            md(f'<div class="dc-ins {"warn" if m["missing"] else "ok"}"><span>{escape(x)}</span></div>')
    with card("multi_map"):
        h3("Information Mapping")
        cols = list(m["mapping"][0].keys())
        html_table(cols, [[r[c] if i == 0 else badge(r[c]) for i, c in enumerate(cols)] for r in m["mapping"]], raw_cols=tuple(range(1, len(cols))))
    st.download_button("Download Multi-Document Report", ss.cache[("report", "multi")], file_name="Multi_Document_Report.pdf", mime="application/pdf",
                       type="primary", icon=":material/download:", key="dl_multi")
