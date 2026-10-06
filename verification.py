import streamlit as st
from components.state import need_doc, get_analysis, get_verification, log_once, save_report_file
from components.ui import header, md, card, h3, svg, ring, badge, doc_html, html_table
from utils import reports


@st.dialog("Custom verification rules", width="large")
def rules_dialog():
    st.write("Define the information this document must contain. One rule per line, in the format `Field: keyword1, keyword2` "
             "(keywords are optional - the field name is used when omitted). Example: `Date of Birth: dob, born`")
    cur = "\n".join(f"{r['field']}: {', '.join(r['keywords'])}" for r in st.session_state.custom_rules)
    txt = st.text_area("Rules", value=cur, height=200, placeholder="Signature: signature, signed\nPassport Number\nAddress: address, street", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    if c1.button("Apply rules", type="primary", width="stretch"):
        rules = []
        for ln in txt.splitlines():
            if not ln.strip():
                continue
            name, _, kw = ln.partition(":")
            kws = [k.strip() for k in kw.split(",") if k.strip()]
            rules.append({"field": name.strip()[:60], "keywords": kws or [name.strip()]})
        if not rules:
            st.error("Please enter at least one rule.")
        else:
            st.session_state.custom_rules = rules
            st.rerun()
    if c2.button("Reset to default checklist", width="stretch"):
        st.session_state.custom_rules = []
        st.rerun()


def render():
    doc = need_doc()
    if not doc:
        return
    a = get_analysis(doc)["a"]
    with st.spinner("Analyzing document..."):
        v = get_verification(doc)
    sig = f"{doc['id']}|{len(st.session_state.custom_rules)}|{v['score']}"
    key = ("report", "verification", sig)
    stem = reports.safe_stem(doc["name"])
    if key not in st.session_state.cache:
        with st.spinner("Generating report..."):
            save_report_file(key, f"{stem}_Verification_Report.pdf", doc["name"], "Verification", v["status"],
                             reports.verification_report(doc, a, v))
    log_once(("hist", "Verification", sig), doc["name"], a["doc_type"], "Verification", v["status"], v["score"],
             payload={"score": v["score"], "label": v["label"], "checklist": v["checklist"], "issues": v["issues"], "explanation": v["explanation"]})
    header("Document Verification")
    with card("doc"):
        l, r = st.columns([5, 1.4], vertical_alignment="center")
        l.markdown(doc_html(doc), unsafe_allow_html=True)
        r.button("Change File", key="chg_ver", width="stretch", on_click=lambda: st.session_state.update(page="upload", doc=None, upload_key=st.session_state.upload_key + 1))
    st.write("")
    left, right = st.columns([1.55, 1])
    with left, card("checklist"):
        h3("Verification Checklist" + (" (custom rules)" if v["custom"] else ""))
        rows = [[c["field"], badge(c["status"]), c["detail"]] for c in v["checklist"]]
        html_table(["Field", "Status", "Details"], rows, raw_cols=(1,))
    with right:
        with card("overall"):
            h3("Overall Result")
            md(ring(v["score"], v["label"]))
            kind = {"Complete": "green", "Needs Attention": "orange", "Incomplete": "red"}[v["label"]]
            md(f'<div style="text-align:center;margin:.4rem 0">{badge(v["label"], kind)}</div><div class="dc-muted" style="text-align:center">{v["explanation"]}</div>')
        with card("custom"):
            h3("Custom Verification")
            st.caption("Create your own verification rules for any document type." + (f" {len(st.session_state.custom_rules)} rule(s) active." if v["custom"] else ""))
            if st.button("Set Custom Rules", key="set_rules", width="stretch"):
                rules_dialog()
    if v["issues"]:
        st.write("")
        with card("issues"):
            h3("Inconsistencies Detected")
            for i in v["issues"]:
                md(f"<div class=\"dc-ins warn\"><span>{__import__('html').escape(i)}</span></div>")
    st.write("")
    _, b = st.columns([4, 1.4])
    b.download_button("Generate Report", st.session_state.cache[key], file_name=f"{stem}_Verification_Report.pdf", mime="application/pdf",
                      type="primary", icon=":material/description:", width="stretch", key="dl_ver")
