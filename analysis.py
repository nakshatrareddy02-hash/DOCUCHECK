import streamlit as st
from html import escape
from components.state import need_doc, get_analysis, log_once, save_report_file, go
from components.ui import header, md, card, h3, pills, html_table, donut, doc_html, badge
from utils import reports

ENT_ROWS = [("persons", "Person"), ("locations", "Location"), ("dates", "Date"), ("organizations", "Organization"),
            ("emails", "Email"), ("phones", "Phone"), ("qualifications", "Qualification"), ("skills", "Skills"), ("urls", "URL")]


def render():
    doc = need_doc()
    if not doc:
        return
    res = get_analysis(doc)
    a, tl = res["a"], res["timeline"]
    summary = res["ai_summary"] or a["summary"]
    key = ("report", "analysis", doc["id"])
    if key not in st.session_state.cache:
        with st.spinner("Generating report..."):
            from utils.reports import safe_stem
            data = reports.analysis_report(doc, a, tl, summary)
            save_report_file(key, f"{safe_stem(doc['name'])}_Analysis_Report.pdf", doc["name"], "Analysis", "Completed", data)
    log_once(("hist", "Analysis", doc["id"]), doc["name"], a["doc_type"], "Analysis", "Completed",
             payload={"stats": {k: a[k] for k in ("words", "pages", "characters", "paragraphs", "language")}, "summary": summary,
                      "entities": a["entities"], "keywords": a["keywords"]})
    header("Document Analysis")
    with card("doc"):
        l, r = st.columns([5, 1.6], vertical_alignment="center")
        l.markdown(doc_html(doc), unsafe_allow_html=True)
        r.download_button("Download Report", st.session_state.cache[key], file_name=f"{reports.safe_stem(doc['name'])}_Analysis_Report.pdf",
                          mime="application/pdf", icon=":material/download:", width="stretch", key="dl_analysis")
    st.write("")
    t = st.tabs(["Overview", "Extracted Info", "Entities", "Timeline", "Summary", "Insights"])
    e = a["entities"]
    with t[0]:
        c1, c2 = st.columns(2)
        with c1, card("ov"):
            h3("Document Overview")
            html_table(["Property", "Value"], [["Document Type", a["doc_type"]], ["Pages", a["pages"]], ["Words", a["words"]],
                                               ["Sections Detected", len(a["sections"])], ["Language", a["language"]],
                                               ["Characters", a["characters"]], ["Paragraphs", a["paragraphs"]]])
            md(f'<div class="dc-muted" style="margin:.8rem 0 .4rem 0">Keywords</div>{pills(a["keywords"])}')
        with c2, card("stats"):
            h3("Document Statistics")
            vals = [("Text", a["body_words"]), ("Headers", a["head_words"]), ("Lists", a["list_words"])]
            vals = [v for v in vals if v[1] > 0] or [("Text", 1)]
            donut([v[0] for v in vals], [v[1] for v in vals], f"<b>{a['words']}</b><br>words")
            m = st.columns(3)
            for col, (lab, v) in zip(m, [("Words", a["words"]), ("Headers", len(a["headings"])), ("Images", a["images"])]):
                col.metric(lab, v)
    with t[1]:
        rows = [["Name", ", ".join(e["persons"][:2]) or "Not detected"], ["Email", ", ".join(e["emails"]) or "Not detected"],
                ["Phone", ", ".join(e["phones"]) or "Not detected"], ["Location", ", ".join(e["locations"][:4]) or "Not detected"],
                ["Education / Qualifications", ", ".join(e["qualifications"]) or "Not detected"],
                ["Organizations", ", ".join(e["organizations"][:5]) or "Not detected"], ["Skills", ", ".join(e["skills"]) or "Not detected"],
                ["Links", ", ".join(e["urls"][:4]) or "Not detected"], ["Dates", ", ".join(e["dates"][:6]) or "Not detected"]]
        with card("extracted"):
            h3("Extracted Information")
            html_table(["Field", "Value"], rows)
            st.caption("Extraction uses pattern matching and may be imperfect.")
        if a["headings"]:
            with card("sections"):
                h3("Sections Detected")
                md(pills(a["headings"][:30]))
    with t[2]:
        with card("entities"):
            h3("Important Entities")
            cols = st.columns(3)
            shown = [(k, lab) for k, lab in ENT_ROWS if e[k]]
            if not shown:
                st.info("No entities were detected in this document.")
            for i, (k, lab) in enumerate(shown):
                with cols[i % 3]:
                    md(f'<div class="dc-entity"><b>{lab}</b><span class="dc-badge b-purple">{len(e[k])}</span></div><div style="margin:-.1rem 0 .8rem 0">{pills(e[k][:10])}</div>')
    with t[3]:
        with card("timeline"):
            h3("Timeline")
            if tl:
                html_table(["Date", "Context"], [[r["date"], r["context"]] for r in tl[:30]])
            else:
                st.info("No dates were found in this document.")
    with t[4]:
        with card("summary"):
            h3("Summary")
            st.write(summary)
            st.caption("Generated with Gemini AI." if res["ai_summary"] else "Basic local summary. Add a GEMINI_API_KEY for AI-written summaries.")
            md(f'<div class="dc-muted">Top keywords</div>{pills(a["keywords"][:8])}')
        if a["sections"]:
            with card("secsum"):
                h3("Section Preview")
                for s in a["sections"][:8]:
                    with st.expander(f"{s['title']}  ({len(s['lines'])} lines)"):
                        st.write("\n".join(s["lines"][:8]))
    with t[5]:
        for i in res["insights"]:
            md(f'<div class="dc-ins {i["level"]}"><b>{escape(i["title"])}</b><span>{escape(i["text"])}</span></div>')
        st.button("Verify this document  →", type="primary", on_click=go, args=("verification",), key="to_verify")
