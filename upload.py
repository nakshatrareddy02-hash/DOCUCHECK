import streamlit as st
from components.state import go, reset_doc
from components.ui import header, md, svg, doc_html, card, h3
from utils.parser import parse_document

TYPES = ["pdf", "docx", "txt", "jpg", "jpeg", "png"]


def _ingest(f) -> dict | None:
    data = f.getvalue()
    pid = f"{f.name}:{len(data)}"
    store = st.session_state.store
    if pid not in store:
        with st.spinner("Processing document..."):
            store[pid] = parse_document(f.name, data)
    return store[pid]


def render():
    header("Upload Your Document", "Upload a document to get started. We support PDF, DOCX, TXT and scanned documents (OCR).")
    ss = st.session_state
    with card("upload"):
        f = st.file_uploader("Upload a document", type=TYPES, key=f"up_{ss.upload_key}", label_visibility="collapsed")
        md('<div class="dc-muted" style="text-align:center;margin-top:.6rem">Supported formats: PDF, DOCX, TXT, JPG, PNG (scanned) • Max 25 MB</div>')
    if f is not None:
        doc = _ingest(f)
        if doc["error"]:
            st.error(f"**{doc['name']}** could not be processed. {doc['error']}")
            ss.doc = None
        else:
            ss.doc = doc
            if doc["warning"]:
                st.warning(doc["warning"])
    doc = ss.doc
    st.write("")
    if doc:
        with card("uploaded"):
            md('<div class="dc-ok" style="font-size:1.05rem"><div class="c" style="width:30px;height:30px">' + svg("check", 16, "#fff", 3) + '</div>Document Uploaded Successfully!</div>')
            c = st.columns(4)
            for col, (k, v) in zip(c, [("File name", doc["name"]), ("File type", doc["ext"]), ("File size", doc["size_label"]), ("Pages", doc["pages"])]):
                col.markdown(f'<div class="dc-muted">{k}</div><div style="font-weight:600;word-break:break-all">{v}</div>', unsafe_allow_html=True)
    ok = [d for d in ss.store.values() if not d["error"]]
    if ok:
        st.write("")
        h3("Recent Uploads")
        for d in list(ok)[-4:][::-1]:
            with card(f"recent_{abs(hash(d['id'])) % 10**6}"):
                a, b, c = st.columns([6, 1.3, .8], vertical_alignment="center")
                a.markdown(doc_html(d), unsafe_allow_html=True)
                key = f"use_{abs(hash(d['id'])) % 10**6}"
                if ss.doc is not None and ss.doc["id"] == d["id"]:
                    b.markdown('<span class="dc-badge b-purple">Selected</span>', unsafe_allow_html=True)
                else:
                    if b.button("Use", key=key):
                        ss.doc = d
                        st.rerun()
                if c.button("✕", key=f"rm_{key}", help="Remove"):
                    ss.store.pop(d["id"], None)
                    if ss.doc is not None and ss.doc["id"] == d["id"]:
                        reset_doc()
                    st.rerun()
    st.write("")
    b1, _, b2 = st.columns([1.2, 4, 1.4])
    b1.button("Change File", key="chg", width="stretch", on_click=reset_doc)
    if b2.button("Continue  →", type="primary", key="cont", width="stretch"):
        if ss.doc:
            go("action")
            st.rerun()
        else:
            st.warning("No document uploaded yet. Please upload a document to continue.")
