"""Left navigation sidebar and settings dialog."""
import streamlit as st
from components.state import go
from components.ui import md, svg
from utils import ai, database

NAV = [("home", "Home", "home"), ("upload", "Upload", "cloud_upload"), ("analysis", "Analysis", "analytics"),
       ("verification", "Verification", "verified_user"), ("multi", "Multi-Document", "library_books"),
       ("comparison", "Comparison", "compare"), ("assistant", "Q&A", "forum"), ("dashboard", "Dashboard", "space_dashboard"),
       ("history", "History", "history"), ("reports", "Reports", "description")]

LOGO = ('<div class="dc-logo"><div class="mark"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="9 14 11 16 15 12"/></svg></div>DOCUCHECK</div>')


@st.dialog("Settings")
def settings_dialog():
    st.markdown("**Gemini AI**")
    if ai.available():
        st.success("GEMINI_API_KEY detected. AI summaries and Q&A are enabled.")
    else:
        st.warning("No GEMINI_API_KEY found. Copy `.env.example` to `.env`, add your key and restart the app. "
                   "DOCUCHECK still works with basic local processing.")
    st.markdown("**Data**")
    st.caption("Uploaded documents live only in your browser session. History and generated reports are stored locally in the `data/` folder.")
    c1, c2 = st.columns(2)
    if c1.button("Clear session", width="stretch"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    if c2.button("Delete history & reports", width="stretch"):
        database.clear_all()
        st.session_state.logged = set()
        st.session_state.cache = {}
        st.toast("History and reports deleted.")
        st.rerun()


def render():
    cur = st.session_state.page
    active = "upload" if cur == "action" else cur
    with st.sidebar:
        md(LOGO)
        for key, label, icon in NAV:
            st.button(label, key=f"nav_{key}", icon=f":material/{icon}:", width="stretch",
                      type="primary" if key == active else "secondary", on_click=go, args=(key,))
        st.write("")
        st.write("")
        if st.button("Settings", key="nav_settings", icon=":material/settings:", width="stretch"):
            settings_dialog()
        md(f'<div class="dc-secure">{svg("lock", 16, "#64748B")}<span>Your documents are secure and not permanently stored.</span></div>')
