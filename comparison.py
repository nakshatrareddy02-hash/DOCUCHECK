import streamlit as st
from html import escape
from components.state import log_once, save_report_file
from components.ui import header, md, card, h3, html_table, badge, pills, svg, donut
from utils.comparison import compare
from utils.parser import parse_document
from utils import reports

TYPES = ["pdf", "docx", "txt", "jpg", "jpeg", "png"]
CASES = [("Resume Versions", "Compare resume updates"), ("Certificates", "Check certificate changes"),
         ("Reports", "Track document revisions"), ("Applications", "Compare application drafts")]


def _slot(which: str, title: str):
    ss = st.session_state
    with card(f"cmp_{which}"):
        md(f'<div class="dc-h3" style="text-align:center">{title}</div>')
        f = st.file_uploader(f"Upload {title}", type=TYPES, key=f"up_small_{which}_{ss.cmp_key}", label_visibility="collapsed")
        if f is not None:
            with st.spinner("Processing document..."):
                d = parse_document(f.name, f.getvalue())
            if d["error"]:
                st.error(d["error"])
                ss[f"cmp_{which}"] = None
            else:
                ss[f"cmp_{which}"] = d
        d = ss[f"cmp_{which}"]
        if d:
            md(f'<div class="dc-muted" style="text-align:center">{escape(d["name"])} • {d["size_label"]} • {d["pages"]} page(s)</div>')


def render():
    ss = st.session_state
    header("Compare Documents", "Upload two documents to see the differences and similarities.")
    a, v, b = st.columns([5, 1, 5])
    with a:
        _slot("a", "Document A")
    v.markdown('<div class="dc-vs">VS</div>', unsafe_allow_html=True)
    with b:
        _slot("b", "Document B")
    st.write("")
    _, mid, _ = st.columns([2, 1.3, 2])
    if mid.button("Compare", type="primary", width="stretch", key="do_compare"):
        if not ss.cmp_a or not ss.cmp_b:
            st.warning("Please upload both Document A and Document B before comparing.")
        else:
            with st.spinner("Comparing documents..."):
                ss.cmp_result = compare(ss.cmp_a, ss.cmp_b)
            c = ss.cmp_result
            with st.spinner("Generating report..."):
                save_report_file(("report", "cmp"), "Comparison_Report.pdf", f"{c['names'][0]} vs {c['names'][1]}", "Comparison", "Completed", reports.comparison_report(c))
            log_once(("hist", "cmp", ss.cmp_a["id"], ss.cmp_b["id"]), f"{c['names'][0]} vs {c['names'][1]}"[:80], c["stats"]["A"]["doc_type"],
                     "Comparison", "Completed", c["similarity"], payload={"similarity": c["similarity"], "added": len(c["added"]),
                     "removed": len(c["removed"]), "changed": len(c["changed"]), "names": c["names"]})
    c = ss.cmp_result
    if not c:
        st.write("")
        with card("cases"):
            h3("Common Use Cases")
            cols = st.columns(4)
            for col, (t, d) in zip(cols, CASES):
                col.markdown(f'<div class="dc-feature"><div class="ic">{svg("file", 20)}</div><b>{t}</b><span>{d}</span></div>', unsafe_allow_html=True)
        return
    st.write("")
    m = st.columns(4)
    for col, (lab, val) in zip(m, [("Similarity", f"{c['similarity']}%"), ("Identical lines", len(c["same"])), ("Changed lines", len(c["changed"])),
                                   ("Added / Removed", f"{len(c['added'])} / {len(c['removed'])}")]):
        col.metric(lab, val)
    t = st.tabs(["Similarities", "Differences", "Sections", "Entities", "Statistics"])
    with t[0], card("c_sim"):
        h3("Similarities")
        st.write(f"The documents are **{c['similarity']}% similar**. {len(c['same'])} line(s) are identical.")
        md(f'<div class="dc-muted">Shared keywords</div>{pills(c["common_keywords"])}')
        for x in c["same"][:15]:
            md(f'<div class="dc-ins ok"><span>{escape(x[:240])}</span></div>')
    with t[1]:
        c1, c2 = st.columns(2)
        with c1, card("c_add"):
            h3(f"Added in B ({len(c['added'])})")
            for x in c["added"][:20] or ["Nothing was added."]:
                md(f'<div class="dc-ins ok"><span>+ {escape(x[:240])}</span></div>')
        with c2, card("c_rem"):
            h3(f"Removed from A ({len(c['removed'])})")
            for x in c["removed"][:20] or ["Nothing was removed."]:
                md(f'<div class="dc-ins" style="border-left-color:#EF4444"><span>− {escape(x[:240])}</span></div>')
        with card("c_chg"):
            h3(f"Changed lines ({len(c['changed'])})")
            if c["changed"]:
                html_table(["Document A", "Document B", "Similarity"], [[x["before"][:200], x["after"][:200], f"{int(x['ratio'] * 100)}%"] for x in c["changed"][:25]])
            else:
                st.info("No changed lines.")
    with t[2], card("c_sec"):
        h3("Changed sections")
        html_table(["Section", "Status", "Similarity"], [[x["section"], badge(x["status"]), f"{x['similarity']}%"] for x in c["sections"]], raw_cols=(1,))
    with t[3], card("c_ent"):
        h3("Common entities")
        shown = False
        for k, v_ in c["entities"].items():
            if v_["common"] or v_["only_a"] or v_["only_b"]:
                shown = True
                md(f'<div class="dc-muted" style="margin-top:.5rem"><b>{k.title()}</b></div>Common: {pills(v_["common"])}<br>Only in A: {pills(v_["only_a"])}<br>Only in B: {pills(v_["only_b"])}')
        if not shown:
            st.info("No entities detected in either document.")
    with t[4], card("c_stats"):
        h3("Document statistics")
        A, B = c["stats"]["A"], c["stats"]["B"]
        html_table(["Metric", A["name"], B["name"]], [[k.replace("_", " ").title(), A[k], B[k]] for k in ("doc_type", "pages", "words", "characters", "paragraphs")])
    st.download_button("Download Comparison Report", ss.cache[("report", "cmp")], file_name="Comparison_Report.pdf", mime="application/pdf",
                       type="primary", icon=":material/download:", key="dl_cmp")
