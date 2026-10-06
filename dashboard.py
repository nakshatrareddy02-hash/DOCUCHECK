import streamlit as st
from components.ui import header, md, card, h3, metric, donut, bars, html_table, badge, empty_state
from utils import database

COLORS = {"Resume": "#4F46E5", "Certificate": "#10B981", "Application": "#F59E0B", "Report": "#8B5CF6", "Other": "#94A3B8"}


def render():
    header("Dashboard", "Welcome back! Here's an overview of your document activity.")
    s = database.stats()
    c = st.columns(4)
    cards = [("file", s["processed"], "Documents Processed", "#EEF2FF", "#4F46E5"), ("shield", s["verified"], "Verified", "#ECFDF5", "#059669"),
             ("compare", s["compared"], "Compared", "#F5F3FF", "#7C3AED"),
             ("bar", f"{s['avg']}%" if s["avg"] is not None else "–", "Avg. Completeness", "#FFFBEB", "#D97706")]
    for col, args in zip(c, cards):
        col.markdown(metric(*args), unsafe_allow_html=True)
    st.write("")
    if not s["total"]:
        empty_state("No activity yet", "Upload a document and run an analysis or verification to see statistics here.", "bar")
        return
    l, r = st.columns(2)
    with l, card("d_types"):
        h3("Document Types")
        if s["types"]:
            labels = list(s["types"].keys())
            donut(labels, list(s["types"].values()), f"<b>{sum(s['types'].values())}</b><br>Total", colors=[COLORS.get(x, "#94A3B8") for x in labels])
        else:
            st.caption("Analyze a document to see types.")
    with r, card("d_res"):
        h3("Verification Results")
        res = s["results"]
        if res:
            bars(["Verified", "Needs Attention", "Failed"], [res.get("Verified", 0), res.get("Needs Attention", 0), res.get("Failed", 0)], ["#10B981", "#F59E0B", "#EF4444"])
        else:
            st.caption("Run a verification to see results.")
    st.write("")
    with card("d_recent"):
        h3("Recent Activity")
        rows = [[x["document"], x["doc_type"], x["action"], badge(x["status"]), x["created"]] for x in s["recent"]]
        html_table(["Document", "Type", "Action", "Status", "Date"], rows, raw_cols=(3,))
