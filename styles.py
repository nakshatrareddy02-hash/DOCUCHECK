"""Global CSS for the DOCUCHECK look & feel."""
import streamlit as st

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--primary:#4F46E5;--secondary:#6366F1;--soft:#EEF2FF;--green:#10B981;--orange:#F59E0B;--red:#EF4444;
--navy:#172554;--muted:#64748B;--bg:#F8FAFC;--card:#FFFFFF;--border:#E2E8F0;}
html,body,[class*="css"],.stApp,button,input,textarea{font-family:'Inter',-apple-system,'Segoe UI',Roboto,sans-serif!important;}
.stApp{background:var(--bg);color:var(--navy);}
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
header[data-testid="stHeader"]{background:transparent;height:2.5rem;}
.block-container{max-width:1180px;padding:1.6rem 2rem 3rem 2rem;}
h1,h2,h3,h4{color:var(--navy);letter-spacing:-0.01em;}
p,li,span,label{color:inherit;}
/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--border);min-width:250px;max-width:250px;}
[data-testid="stSidebar"] > div:first-child{padding-top:.6rem;}
[data-testid="stSidebarUserContent"]{padding:0 .9rem 1rem .9rem;}
[data-testid="stSidebar"] .stButton>button{justify-content:flex-start;gap:.6rem;background:transparent;border:none;color:#475569;
 font-weight:500;font-size:.9rem;padding:.55rem .8rem;border-radius:10px;box-shadow:none;min-height:0;}
