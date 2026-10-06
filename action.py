import streamlit as st
from components.state import go, need_doc, reset_doc
from components.ui import header, md, svg, doc_html, card

ACTIONS = [
    ("analysis", "Analysis", "search", "linear-gradient(135deg,#4F46E5,#6366F1)", "Analyze one document",
     ["Extract information", "Identify sections", "Summarize content", "Generate insights"], "Analyze  →", "analysis", "btn_analyze"),
    ("verification", "Verification", "shield", "linear-gradient(135deg,#059669,#10B981)", "Verify one document",
     ["Check required information", "Find missing fields", "Check completeness", "Detect inconsistencies"], "Verify  →", "verification", "btn_verify"),
    ("multi", "Multi-Document Analysis", "layers", "linear-gradient(135deg,#7C3AED,#A78BFA)", "Analyze multiple documents",
     ["Cross-document insights", "Find inconsistencies", "Combined summary", "Information mapping"], "Multi-Document  →", "multi", "btn_multi"),
]


def render():
    doc = need_doc()
    if not doc:
        return
    md('<div class="dc-ok"><div class="c">' + svg("check", 20, "#fff", 3) + '</div>Document Uploaded Successfully!</div>')
    with card("doc"):
        a, b = st.columns([6, 1.2], vertical_alignment="center")
        a.markdown(doc_html(doc), unsafe_allow_html=True)
        if b.button("Change File", key="chg_action", width="stretch", on_click=lambda: (reset_doc(), go("upload"))):
            pass
    st.write("")
    md('<div class="dc-h3" style="font-size:1.25rem">What would you like to do?</div>')
    cols = st.columns(3)
    for col, (key, title, ic, grad, sub, items, label, page, bkey) in zip(cols, ACTIONS):
        with col, card(f"act_{key}"):
            md(f'<div class="dc-action-head" style="background:{grad}">{svg(ic, 34, "#fff", 1.6)}{title}</div>'
               f'<div style="font-weight:700;margin-bottom:.4rem">{sub}</div><ul class="dc-list">' +
               "".join(f'<li>{svg("check", 14, "#10B981", 3)}{i}</li>' for i in items) + '</ul>')
            st.button(label, key=bkey, type="primary", width="stretch", on_click=go, args=(page,))
