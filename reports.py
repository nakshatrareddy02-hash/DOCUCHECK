import streamlit as st
from components.ui import header, md, card, html_table, badge, empty_state, svg
from utils import database


def render():
    header("Generated Reports", "Download your analysis, verification and comparison reports.")
    reps = database.list_reports()
    if not reps:
        empty_state("No reports yet", "Reports are generated automatically when you analyze, verify or compare documents.", "file")
        return
    with card("rep_head"):
        h = st.columns([3.2, 2.4, 1.5, 1.5, 1.6, 1.3])
        for c, t in zip(h, ["Report", "Document", "Type", "Status", "Date", ""]):
            c.markdown(f'<span class="dc-muted"><b>{t}</b></span>', unsafe_allow_html=True)
        for r in reps:
            c = st.columns([3.2, 2.4, 1.5, 1.5, 1.6, 1.3], vertical_alignment="center")
            c[0].markdown(f'<div class="dc-doc"><div class="ico">{svg("file", 18, "#DC2626")}</div><div class="nm">{r["filename"]}</div></div>', unsafe_allow_html=True)
            c[1].caption(r["document"])
            c[2].write(r["report_type"])
            c[3].markdown(badge(r["status"]), unsafe_allow_html=True)
            c[4].caption(r["created"])
            data = database.read_report(r["path"])
            if data:
                c[5].download_button("Download", data, file_name=r["filename"], mime="application/pdf", key=f"dlr_{r['id']}", width="stretch")
            else:
                c[5].caption("File missing")