[data-testid="stSidebar"] .stButton>button p{font-size:.9rem;font-weight:500;}
[data-testid="stSidebar"] .stButton>button:hover{background:#F1F5F9;color:var(--primary);border:none;}
[data-testid="stSidebar"] .stButton>button>div{justify-content:flex-start!important;width:100%;gap:.6rem;}
[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"]{background:var(--soft);color:var(--primary);font-weight:600;border:none!important;box-shadow:none;}
[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"]:hover{background:var(--soft);color:var(--primary);}
[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"] p,[data-testid="stSidebar"] .stButton>button[data-testid="stBaseButton-primary"] span{font-weight:600;color:var(--primary)!important;}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.15rem;}
.dc-logo{display:flex;align-items:center;gap:.6rem;font-weight:800;color:var(--navy);font-size:1.05rem;letter-spacing:.02em;padding:.6rem .4rem 1.1rem .4rem;}
.dc-logo .mark{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#4F46E5,#6366F1);display:flex;align-items:center;justify-content:center;}
.dc-secure{font-size:.72rem;color:var(--muted);display:flex;gap:.5rem;align-items:flex-start;padding:.9rem .5rem 0 .5rem;border-top:1px solid var(--border);margin-top:.6rem;line-height:1.35;}
/* ---------- buttons ---------- */
.stButton>button,.stDownloadButton>button{border-radius:10px;font-weight:600;font-size:.88rem;padding:.55rem 1.2rem;border:1px solid var(--border);
 background:#fff;color:var(--navy);transition:all .15s ease;box-shadow:0 1px 2px rgba(15,23,42,.04);}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--secondary);color:var(--primary);background:#fff;}
.stButton>button[data-testid="stBaseButton-primary"],.stDownloadButton>button[data-testid="stBaseButton-primary"]{background:var(--primary);color:#fff;border:1px solid var(--primary);
 box-shadow:0 4px 12px rgba(79,70,229,.25);}
.stButton>button[data-testid="stBaseButton-primary"]:hover,.stDownloadButton>button[data-testid="stBaseButton-primary"]:hover{background:#4338CA;color:#fff;border-color:#4338CA;}
.stButton>button[data-testid="stBaseButton-primary"] p,.stDownloadButton>button[data-testid="stBaseButton-primary"] p{color:#fff;}
.stButton>button[data-testid="stBaseButton-tertiary"]{border:none;background:transparent;box-shadow:none;color:#475569;font-weight:500;}
.stButton>button[data-testid="stBaseButton-tertiary"]:hover{color:var(--primary);background:transparent;}
.st-key-btn_verify button{background:var(--green)!important;border-color:var(--green)!important;box-shadow:0 4px 12px rgba(16,185,129,.25)!important;}
.st-key-btn_multi button{background:#8B5CF6!important;border-color:#8B5CF6!important;box-shadow:0 4px 12px rgba(139,92,246,.25)!important;}
.st-key-btn_verify button:hover{background:#059669!important;}.st-key-btn_multi button:hover{background:#7C3AED!important;}
/* ---------- cards ---------- */
[class*="st-key-card"]{background:var(--card);border:1px solid var(--border)!important;border-radius:14px!important;box-shadow:0 1px 3px rgba(15,23,42,.05);padding:1.1rem 1.25rem!important;}
.dc-card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:1.1rem 1.25rem;box-shadow:0 1px 3px rgba(15,23,42,.05);}
.dc-title{font-size:1.9rem;font-weight:700;color:var(--navy);margin:.2rem 0 .3rem 0;letter-spacing:-0.02em;}
.dc-sub{color:var(--muted);font-size:.95rem;margin-bottom:1.3rem;max-width:760px;}
.dc-h3{font-size:1rem;font-weight:700;color:var(--navy);margin:0 0 .8rem 0;}
.dc-muted{color:var(--muted);font-size:.85rem;}
.dc-doc{display:flex;align-items:center;gap:.9rem;}
.dc-doc .ico{width:42px;height:42px;border-radius:10px;background:#FEE2E2;display:flex;align-items:center;justify-content:center;flex:none;}
.dc-doc .ico.docx{background:#DBEAFE}.dc-doc .ico.txt{background:#F1F5F9}.dc-doc .ico.img{background:#DCFCE7}
.dc-doc .nm{font-weight:600;color:var(--navy);font-size:.95rem;}
.dc-doc .meta{color:var(--muted);font-size:.8rem;}
.dc-feature{text-align:center;padding:.4rem .6rem;}
.dc-feature .ic{width:46px;height:46px;border-radius:50%;background:var(--soft);display:flex;align-items:center;justify-content:center;margin:0 auto .7rem auto;}
.dc-feature b{display:block;color:var(--navy);font-size:.95rem;margin-bottom:.2rem;}
.dc-feature span{color:var(--muted);font-size:.82rem;}
.dc-metric{border-radius:14px;padding:1rem 1.1rem;display:flex;align-items:center;gap:.9rem;border:1px solid rgba(15,23,42,.05);}
.dc-metric .v{font-size:1.7rem;font-weight:800;line-height:1.1;}.dc-metric .l{font-size:.78rem;color:var(--muted);font-weight:500;}
.dc-metric .ic{width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,.8);display:flex;align-items:center;justify-content:center;flex:none;}
.dc-action-head{border-radius:12px;padding:1.1rem;color:#fff;text-align:center;font-weight:700;font-size:1.1rem;margin-bottom:1rem;}
.dc-action-head svg{display:block;margin:0 auto .4rem auto;}
.dc-list{list-style:none;padding:0;margin:.3rem 0 .5rem 0;}
.dc-list li{font-size:.85rem;color:#475569;padding:.22rem 0;display:flex;gap:.5rem;align-items:center;}
.dc-pill{display:inline-block;background:var(--soft);color:var(--primary);border-radius:6px;padding:.18rem .6rem;font-size:.78rem;font-weight:500;margin:0 .3rem .3rem 0;}
.dc-badge{display:inline-block;border-radius:6px;padding:.15rem .6rem;font-size:.74rem;font-weight:600;}
.b-green{background:#D1FAE5;color:#047857}.b-orange{background:#FEF3C7;color:#B45309}.b-red{background:#FEE2E2;color:#B91C1C}
.b-blue{background:#DBEAFE;color:#1D4ED8}.b-gray{background:#F1F5F9;color:#475569}.b-purple{background:var(--soft);color:var(--primary)}
.dc-table{width:100%;border-collapse:collapse;font-size:.85rem;}
.dc-table th{text-align:left;color:var(--muted);font-weight:600;font-size:.76rem;padding:.6rem .7rem;border-bottom:1px solid var(--border);background:#F8FAFC;}
.dc-table td{padding:.65rem .7rem;border-bottom:1px solid #F1F5F9;color:var(--navy);vertical-align:top;}
.dc-table tr:last-child td{border-bottom:none}
.dc-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:12px;background:#fff;}
.dc-hero h1{font-size:3.4rem;font-weight:800;color:#312E81;margin:0 0 .4rem 0;letter-spacing:-0.03em;line-height:1.05;}
.dc-hero h2{font-size:1.45rem;font-weight:600;color:var(--navy);margin:0 0 1.1rem 0;}
.dc-hero p{color:#475569;font-size:1rem;line-height:1.65;max-width:480px;margin-bottom:1.4rem;}
.dc-nav-logo{display:flex;align-items:center;gap:.6rem;font-weight:800;color:var(--navy);font-size:1.1rem;padding-top:.3rem;}
.dc-entity{display:flex;justify-content:space-between;align-items:center;padding:.5rem .7rem;border:1px solid var(--border);border-radius:9px;margin-bottom:.45rem;font-size:.85rem;background:#fff;}
.dc-ins{border-left:4px solid var(--primary);background:#fff;border-radius:10px;padding:.75rem 1rem;margin-bottom:.6rem;border-top:1px solid var(--border);border-right:1px solid var(--border);border-bottom:1px solid var(--border);}
.dc-ins.ok{border-left-color:var(--green)}.dc-ins.warn{border-left-color:var(--orange)}
.dc-ins b{display:block;font-size:.88rem}.dc-ins span{font-size:.84rem;color:#475569}
.dc-empty{text-align:center;padding:2.6rem 1rem;background:#fff;border:1px dashed #C7D2FE;border-radius:14px;color:var(--muted);}
.dc-empty b{display:block;color:var(--navy);font-size:1.05rem;margin:.6rem 0 .2rem 0}
.dc-ok{display:flex;align-items:center;gap:.8rem;font-weight:700;font-size:1.25rem;color:var(--navy);margin-bottom:1rem;}
.dc-ok .c{width:38px;height:38px;border-radius:50%;background:var(--green);display:flex;align-items:center;justify-content:center;}
.dc-vs{display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.3rem;color:var(--navy);height:100%;min-height:120px;}
/* ---------- upload ---------- */
[data-testid="stFileUploaderDropzone"]{border:2px dashed #A5B4FC;border-radius:14px;background:#F5F7FF;padding:2.2rem 1rem;flex-direction:column-reverse!important;align-items:center!important;justify-content:center;gap:.9rem;}
[data-testid="stFileUploaderDropzoneInstructions"]{flex-direction:column;align-items:center;}
[data-testid="stFileUploaderDropzoneInstructions"] > div{display:none;}
[data-testid="stFileUploaderDropzoneInstructions"]::before{content:"Drag and drop your file here\A or";white-space:pre;text-align:center;font-weight:600;color:var(--navy);font-size:.95rem;
 line-height:1.6;padding-top:52px;font-family:Inter,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 24 24' fill='none' stroke='%234F46E5' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'><polyline points='16 16 12 12 8 16'/><line x1='12' y1='12' x2='12' y2='21'/><path d='M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3'/></svg>") no-repeat top center;}
[data-testid="stFileUploaderDropzone"]:has([data-testid="stFileUploaderDropzoneInstructions"]) button{background:var(--primary);color:#fff;border:none;border-radius:9px;font-weight:600;padding:.5rem 1.6rem;}
[data-testid="stFileUploaderDropzone"]:has([data-testid="stFileUploaderDropzoneInstructions"]) button:hover{background:#4338CA;color:#fff;}
.st-key-up_multi [data-testid="stFileUploaderDropzone"],.st-key-up_small [data-testid="stFileUploaderDropzone"]{padding:1.4rem 1rem;}
[data-testid="stFileUploaderFile"]{background:#fff;border-radius:10px;}
/* ---------- tabs, inputs ---------- */
.stTabs [data-baseweb="tab-list"]{gap:1.6rem;border-bottom:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{padding:.6rem .1rem;color:var(--muted);font-weight:500;font-size:.9rem;background:transparent;}
.stTabs [aria-selected="true"]{color:var(--primary)!important;font-weight:600;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--primary);height:2px;}
.stTextInput input,.stTextArea textarea,.stSelectbox [data-baseweb="select"]>div{border-radius:10px;border-color:var(--border);background:#fff;}
[data-testid="stChatInput"]{border-radius:12px;border:1px solid var(--border);background:#fff;}
[data-testid="stChatMessage"]{background:#fff;border:1px solid var(--border);border-radius:14px;padding:.8rem 1rem;}
[data-testid="stAlert"]{border-radius:12px;}
[data-testid="stDialog"] div[role="dialog"]{border-radius:16px;}
[data-testid="stMetricValue"]{font-weight:700;color:var(--navy);font-family:Inter,"Segoe UI",Roboto,Arial,sans-serif;}
[data-testid="stMetricLabel"]{color:var(--muted);}
.stSpinner{color:var(--primary);}
@media (max-width:900px){
 .block-container{padding:1rem 1rem 2rem 1rem;}
 .dc-hero h1{font-size:2.5rem}.dc-title{font-size:1.5rem}
 [data-testid="stHorizontalBlock"]{flex-wrap:wrap;gap:.8rem;}
 [data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{min-width:calc(50% - 1rem);}
}
@media (max-width:640px){[data-testid="stHorizontalBlock"]>[data-testid="stColumn"]{min-width:100%;}}
</style>
"""

HIDE_SIDEBAR = """<style>[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],[data-testid="stExpandSidebarButton"]{display:none!important;}
.block-container{max-width:1180px;}</style>"""


def inject(hide_sidebar: bool = False):
    st.markdown(CSS, unsafe_allow_html=True)
    if hide_sidebar:
        st.markdown(HIDE_SIDEBAR, unsafe_allow_html=True)
