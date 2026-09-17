"""Shared cinematic navy/black glassmorphism theme."""
import base64
import os
import streamlit as st

MAIN_COLOR = "#5E8CFF"
ACCENT_COLOR = "#28D7FF"
PINK_COLOR = "#C55CFF"
GREEN_COLOR = "#32E6A8"
YELLOW_COLOR = "#FFC857"
PLOT_BG = "rgba(3,10,24,0.0)"
PAPER_BG = "rgba(0,0,0,0)"
TEXT_COLOR = "#F5F8FF"
COLOR_SEQUENCE = [MAIN_COLOR, "#8B5CFF", PINK_COLOR, ACCENT_COLOR, GREEN_COLOR, YELLOW_COLOR]

PLOTLY_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(family="Inter, Arial", color=TEXT_COLOR, size=12),
    title_font=dict(size=17, color="#FFFFFF"),
    margin=dict(l=42, r=18, t=48, b=38),
    hoverlabel=dict(bgcolor="#0A1630", font_color="#FFFFFF", font_size=12),
    xaxis=dict(gridcolor="rgba(130,170,255,.08)", zerolinecolor="rgba(130,170,255,.12)", color="#AFC0DD"),
    yaxis=dict(gridcolor="rgba(130,170,255,.08)", zerolinecolor="rgba(130,170,255,.12)", color="#AFC0DD"),
)

_ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

