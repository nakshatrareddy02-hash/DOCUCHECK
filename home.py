import streamlit as st
from components.state import go
from components.ui import md, svg, h3

HERO_SVG = """<svg viewBox="0 0 440 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:470px">
<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C7D2FE"/><stop offset="1" stop-color="#EEF2FF"/></linearGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#4F46E5" flood-opacity=".18"/></filter></defs>
<circle cx="250" cy="160" r="150" fill="url(#g1)" opacity=".7"/><circle cx="390" cy="60" r="8" fill="#C7D2FE"/><circle cx="60" cy="90" r="5" fill="#C7D2FE"/>
<g filter="url(#sh)"><rect x="170" y="40" width="150" height="190" rx="10" fill="#fff" transform="rotate(-6 245 135)"/>
<rect x="200" y="30" width="160" height="200" rx="10" fill="#fff" stroke="#E0E7FF"/></g>
<rect x="216" y="50" width="70" height="9" rx="4" fill="#4F46E5"/><rect x="216" y="70" width="128" height="6" rx="3" fill="#CBD5E1"/><rect x="216" y="84" width="110" height="6" rx="3" fill="#E2E8F0"/>
<rect x="216" y="98" width="128" height="6" rx="3" fill="#E2E8F0"/><rect x="216" y="120" width="52" height="40" rx="5" fill="#E0E7FF"/><rect x="276" y="120" width="68" height="6" rx="3" fill="#CBD5E1"/>
<rect x="276" y="134" width="56" height="6" rx="3" fill="#E2E8F0"/><rect x="276" y="148" width="68" height="6" rx="3" fill="#E2E8F0"/><rect x="216" y="172" width="128" height="6" rx="3" fill="#E2E8F0"/>
<rect x="216" y="186" width="96" height="6" rx="3" fill="#E2E8F0"/><rect x="216" y="200" width="118" height="6" rx="3" fill="#E2E8F0"/>
<g filter="url(#sh)"><path d="M70 170h60l14 16h96a10 10 0 0 1 10 10v84a10 10 0 0 1-10 10H70a10 10 0 0 1-10-10V180a10 10 0 0 1 10-10z" fill="#6366F1"/>
<path d="M60 205h180v75a10 10 0 0 1-10 10H70a10 10 0 0 1-10-10z" fill="#4F46E5"/></g>
<circle cx="190" cy="215" r="44" fill="#fff" fill-opacity=".55" stroke="#4338CA" stroke-width="9"/><circle cx="190" cy="215" r="34" fill="#C7D2FE" fill-opacity=".35"/>
<line x1="224" y1="249" x2="262" y2="287" stroke="#312E81" stroke-width="12" stroke-linecap="round"/>
<path d="M172 214l12 12 22-24" fill="none" stroke="#4F46E5" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<g filter="url(#sh)"><circle cx="352" cy="190" r="34" fill="#10B981"/></g><path d="M336 190l11 11 20-22" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

FEATURES = [("zap", "Smart Analysis", "Extract & understand key information"), ("shield", "Accurate Verification", "Check completeness & validity"),
            ("layers", "Multi-Document Support", "Analyze documents together"), ("lock", "Secure & Private", "Your data stays safe and private")]


@st.dialog("How DOCUCHECK works", width="large")
def how_dialog():
    steps = [("1. Upload", "Add a PDF, DOCX, TXT or scanned image (JPG/PNG). Text is extracted automatically, with OCR for images when available."),
             ("2. Choose an action", "Analyse one document, verify its completeness, or analyse several documents together."),
             ("3. Review the results", "See entities, statistics, a timeline, a summary, verification status and detected inconsistencies."),
             ("4. Ask & compare", "Compare two documents side by side or ask questions in plain language using the Gemini-powered assistant."),
             ("5. Download", "Every analysis produces a PDF report you can download from the Reports page. History and the dashboard update automatically.")]
    for t, d in steps:
        st.markdown(f"**{t}**  \n{d}")
    st.button("Get Started", type="primary", on_click=go, args=("upload",))


@st.dialog("About DOCUCHECK")
def about_dialog():
    st.markdown("**DOCUCHECK – Understand. Analyze. Verify.**")
    st.write("DOCUCHECK is an intelligent document platform that extracts information, analyses content and verifies whether required "
             "information is complete and valid. It uses rule-based text processing, with optional Gemini AI for summaries and Q&A. "
             "Detection is pattern-based and may not be perfectly accurate - always review important results.")


def render():
    c = st.columns([2.4, 2.6, .8, 1.5, .8, 1.5], vertical_alignment="center")
    c[0].markdown('<div class="dc-nav-logo"><div class="mark" style="width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#4F46E5,#6366F1);'
                  'display:flex;align-items:center;justify-content:center"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="9 14 11 16 15 12"/></svg></div>DOCUCHECK</div>', unsafe_allow_html=True)
    c[2].button("Home", type="tertiary", key="top_home")
    if c[3].button("How It Works", type="tertiary", key="top_how"):
        how_dialog()
    if c[4].button("About", type="tertiary", key="top_about"):
        about_dialog()
    c[5].button("Get Started", type="primary", key="top_start", width="stretch", on_click=go, args=("upload",))
    st.write("")
    l, r = st.columns([1.05, 1], vertical_alignment="center")
    with l:
        md_html = ('<div class="dc-hero"><h1>DOCUCHECK</h1><h2>Understand. Analyze. Verify.</h2><p>An intelligent document platform that extracts '
                   'important information, analyzes content, and verifies whether required information is complete and valid.</p></div>')
        st.markdown(md_html, unsafe_allow_html=True)
        b1, b2, _ = st.columns([1.1, 1.1, 1.2])
        b1.button("Get Started", type="primary", key="hero_start", width="stretch", on_click=go, args=("upload",))
        if b2.button("How It Works", key="hero_how", width="stretch"):
            how_dialog()
    r.markdown(f'<div style="display:flex;justify-content:center">{HERO_SVG}</div>', unsafe_allow_html=True)
    st.write("")
    with st.container(border=True, key="card_features"):
        cols = st.columns(4)
        for col, (ic, t, d) in zip(cols, FEATURES):
            col.markdown(f'<div class="dc-feature"><div class="ic">{svg(ic, 22)}</div><b>{t}</b><span>{d}</span></div>', unsafe_allow_html=True)
