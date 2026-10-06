"""DOCUCHECK – Understand. Analyze. Verify."""
import streamlit as st

st.set_page_config(page_title="DOCUCHECK", page_icon="📄", layout="wide", initial_sidebar_state="expanded")

from components import sidebar, state, styles
from views import action, analysis, assistant, comparison, dashboard, history, home, multi_document, reports, upload, verification

ROUTES = {"home": home, "upload": upload, "action": action, "analysis": analysis, "verification": verification, "multi": multi_document,
          "comparison": comparison, "assistant": assistant, "dashboard": dashboard, "history": history, "reports": reports}


def main():
    state.init()
    page = st.session_state.page if st.session_state.page in ROUTES else "home"
    styles.inject(hide_sidebar=(page == "home"))
    if page != "home":
        sidebar.render()
    try:
        ROUTES[page].render()
    except Exception as exc:  # last-resort guard so users never see a raw traceback
        st.error(f"Something went wrong while showing this page ({type(exc).__name__}: {exc}). Please try again or go back to Upload.")
        st.button("Back to Upload", on_click=state.go, args=("upload",))


main()