@st.cache_data(show_spinner=False)
def get_base64_image(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Asset not found: {path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def apply_page_style(page_title: str, page_icon: str = "🚗", layout: str = "wide"):
    st.set_page_config(
        page_title=f"{page_title} | Car Price Prediction",
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="collapsed",
    )
    _inject_css()

def _inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {{ --bg:#01040C; --navy:#061329; --blue:#5E8CFF; --cyan:#28D7FF; --purple:#B76CFF; }}
    html, body, [class*="css"] {{ font-family:'Inter',sans-serif; }}
    .stApp {{
      background:
        radial-gradient(circle at 55% 6%, rgba(44,85,160,.20), transparent 34%),
        radial-gradient(circle at 8% 44%, rgba(22,54,112,.14), transparent 34%),
        linear-gradient(145deg,#01030A 0%,#030916 48%,#000207 100%);
      color:{TEXT_COLOR};
    }}
    .stApp::before {{
      content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.45;
      background-image:
        radial-gradient(circle at 7% 12%,rgba(255,255,255,.9) 0 1px,transparent 1.7px),
        radial-gradient(circle at 18% 68%,rgba(255,255,255,.8) 0 1px,transparent 1.8px),
        radial-gradient(circle at 31% 23%,rgba(255,255,255,.75) 0 1px,transparent 1.7px),
        radial-gradient(circle at 43% 82%,rgba(255,255,255,.7) 0 1px,transparent 1.7px),
        radial-gradient(circle at 57% 11%,rgba(255,255,255,.9) 0 1px,transparent 1.8px),
        radial-gradient(circle at 68% 63%,rgba(255,255,255,.8) 0 1px,transparent 1.8px),
        radial-gradient(circle at 79% 19%,rgba(255,255,255,.75) 0 1px,transparent 1.7px),
        radial-gradient(circle at 91% 76%,rgba(255,255,255,.8) 0 1px,transparent 1.8px),
        radial-gradient(circle at 96% 31%,rgba(255,255,255,.7) 0 1px,transparent 1.6px);
    }}
    .main,.block-container,section[data-testid="stSidebar"] {{ position:relative; z-index:1; }}
    .block-container {{ max-width:1540px; padding-top:.7rem; padding-bottom:3rem; }}
    #MainMenu,footer {{ visibility:hidden; }}
    h1,h2,h3,h4 {{ color:#fff !important; font-weight:750 !important; }}
    .section-caption {{ color:#93A4BF; font-size:.9rem; margin-top:-8px; margin-bottom:1rem; }}
    hr {{ border-color:rgba(126,167,255,.10) !important; }}


    /* Home reference design: cinematic hero + neon glass cards */
    .home-hero {{ position:relative; height:470px; margin:4px -2vw 0; overflow:hidden; border-top:1px solid rgba(91,143,255,.08); border-bottom:1px solid rgba(80,140,255,.24); background:#010611; }}
    .home-hero-bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center 48%; filter:brightness(.55) saturate(1.18) contrast(1.08); transform:scale(1.015); }}
    .home-hero-overlay {{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(1,5,16,.97) 0%,rgba(1,7,20,.84) 24%,rgba(1,6,17,.42) 49%,rgba(1,4,12,.05) 77%,rgba(1,3,9,.24) 100%),linear-gradient(0deg,rgba(1,4,13,.82) 0%,transparent 38%,rgba(1,4,13,.12) 100%); }}
    .home-hero-content {{ position:absolute; left:5.2%; top:62px; z-index:2; max-width:570px; }}
    .home-hero-content h1 {{ margin:18px 0 12px !important; font-size:3.35rem !important; line-height:1.05 !important; letter-spacing:-1.8px; text-shadow:0 8px 34px rgba(0,0,0,.5); }}
    .home-hero-content h1 span {{ color:#75A2FF; text-shadow:0 0 26px rgba(66,118,255,.28); }}
    .home-hero-content p {{ color:#CBD8F0; font-size:1rem; line-height:1.7; margin:0; }}
    .hero-badge {{ display:inline-flex; align-items:center; gap:7px; padding:8px 14px; border:1px solid rgba(90,147,255,.46); border-radius:999px; color:#BCD2FF; background:rgba(2,12,29,.45); box-shadow:0 0 24px rgba(47,108,255,.10), inset 0 1px 0 rgba(255,255,255,.05); font-size:.72rem; backdrop-filter:blur(9px); }}
    .badge-dot {{ width:8px; height:8px; border-radius:50%; background:#32D8FF; box-shadow:0 0 13px #32D8FF; animation:iconBlink 1.7s ease-in-out infinite; }}
    .shortcut-grid {{ position:relative; z-index:4; display:grid; grid-template-columns:repeat(4,1fr); gap:24px; margin:-38px 2.5% 0; }}
    .home-shortcut {{ min-height:96px; display:flex; align-items:center; gap:17px; padding:17px 22px; color:#fff !important; text-decoration:none !important; border:1px solid rgba(75,137,255,.50); border-radius:17px; background:linear-gradient(135deg,rgba(5,20,45,.78),rgba(3,9,22,.63)); box-shadow:0 18px 48px rgba(0,0,0,.62),0 0 24px rgba(48,103,255,.10),inset 0 1px 0 rgba(255,255,255,.06); backdrop-filter:blur(17px); transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease,background .22s ease; }}
    .home-shortcut:hover {{ transform:translateY(-5px); border-color:rgba(95,157,255,.92); background:linear-gradient(135deg,rgba(10,30,68,.86),rgba(5,13,31,.72)); box-shadow:0 22px 56px rgba(0,0,0,.72),0 0 35px rgba(48,112,255,.26),inset 0 1px 0 rgba(255,255,255,.09); }}
    .shortcut-icon {{ width:52px; height:52px; display:grid; place-items:center; flex:0 0 52px; font-size:2rem; filter:drop-shadow(0 0 12px rgba(67,139,255,.72)); animation:iconBlink 2.4s ease-in-out infinite; }}
    .home-shortcut:nth-child(2) .shortcut-icon {{ filter:drop-shadow(0 0 13px rgba(40,215,255,.78)); animation-delay:.35s; }}
    .home-shortcut:nth-child(3) .shortcut-icon {{ filter:drop-shadow(0 0 13px rgba(197,92,255,.75)); animation-delay:.7s; }}
    .home-shortcut:nth-child(4) .shortcut-icon {{ filter:drop-shadow(0 0 13px rgba(139,92,255,.82)); animation-delay:1.05s; }}
    .shortcut-copy {{ display:flex; flex-direction:column; min-width:0; }}
    .shortcut-copy strong {{ font-size:.94rem; font-weight:650; color:#F5F8FF; }}
    .shortcut-copy small {{ margin-top:4px; color:#9EB0CF; font-size:.76rem; }}
    .shortcut-arrow {{ margin-left:auto; font-size:1.5rem; color:#EAF2FF; text-shadow:0 0 14px rgba(120,165,255,.65); }}
    @keyframes iconBlink {{ 0%,100% {{ opacity:.72; transform:scale(.98); }} 45% {{ opacity:1; transform:scale(1.06); }} 55% {{ opacity:.82; }} }}
    .kpi-head {{ margin:20px 2.5% 12px !important; }}
    .kpi-title-icon {{ color:#71A5FF; text-shadow:0 0 14px rgba(71,132,255,.75); }}
    .kpi-card-title {{ color:#C5D4EF; font-size:.77rem; font-weight:550; margin:1px 4px 4px; }}
    .kpi-value {{ color:#F7FAFF; font-size:1.78rem; font-weight:750; letter-spacing:.2px; margin:2px 4px; text-shadow:0 0 20px rgba(94,140,255,.20); }}
    .kpi-delta {{ color:#31E4A7; font-size:.68rem; margin:0 4px 2px; }}
    @media (max-width: 900px) {{ .shortcut-grid {{ grid-template-columns:repeat(2,1fr); }} .home-hero-content h1 {{ font-size:2.5rem !important; }} }}
    @media (max-width: 600px) {{ .shortcut-grid {{ grid-template-columns:1fr; margin-top:-18px; }} .home-hero {{ height:540px; }} .home-hero-content {{ left:7%; right:7%; top:45px; }} .desktop-break {{ display:none; }} }}

    /* Reference-style top navigation */
    .topbar {{ display:flex; align-items:center; gap:22px; justify-content:space-between; padding:10px 4px 14px; margin-bottom:0; border-bottom:1px solid rgba(115,154,235,.14); }}
    .brand {{ display:flex; align-items:center; gap:11px; color:#fff; font-size:1.08rem; font-weight:750; white-space:nowrap; text-shadow:0 0 18px rgba(94,140,255,.16); }}
    .brand-icon {{ font-size:1.65rem; filter:drop-shadow(0 0 9px rgba(94,140,255,.85)); }}
    .topnav {{ display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap; flex:1; }}
    .topnav .nav-link {{ display:inline-flex; align-items:center; gap:8px; padding:10px 17px; border:1px solid transparent; border-radius:999px; color:#D9E4FA; text-decoration:none; font-size:.82rem; transition:.22s ease; }}
    .topnav .nav-link:hover {{ border-color:rgba(94,140,255,.38); background:rgba(45,88,175,.12); box-shadow:0 0 24px rgba(61,112,255,.16); color:#fff; }}
    .topnav .nav-link.active {{ border-color:rgba(94,140,255,.48); background:linear-gradient(135deg,rgba(43,86,180,.22),rgba(94,140,255,.06)); box-shadow:0 0 28px rgba(61,112,255,.18), inset 0 1px 0 rgba(255,255,255,.04); color:#fff; }}
    .dark-pill {{ color:#DDE7FF; padding:9px 14px; border:1px solid rgba(126,167,255,.15); border-radius:999px; background:rgba(5,12,25,.38); white-space:nowrap; font-size:.8rem; }}

    /* Hero */
    .hero-reference {{ position:relative; min-height:435px; overflow:hidden; border-bottom:1px solid rgba(110,157,255,.18); margin:0 -2vw; padding:0 2vw; }}
    .hero-reference .hero-bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:center 52%; filter:brightness(.58) saturate(1.04); transform:scale(1.02); }}
    .hero-reference::after {{ content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(1,4,12,.97) 0%,rgba(1,5,15,.83) 29%,rgba(1,5,15,.35) 53%,rgba(1,3,10,.10) 100%),linear-gradient(0deg,rgba(1,4,12,.84) 0%,transparent 48%,rgba(1,4,12,.22) 100%); }}
    .hero-content {{ position:relative; z-index:2; padding:65px 34px 30px; max-width:620px; }}
    .hero-badge {{ display:inline-block; padding:7px 12px; border:1px solid rgba(94,140,255,.38); border-radius:999px; color:#B8CAFF; background:rgba(5,16,36,.45); box-shadow:0 0 22px rgba(60,111,255,.10); font-size:.72rem; letter-spacing:.03em; }}
    .hero-title {{ margin:17px 0 12px; font-size:clamp(2.6rem,5vw,4.3rem); line-height:1.02; letter-spacing:-.035em; color:#fff; text-shadow:0 8px 35px rgba(0,0,0,.75); }}
    .hero-title span {{ color:#6E91FF; text-shadow:0 0 28px rgba(75,111,255,.36); }}
    .hero-copy {{ color:#C1CEE2; font-size:.98rem; line-height:1.62; max-width:500px; }}

    /* Page shortcut cards */
    .shortcut-card {{ min-height:76px; padding:14px 17px; border-radius:17px; border:1px solid rgba(102,151,255,.28); background:linear-gradient(135deg,rgba(5,17,38,.64),rgba(5,10,22,.40)); box-shadow:0 15px 38px rgba(0,0,0,.44), inset 0 1px 0 rgba(255,255,255,.035); backdrop-filter:blur(15px); transition:.22s ease; }}
    .shortcut-card:hover {{ transform:translateY(-3px); border-color:rgba(94,140,255,.60); box-shadow:0 20px 50px rgba(0,0,0,.55),0 0 34px rgba(55,113,255,.16); }}
    .shortcut-icon {{ font-size:1.65rem; margin-right:10px; filter:drop-shadow(0 0 9px rgba(94,140,255,.75)); animation:iconBlink 2.8s ease-in-out infinite; }}
    .shortcut-card:nth-child(2) .shortcut-icon {{ animation-delay:.35s; }}
    .shortcut-card:nth-child(3) .shortcut-icon {{ animation-delay:.7s; }}
    .shortcut-card:nth-child(4) .shortcut-icon {{ animation-delay:1.05s; }}
    @keyframes iconBlink {{ 0%,100% {{ opacity:1; filter:drop-shadow(0 0 6px rgba(94,140,255,.48)); }} 50% {{ opacity:.62; filter:drop-shadow(0 0 17px rgba(80,160,255,1)); }} }}
    .shortcut-title {{ color:#F8FAFF; font-size:.95rem; font-weight:650; }}
    .shortcut-sub {{ color:#92A5C1; font-size:.74rem; margin-top:3px; }}
    .shortcut-arrow {{ margin-left:auto; color:#D9E7FF; font-size:1.25rem; }}
    div[class*="st-key-shortcut_"] {{ background:linear-gradient(135deg,rgba(5,17,38,.70),rgba(3,8,19,.52)) !important; border:1px solid rgba(102,151,255,.28) !important; border-radius:17px !important; padding:0 !important; overflow:hidden; box-shadow:0 15px 38px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.035) !important; backdrop-filter:blur(15px); }}
    div[class*="st-key-shortcut_"] .stButton > button {{ min-height:88px !important; border:0 !important; border-radius:16px !important; background:transparent !important; text-align:left !important; box-shadow:none !important; white-space:pre-line !important; font-size:.92rem !important; font-weight:650 !important; line-height:1.55 !important; transition:transform .22s ease, box-shadow .22s ease, background .22s ease !important; animation:cardGlow 3.2s ease-in-out infinite; }}
    div[class*="st-key-shortcut_"] .stButton > button:hover {{ transform:translateY(-2px) !important; background:rgba(55,107,220,.10) !important; box-shadow:0 0 30px rgba(67,125,255,.20) !important; }}
    @keyframes cardGlow {{ 0%,100% {{ box-shadow:inset 0 1px 0 rgba(255,255,255,.035), 0 0 0 rgba(70,130,255,0); }} 50% {{ box-shadow:inset 0 1px 0 rgba(255,255,255,.055), 0 0 22px rgba(70,130,255,.13); }} }}

    /* KPI section */
    .kpi-head {{ display:flex; align-items:center; justify-content:space-between; margin:18px 0 12px; }}
    .kpi-title {{ color:#F4F7FF; font-size:1.05rem; font-weight:700; }}
    .live {{ border:1px solid rgba(94,140,255,.24); border-radius:999px; padding:5px 10px; color:#BBD0FF; font-size:.68rem; background:rgba(5,17,34,.48); }}
    .live-dot {{ display:inline-block; width:7px; height:7px; border-radius:50%; background:#2FE5A7; box-shadow:0 0 11px #2FE5A7; margin-right:6px; animation:livePulse 1.6s infinite; }}
    @keyframes livePulse {{ 50% {{ opacity:.35; transform:scale(.78); }} }}
    div[class*="st-key-home_kpi_"] {{ background:linear-gradient(145deg,rgba(7,21,43,.82),rgba(2,8,18,.90)) !important; border:1px solid rgba(102,151,255,.20) !important; border-radius:18px !important; padding:12px 13px 4px !important; box-shadow:0 20px 52px rgba(0,0,0,.48),0 0 26px rgba(37,91,182,.07),inset 0 1px 0 rgba(255,255,255,.035) !important; backdrop-filter:blur(14px); }}
    div[class*="st-key-chart_"] {{ background:linear-gradient(145deg,rgba(7,21,43,.86),rgba(2,8,18,.92)) !important; border:1px solid rgba(102,151,255,.20) !important; border-radius:20px !important; padding:7px 9px 1px !important; box-shadow:0 22px 58px rgba(0,0,0,.50),0 0 34px rgba(37,91,182,.08),inset 0 1px 0 rgba(255,255,255,.035) !important; }}
    div[data-testid="stMetric"] {{ background:transparent !important; border:0 !important; padding:5px 5px 3px !important; box-shadow:none !important; }}
    div[data-testid="stMetricLabel"] {{ color:#93A7C4 !important; font-size:.73rem !important; }}
    div[data-testid="stMetricValue"] {{ color:#F5F8FF !important; font-size:1.7rem !important; text-shadow:0 0 18px rgba(77,130,255,.16); }}
    div[data-testid="stMetricDelta"] {{ color:#36E5A9 !important; }}

    /* All charts */
    div[data-testid="stPlotlyChart"] {{ border-radius:16px; overflow:hidden; filter:drop-shadow(0 9px 17px rgba(0,0,0,.16)); }}

    /* Page content glass */
    div[class*="st-key-glasscard_"] {{ background:linear-gradient(145deg,rgba(7,21,43,.78),rgba(2,8,18,.9)) !important; border:1px solid rgba(102,151,255,.17) !important; border-radius:18px !important; padding:16px 18px !important; box-shadow:0 18px 50px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,255,255,.025) !important; }}
    div[data-baseweb="select"] > div, input, textarea {{ background:rgba(4,13,29,.88) !important; color:#fff !important; border-color:rgba(126,167,255,.20) !important; }}
    .stButton > button, div[data-testid="stFormSubmitButton"] button {{ border-radius:12px !important; border:1px solid rgba(102,151,255,.30) !important; background:linear-gradient(135deg,rgba(52,100,220,.20),rgba(168,86,255,.10)) !important; color:#fff !important; box-shadow:0 10px 28px rgba(0,0,0,.28); }}
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {{ border-color:#78A4FF !important; box-shadow:0 0 30px rgba(77,124,254,.24); }}
    section[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#031020,#01040B) !important; border-right:1px solid rgba(126,167,255,.10); }}
    section[data-testid="stSidebar"] * {{ color:#EAF0FF !important; }}

    /* Final Home viewport tuning: keep the complete navigation visible and
       remove Streamlit's fixed header from the visual composition. */
    header[data-testid="stHeader"] {{ height:0 !important; min-height:0 !important; background:transparent !important; }}
    header[data-testid="stHeader"] * {{ visibility:hidden !important; }}
    div[data-testid="stToolbar"] {{ display:none !important; }}
    .block-container {{ max-width:1540px !important; padding-top:0 !important; padding-left:2rem !important; padding-right:2rem !important; }}
    .topbar {{ min-height:62px; padding:7px 10px 10px; margin:0 0 0; position:relative; z-index:20; background:linear-gradient(180deg,rgba(1,5,16,.94),rgba(1,5,16,.70)); box-shadow:0 10px 35px rgba(0,0,0,.35); }}
    .home-hero {{ height:430px !important; margin:0 -2rem !important; border-radius:0 !important; }}
    .home-hero-bg {{ object-position:center 50% !important; filter:brightness(.48) saturate(1.20) contrast(1.10) !important; }}
    .home-hero-overlay {{ background:linear-gradient(90deg,rgba(0,3,12,.96) 0%,rgba(1,5,16,.78) 30%,rgba(1,5,16,.30) 54%,rgba(0,2,9,.08) 100%),linear-gradient(0deg,rgba(0,3,12,.86) 0%,transparent 50%,rgba(0,3,12,.16) 100%) !important; }}
    .home-hero-content {{ left:4.1% !important; top:54px !important; max-width:620px !important; }}
    .home-hero-content h1 {{ font-size:3.35rem !important; }}
    .shortcut-grid {{ margin:-42px 2.5% 0 !important; gap:16px !important; grid-template-columns:repeat(5,1fr) !important; }}
    .home-shortcut {{ min-height:94px !important; padding:15px 16px !important; gap:12px !important; }}
    .home-shortcut:nth-child(5) .shortcut-icon {{ filter:drop-shadow(0 0 13px rgba(50,230,168,.78)); animation-delay:1.4s; }}
    .shortcut-grid .shortcut-icon {{ width:44px !important; height:44px !important; flex:0 0 44px !important; font-size:1.7rem !important; }}
    @media (max-width:1250px) {{ .shortcut-grid {{ grid-template-columns:repeat(3,1fr) !important; }} }}
    @media (max-width:900px) {{ .shortcut-grid {{ grid-template-columns:repeat(2,1fr) !important; }} }}
    @media (max-width:600px) {{ .shortcut-grid {{ grid-template-columns:1fr !important; }} }}
    .kpi-head {{ margin:20px 2.5% 10px !important; }}
    div[class*="st-key-home_kpi_"] {{ min-height:220px !important; }}
    div[data-testid="stPlotlyChart"] {{ filter:drop-shadow(0 13px 28px rgba(30,85,190,.16)); }}
    .topbar-spacer {{ height:16px; }}
    .topnav .nav-link {{ white-space:nowrap; }}
    @media (max-width:1400px) {{ .topnav {{ gap:4px; }} .topnav .nav-link {{ padding:9px 12px; font-size:.78rem; }} }}
    @media (max-width:1150px) {{ .topbar {{ flex-wrap:wrap; }} .dark-pill {{ display:none; }} .topnav {{ justify-content:flex-start; }} }}
    @media (max-width:900px) {{ .topbar {{ gap:8px; }} .brand {{ font-size:.9rem; }} .topnav .nav-link {{ padding:8px 9px; font-size:.7rem; }} .home-hero {{ height:470px !important; }} }}
    </style>
    """, unsafe_allow_html=True)
    st.markdown(_NEON_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Shared top navigation
# ---------------------------------------------------------------------------
# IMPORTANT: Streamlit strips the numeric ordering prefix from files inside
# `pages/`, so `pages/1_KPI_Overview.py` is served at `/KPI_Overview` — NOT at
# `/1_KPI_Overview`. Linking to the file name with its number is what produced
# the "Page not found" errors.
#
# The hrefs below are RELATIVE (no leading slash) on purpose: from `/` they
# resolve to `/KPI_Overview`, and from `/Car_Analysis` they resolve to
# `/KPI_Overview` as well. That keeps the links working locally, on Streamlit
# Community Cloud, and behind a sub-path reverse proxy.
ICON_PATHS = {
    "home": '<path d="M3.2 9.8 12 3l8.8 6.8V20a1 1 0 0 1-1 1h-4.6v-6.6H8.8V21H4.2a1 1 0 0 1-1-1z"/>',
    "bars": '<path d="M4 20h16"/><path d="M7.5 20v-6.5M12 20V5.5M16.5 20v-9.5"/>',
    "brain": '<path d="M12 6a3 3 0 0 0-3-3 2.6 2.6 0 0 0-2.5 1.8A2.8 2.8 0 0 0 4.2 9a2.9 2.9 0 0 0 .6 4.6A2.8 2.8 0 0 0 6 18.6 2.7 2.7 0 0 0 9 21a3 3 0 0 0 3-3z"/><path d="M12 6a3 3 0 0 1 3-3 2.6 2.6 0 0 1 2.5 1.8A2.8 2.8 0 0 1 19.8 9a2.9 2.9 0 0 1-.6 4.6A2.8 2.8 0 0 1 18 18.6 2.7 2.7 0 0 1 15 21a3 3 0 0 1-3-3"/>',
    "doc": '<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5"/><path d="M8.8 12.8h6.4M8.8 16.2h4.4"/>',
    "nodes": '<circle cx="18" cy="5.2" r="2.4"/><circle cx="6" cy="12" r="2.4"/><circle cx="18" cy="18.8" r="2.4"/><path d="M8.2 10.9 15.8 6.4M8.2 13.1l7.6 4.5"/>',
    "list": '<rect x="4.8" y="4.2" width="14.4" height="16.6" rx="2.4"/><path d="M9.2 4.2h5.6v2.9H9.2z"/><path d="M8.6 11.2h6.8M8.6 15.2h4.6"/>',
    "car": '<path d="M5.1 11.2 6.7 6.9A2.1 2.1 0 0 1 8.7 5.5h6.6a2.1 2.1 0 0 1 2 1.4l1.6 4.3"/><rect x="3" y="11.2" width="18" height="6.1" rx="1.6"/><circle cx="7.6" cy="14.3" r="1.15"/><circle cx="16.4" cy="14.3" r="1.15"/><path d="M6 17.3v1.6M18 17.3v1.6"/>',
    "moon": '<path d="M20.2 14.6A8.6 8.6 0 0 1 9.4 3.8a8.6 8.6 0 1 0 10.8 10.8z"/>',
    "coins": '<ellipse cx="12" cy="6.8" rx="7" ry="3"/><path d="M5 6.8v4.9c0 1.7 3.1 3 7 3s7-1.3 7-3V6.8"/><path d="M5 11.7v5c0 1.7 3.1 3 7 3s7-1.3 7-3v-5"/>',
    "drop": '<path d="M12 3.2c3.3 3.6 5.9 6.9 5.9 9.7a5.9 5.9 0 1 1-11.8 0c0-2.8 2.6-6.1 5.9-9.7z"/>',
    "star": '<path d="m12 3.6 2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.7-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z"/>',
    "arrow": '<path d="M4.8 12h13.4M13 6.6l5.4 5.4-5.4 5.4"/>',
}


def icon(name: str, size: int = 22, cls: str = "ico") -> str:
    """Inline neon line-icon. Colour is inherited from CSS `color`."""
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" '
        'fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round">'
        f'{ICON_PATHS.get(name, "")}</svg>'
    )


# ---------------------------------------------------------------------------
# Shared top navigation
# ---------------------------------------------------------------------------
# Streamlit strips the numeric ordering prefix from files inside `pages/`, so
# `pages/1_KPI_Overview.py` is served at `/KPI_Overview` — NOT `/1_KPI_Overview`.
# Hrefs are relative (no leading slash) so they resolve correctly from any page
# and behind a sub-path reverse proxy.
NAV_ITEMS = [
    ("home", "Home", "./"),
    ("bars", "EDA", "KPI_Overview"),
    ("car", "Car Analysis", "Car_Analysis"),
    ("list", "Description", "Data_Description"),
    ("brain", "Predict Price", "Predict_Price"),
    ("doc", "Report", "Report"),
    ("nodes", "ML Models", "ML_Models"),
]


def render_topbar(active: str = "Home", spacer: bool = True):
    """Render the glass top navigation. Called on every page.

    `active` matches a label in NAV_ITEMS ("Home", "EDA", "Car Analysis",
    "Description", "Predict Price", "Report", "ML Models").
    """
    links = "".join(
        f'<a class="nav-link{" active" if label == active else ""}" href="{href}" '
        f'target="_self">{icon(name, 20)}<span>{label}</span></a>'
        for name, label, href in NAV_ITEMS
    )
    st.markdown(
        f"""<div class="topbar">
  <div class="brand"><span class="brand-mark">{icon("car", 24)}</span><span>Car Price Prediction</span></div>
  <nav class="topnav">{links}</nav>
  <div class="dark-pill">{icon("moon", 18)}<span>Dark Mode</span></div>
</div>""",
        unsafe_allow_html=True,
    )
    if spacer:
        st.markdown('<div class="topbar-spacer"></div>', unsafe_allow_html=True)


def hero_banner(title: str, subtitle: str, badge: str = "CAR SALES INTELLIGENCE"):
    img_b64 = get_base64_image("reference_car.jpg")
    st.markdown(f"""
    <div class="hero-reference">
      <img class="hero-bg" src="data:image/jpeg;base64,{img_b64}" />
      <div class="hero-content"><span class="hero-badge">{badge}</span><div class="hero-title">{title}</div><div class="hero-copy">{subtitle}</div></div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Neon reference skin (plain string: no f-string brace doubling needed)
# ---------------------------------------------------------------------------
_NEON_CSS = """
<style>
:root{
  --neon-blue:#4C8DFF; --neon-cyan:#35D9F5; --neon-violet:#A66BFF;
  --neon-pink:#F05CC8; --neon-mint:#3FE0B0;
  --ink:#F3F7FF; --ink-dim:#93A3C4;
  --glass:linear-gradient(150deg,rgba(18,26,58,.62),rgba(6,9,24,.48));
  --edge:rgba(116,158,255,.30);
}
.stApp{
  background:
    radial-gradient(900px 480px at 68% -8%, rgba(94,60,190,.26), transparent 62%),
    radial-gradient(760px 420px at 6% 34%, rgba(26,70,168,.20), transparent 60%),
    linear-gradient(160deg,#04050E 0%,#07091A 46%,#02030A 100%);
}
.ico{flex:0 0 auto;overflow:visible}

/* ---------- top bar ---------- */
.topbar{
  display:flex;align-items:center;gap:20px;justify-content:space-between;
  min-height:70px;padding:11px 8px;margin:0 -1rem;position:relative;z-index:30;
  background:linear-gradient(180deg,rgba(4,6,18,.96),rgba(4,6,18,.72));
  border-bottom:1px solid rgba(110,150,255,.16);box-shadow:0 12px 38px rgba(0,0,0,.42);
}
.brand{display:flex;align-items:center;gap:13px;color:#fff;font-size:1.12rem;font-weight:700;letter-spacing:-.2px;white-space:nowrap}
.brand-mark{
  display:grid;place-items:center;width:42px;height:42px;border-radius:13px;color:var(--neon-cyan);
  border:1px solid rgba(76,141,255,.42);background:linear-gradient(145deg,rgba(28,48,112,.55),rgba(8,12,32,.55));
  filter:drop-shadow(0 0 10px rgba(53,217,245,.55));
}
.topnav{display:flex;align-items:center;justify-content:center;gap:6px;flex:1;flex-wrap:wrap}
.topnav .nav-link{
  position:relative;display:inline-flex;align-items:center;gap:9px;padding:11px 17px;
  border:1px solid transparent;border-radius:14px;color:#C6D4F0 !important;
  text-decoration:none !important;font-size:.9rem;font-weight:500;white-space:nowrap;
  transition:color .18s ease,border-color .18s ease,background .18s ease;
}
.topnav .nav-link .ico{color:var(--neon-blue);transition:color .18s ease,filter .18s ease}
.topnav .nav-link:hover{color:#fff !important;border-color:rgba(108,150,255,.32);background:rgba(34,58,128,.20)}
.topnav .nav-link:hover .ico{color:var(--neon-cyan);filter:drop-shadow(0 0 8px rgba(53,217,245,.6))}
.topnav .nav-link.active{
  color:#fff !important;border-color:rgba(122,150,255,.55);
  background:linear-gradient(145deg,rgba(60,86,190,.34),rgba(120,72,214,.16));
  box-shadow:0 0 30px rgba(74,110,255,.26), inset 0 1px 0 rgba(255,255,255,.08);
}
.topnav .nav-link.active .ico{color:var(--neon-cyan);filter:drop-shadow(0 0 9px rgba(53,217,245,.85))}
.topnav .nav-link.active::after{
  content:"";position:absolute;left:24%;right:24%;bottom:4px;height:2px;border-radius:2px;
  background:linear-gradient(90deg,transparent,var(--neon-cyan),var(--neon-violet),transparent);
  box-shadow:0 0 10px rgba(53,217,245,.9);
}
.topnav .nav-link:focus-visible{outline:2px solid var(--neon-cyan);outline-offset:2px}
.dark-pill{
  display:inline-flex;align-items:center;gap:9px;padding:11px 18px;border-radius:999px;
  color:#DCE6FF;font-size:.88rem;white-space:nowrap;
  border:1px solid rgba(110,150,255,.34);background:linear-gradient(145deg,rgba(20,30,70,.55),rgba(6,10,26,.45));
}
.dark-pill .ico{color:var(--neon-cyan);filter:drop-shadow(0 0 8px rgba(53,217,245,.65))}
.topbar-spacer{height:18px}

/* ---------- hero ---------- */
html,body,.stApp{overflow-x:hidden}
.home-hero{
  position:relative;height:470px;overflow:hidden;background:#03050F;
  width:100vw;max-width:100vw;
  margin-left:calc(50% - 50vw) !important;margin-right:calc(50% - 50vw) !important;
  border-bottom:1px solid rgba(120,90,220,.28);
}
.home-hero-bg{
  position:absolute !important;top:0;left:0;bottom:0;right:0;
  width:100% !important;height:100% !important;min-width:100% !important;max-width:none !important;
  display:block;object-fit:cover !important;object-position:center 46%;
  filter:brightness(.62) saturate(1.35) contrast(1.06);
}
.home-hero-overlay{position:absolute;inset:0;
  background:
    linear-gradient(90deg,rgba(3,4,14,.96) 0%,rgba(4,6,20,.84) 24%,rgba(5,7,24,.36) 48%,rgba(8,4,26,.06) 72%,rgba(20,6,44,.18) 100%),
    linear-gradient(0deg,rgba(3,4,14,.88) 0%,transparent 44%,rgba(3,4,14,.30) 100%);
}
.home-hero-content{position:absolute;left:max(4.2%,calc(50vw - 738px));top:66px;z-index:2;max-width:640px}
.home-hero-content h1{margin:20px 0 14px !important;font-size:4rem !important;line-height:1.0 !important;
  font-weight:800 !important;letter-spacing:-2.6px;text-shadow:0 10px 40px rgba(0,0,0,.6)}
.home-hero-content h1 span{
  background:linear-gradient(94deg,#C77DFF 0%,#8A7BFF 42%,#4FA8FF 100%);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;
  text-shadow:none;filter:drop-shadow(0 0 26px rgba(150,110,255,.38));
}
.home-hero-content p{color:#C9D5EE;font-size:1.05rem;line-height:1.7;margin:0;max-width:560px}
.hero-badge{display:inline-flex;align-items:center;gap:9px;padding:9px 17px;border-radius:999px;
  border:1px solid rgba(120,160,255,.45);background:rgba(6,12,30,.55);backdrop-filter:blur(10px);
  color:#C3D5FF;font-size:.8rem;box-shadow:0 0 26px rgba(70,110,255,.16)}
.badge-dot{width:9px;height:9px;border-radius:50%;background:var(--neon-cyan);box-shadow:0 0 12px var(--neon-cyan)}

/* ---------- quick cards ---------- */
.shortcut-grid{position:relative;z-index:4;display:grid;grid-template-columns:repeat(5,1fr) !important;
  gap:18px !important;margin:-52px 2.2% 0 !important}
.home-shortcut{
  display:flex;align-items:center;gap:15px;min-height:96px !important;padding:16px 18px !important;
  border-radius:16px;border:1px solid var(--edge);background:var(--glass);backdrop-filter:blur(18px);
  color:#fff !important;text-decoration:none !important;
  box-shadow:0 20px 48px rgba(0,0,0,.62), inset 0 1px 0 rgba(255,255,255,.06);
  transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease;
}
.home-shortcut:hover{transform:translateY(-4px);border-color:rgba(150,180,255,.72);
  box-shadow:0 26px 60px rgba(0,0,0,.7),0 0 34px rgba(90,120,255,.26), inset 0 1px 0 rgba(255,255,255,.1)}
.home-shortcut:focus-visible{outline:2px solid var(--neon-cyan);outline-offset:3px}
.shortcut-icon{display:grid;place-items:center;width:46px !important;height:46px !important;flex:0 0 46px !important;
  color:var(--neon-blue);filter:drop-shadow(0 0 14px currentColor) drop-shadow(0 0 4px currentColor);animation:none !important}
.home-shortcut:nth-child(1) .shortcut-icon{color:#7C6BFF}
.home-shortcut:nth-child(2) .shortcut-icon{color:#3FE0B0}
.home-shortcut:nth-child(3) .shortcut-icon{color:var(--neon-cyan)}
.home-shortcut:nth-child(4) .shortcut-icon{color:#5AA9FF}
.home-shortcut:nth-child(5) .shortcut-icon{color:var(--neon-violet)}
.shortcut-copy{display:flex;flex-direction:column;min-width:0}
.shortcut-copy strong{font-size:1rem;font-weight:620;color:#F4F8FF;letter-spacing:-.1px}
.shortcut-copy small{margin-top:4px;color:var(--ink-dim);font-size:.79rem}
.shortcut-arrow{margin-left:auto;display:grid;place-items:center;color:#D8E6FF;opacity:.85}

/* ---------- KPI ---------- */
.kpi-head{display:flex;align-items:center;justify-content:space-between;margin:30px 2.2% 14px !important}
.kpi-title{display:flex;align-items:center;gap:11px;color:#F4F8FF;font-size:1.22rem;font-weight:700;letter-spacing:-.3px}
.kpi-title .ico{color:var(--neon-blue);filter:drop-shadow(0 0 10px rgba(76,141,255,.8))}
.live{display:inline-flex;align-items:center;border:1px solid rgba(110,150,255,.28);border-radius:999px;
  padding:7px 14px;color:#C9DBFF;font-size:.76rem;background:rgba(8,14,32,.6)}
div[class*="st-key-home_kpi_"]{
  background:var(--glass) !important;border:1px solid var(--edge) !important;border-radius:18px !important;
  padding:16px 18px 6px !important;min-height:250px !important;backdrop-filter:blur(16px);
  box-shadow:0 22px 56px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.05) !important;
}
.kpi-card-title{display:flex;align-items:center;gap:10px;color:#D3DFF7;font-size:.92rem;font-weight:550;margin:0 0 6px}
.kpi-card-title .ico{filter:drop-shadow(0 0 9px currentColor)}
.kpi-value{color:#FFF;font-size:2.15rem;font-weight:760;letter-spacing:-1px;margin:2px 0 3px}
.kpi-delta{color:var(--neon-mint);font-size:.82rem;margin:0 0 4px;display:flex;align-items:center;gap:7px}
.kpi-delta em{font-style:normal;color:var(--ink-dim)}
.kpi-delta.down{color:#FF7A9C}

/* donut legend */
.legend{display:flex;flex-direction:column;gap:13px;padding:14px 2px 0}
.legend-row{display:flex;align-items:center;gap:10px;font-size:.86rem;color:#DCE6FA}
.legend-row i{width:9px;height:9px;border-radius:50%;flex:0 0 9px;box-shadow:0 0 9px currentColor;background:currentColor}
.legend-row b{margin-left:auto;font-weight:600;color:#fff}

/* brand bars */
.brandlist{display:flex;flex-direction:column;gap:11px;padding:8px 0 10px}
.brandrow{display:grid;grid-template-columns:96px 1fr 60px;align-items:center;gap:11px;font-size:.84rem}
.brandrow span{color:#D6E1F7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.brandrow div{height:9px;border-radius:999px;background:rgba(120,160,255,.13);overflow:hidden}
.brandrow div u{display:block;height:100%;border-radius:999px;text-decoration:none}
.brandrow b{text-align:right;color:#F2F6FF;font-weight:600}

@media (max-width:1400px){
  .topnav .nav-link{padding:10px 12px;font-size:.82rem}
  .shortcut-grid{grid-template-columns:repeat(3,1fr) !important}
}
@media (max-width:1150px){
  .topbar{flex-wrap:wrap;gap:10px}.dark-pill{display:none}.topnav{justify-content:flex-start}
  .home-hero-content h1{font-size:3rem !important}
}
@media (max-width:900px){
  .shortcut-grid{grid-template-columns:repeat(2,1fr) !important;margin-top:-26px !important}
  .home-hero{height:500px}
}
@media (max-width:600px){
  .shortcut-grid{grid-template-columns:1fr !important}
  .home-hero-content h1{font-size:2.4rem !important;letter-spacing:-1.4px}
  .home-hero-content{left:6%;right:6%;top:46px}
  .desktop-break{display:none}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important;transition:none !important}
}
</style>
"""
