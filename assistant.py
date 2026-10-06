import streamlit as st

from components.state import need_doc, get_analysis, get_verification
from components.ui import header
from utils import ai


SUGGESTED = [
    "What is this document about?",
    "Summarize this document.",
    "What are the important details?",
    "What information is missing?",
    "What are the key entities?",
]


def render():

    header(
        "Ask Your Document",
        "Ask questions about your document and get instant answers."
    )

    doc = need_doc()

    if not doc:
        return

    ss = st.session_state

    hist = ss.chat.setdefault(doc["id"], [])

    # ---------------------------------------------------------
    # AI STATUS
    # ---------------------------------------------------------

    if not ai.available():

        st.info(
            "**Gemini is not configured.** "
            "Copy `.env.example` to `.env`, set "
            "`GEMINI_API_KEY=your_key` and restart the app. "
            "Until then, answers come from basic local processing."
        )

    # ---------------------------------------------------------
    # DOCUMENT INFO
    # ---------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 📄 Current Document")

        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"**{doc['name']}**")

        with col2:
            st.caption("✓ Analyzed")

    st.markdown("### 💡 Suggested Questions")

    cols = st.columns(3)

    for i, q in enumerate(SUGGESTED):

        col = cols[i % 3]

        if col.button(
            q,
            key=f"sq_{i}",
            width="stretch"
        ):
            ss.pending_q = q

    # ---------------------------------------------------------
    # CHAT HISTORY
    # ---------------------------------------------------------

    for m in hist:

        with st.chat_message(m["role"]):

            st.markdown(m["content"])

            # Evidence is stored separately with assistant messages.
            if (
                m["role"] == "assistant"
                and m.get("evidence")
            ):

                with st.expander(
                    "📍 View Evidence from Document"
                ):

                    st.caption(
                        "Relevant information found in the "
                        "uploaded document:"
                    )

                    for index, evidence in enumerate(
                        m["evidence"],
                        start=1
                    ):

                        st.markdown(
                            f"**Evidence {index}**"
                        )

                        st.info(evidence)

    # ---------------------------------------------------------
    # USER QUESTION
    # ---------------------------------------------------------

    typed = st.chat_input(
        "Ask anything about your document..."
    )

    q = typed or ss.pending_q

    ss.pending_q = None

    if q:

        # -----------------------------------------------------
        # USER MESSAGE
        # -----------------------------------------------------

        with st.chat_message("user"):
            st.markdown(q)

        # -----------------------------------------------------
        # AI RESPONSE
        # -----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing your document..."
            ):

                ans, err = ai.ask(
                    q,
                    doc["text"],
                    hist
                )

                # ---------------------------------------------
                # LOCAL FALLBACK
                # ---------------------------------------------

                if ans is None:

                    a = get_analysis(doc)["a"]

                    local = ai.local_answer(
                        q,
                        doc,
                        a,
                        get_verification(doc)
                    )

                    if err == "missing_key":

                        ans = (
                            local
                            + "\n\n"
                            "*Basic local answer — add a "
                            "GEMINI_API_KEY for AI answers.*"
                        )

                    else:

                        ans = (
                            f"⚠️ {err}\n\n"
                            f"{local}"
                        )

                # ---------------------------------------------
                # SHOW ANSWER
                # ---------------------------------------------

                st.markdown(ans)

                # ---------------------------------------------
                # FIND EVIDENCE
                # ---------------------------------------------

                evidence = ai.evidence_for_question(
                    q,
                    doc["text"],
                    max_items=3
                )

                if evidence:

                    with st.expander(
                        "📍 View Evidence from Document"
                    ):

                        st.caption(
                            "Relevant excerpts from your "
                            "uploaded document:"
                        )

                        for index, item in enumerate(
                            evidence,
                            start=1
                        ):

                            st.markdown(
                                f"**Evidence {index}**"
                            )

                            st.info(item)

                else:

                    evidence = []

                    st.caption(
                        "📍 No directly matching evidence "
                        "was found in the extracted text."
                    )

        # -----------------------------------------------------
        # SAVE CONVERSATION
        # -----------------------------------------------------

        hist.append(
            {
                "role": "user",
                "content": q,
            }
        )

        hist.append(
            {
                "role": "assistant",
                "content": ans,
                "evidence": evidence,
            }
        )

    # ---------------------------------------------------------
    # CLEAR CHAT
    # ---------------------------------------------------------

    if hist:

        st.divider()

        if st.button(
            "Clear conversation",
            key="clr_chat"
        ):

            ss.chat[doc["id"]] = []

            st.rerun()