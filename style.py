import streamlit as st

FONT_LINK = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
"""

PREMIUM_CSS = """
<style>
* { box-sizing: border-box; }

html, body {
    font-family: 'Inter', sans-serif !important;
    background: #070B14 !important;
}

[class*="css"], .stApp, .main {
    font-family: 'Inter', sans-serif !important;
    background: #070B14 !important;
    color: #e2e8f0 !important;
}

.stApp {
    background: #070B14 !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0,245,255,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(59,130,246,0.02) 0%, transparent 70%) !important;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { visibility: hidden; }

.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem !important;
    max-width: 1440px !important;
}

/* ─── SIDEBAR ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08101F 0%, #050C18 100%) !important;
    border-right: 1px solid rgba(0,245,255,0.12) !important;
    box-shadow: 4px 0 30px rgba(0,245,255,0.04) !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 6px !important;
    padding: 0.5rem 0.8rem !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    color: #4a5568 !important;
    margin: 2px 0 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(0,245,255,0.06) !important;
    color: #00F5FF !important;
    border-color: rgba(0,245,255,0.15) !important;
    text-shadow: 0 0 8px rgba(0,245,255,0.5) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(90deg, rgba(0,245,255,0.1), rgba(0,245,255,0.03)) !important;
    color: #00F5FF !important;
    border-left: 2px solid #00F5FF !important;
    text-shadow: 0 0 10px rgba(0,245,255,0.6) !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.08) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown div {
    color: #4a5568 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.82rem !important;
}

[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; }

/* ─── HEADINGS with ORBITRON ─────────────────── */
h1, h2, h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.05em !important;
}

h1, [data-testid="stMarkdownContainer"] h1 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    margin-bottom: 0.25rem !important;
}

h2, [data-testid="stMarkdownContainer"] h2 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

h3, [data-testid="stMarkdownContainer"] h3 {
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
}

p, li { color: #94a3b8; line-height: 1.7; }

/* ─── KPI CARDS ──────────────────────────────── */
.nc-kpi-card {
    background: linear-gradient(135deg, rgba(13,20,35,0.95) 0%, rgba(8,14,26,0.95) 100%);
    border: 1px solid rgba(255,255,255,0.04);
    border-left: 3px solid;
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}

.nc-kpi-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, transparent 60%);
    pointer-events: none;
}

.nc-kpi-card:hover {
    transform: translateY(-3px);
}

.nc-kpi-icon {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    display: block;
}

.nc-kpi-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.65rem;
    font-weight: 700;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.4rem;
    display: block;
}

.nc-kpi-value {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1;
    display: block;
}

.nc-kpi-delta {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.72rem;
    color: #4a5568;
    margin-top: 0.4rem;
    display: block;
}

/* ─── SECTION HEADERS ────────────────────────── */
.nc-section-header {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.72rem;
    font-weight: 700;
    color: #00F5FF;
    margin: 2rem 0 0.9rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(0,245,255,0.12);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    text-shadow: 0 0 10px rgba(0,245,255,0.4);
}

/* ─── CHART LABELS ───────────────────────────── */
.nc-chart-label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.92rem;
    font-weight: 700;
    color: #cbd5e1;
    margin-bottom: 0.2rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.nc-chart-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #4a5568;
    margin-bottom: 0.5rem;
}

/* ─── INSIGHT CARDS ──────────────────────────── */
.nc-insight {
    border-left: 3px solid;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.65rem;
    font-size: 0.875rem;
    line-height: 1.65;
    color: #94a3b8;
    backdrop-filter: blur(4px);
}

/* ─── STREAMLIT METRICS ──────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(13,20,35,0.95), rgba(8,14,26,0.95)) !important;
    border: 1px solid rgba(0,245,255,0.08) !important;
    border-radius: 10px !important;
    padding: 1rem 1.25rem !important;
    transition: transform 0.2s ease !important;
}

[data-testid="stMetric"]:hover { transform: translateY(-2px) !important; }

[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    color: #4a5568 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
}

/* ─── BUTTONS ────────────────────────────────── */
.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: rgba(8,14,26,0.9) !important;
    color: #64748b !important;
    border: 1px solid rgba(0,245,255,0.15) !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    padding: 0.45rem 1.1rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: rgba(0,245,255,0.07) !important;
    border-color: #00F5FF !important;
    color: #00F5FF !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.15), inset 0 0 10px rgba(0,245,255,0.03) !important;
    text-shadow: 0 0 8px rgba(0,245,255,0.5) !important;
}

/* ─── INPUTS ─────────────────────────────────── */
.stTextInput > div > div > input,
.stDateInput > div > div > input {
    background: rgba(8,14,26,0.9) !important;
    border: 1px solid rgba(0,245,255,0.12) !important;
    border-radius: 6px !important;
    color: #f1f5f9 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
}

.stSelectbox > div > div {
    background: rgba(8,14,26,0.9) !important;
    border: 1px solid rgba(0,245,255,0.12) !important;
    border-radius: 6px !important;
    color: #f1f5f9 !important;
}

/* ─── DATAFRAME ──────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,245,255,0.08) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ─── EXPANDER ───────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(8,14,26,0.8) !important;
    border: 1px solid rgba(0,245,255,0.08) !important;
    border-radius: 10px !important;
}

/* ─── TABS ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(8,14,26,0.9);
    border-radius: 8px;
    padding: 3px;
    gap: 3px;
    border: 1px solid rgba(0,245,255,0.08);
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    background: transparent !important;
    color: #4a5568 !important;
    border-radius: 6px !important;
    padding: 0.35rem 1rem !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,245,255,0.08) !important;
    color: #00F5FF !important;
    text-shadow: 0 0 8px rgba(0,245,255,0.4) !important;
}

/* ─── DOWNLOAD BUTTON ────────────────────────── */
.stDownloadButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: rgba(59,130,246,0.1) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59,130,246,0.2) !important;
    border-radius: 6px !important;
}

.stDownloadButton > button:hover {
    background: rgba(59,130,246,0.2) !important;
    border-color: #3b82f6 !important;
    box-shadow: 0 0 12px rgba(59,130,246,0.2) !important;
}

/* ─── ALERTS ─────────────────────────────────── */
.stSuccess {
    background: rgba(16,185,129,0.07) !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
    border-radius: 8px !important;
}
.stInfo {
    background: rgba(59,130,246,0.07) !important;
    border: 1px solid rgba(59,130,246,0.18) !important;
    border-radius: 8px !important;
}
.stWarning {
    background: rgba(245,158,11,0.07) !important;
    border: 1px solid rgba(245,158,11,0.18) !important;
    border-radius: 8px !important;
}
.stError {
    background: rgba(239,68,68,0.07) !important;
    border: 1px solid rgba(239,68,68,0.18) !important;
    border-radius: 8px !important;
}

hr {
    border: none !important;
    border-top: 1px solid rgba(0,245,255,0.06) !important;
    margin: 1.5rem 0 !important;
}

/* ─── SCROLLBAR ──────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #070B14; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.25); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,245,255,0.45); }

/* ─── FILE UPLOADER ──────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(8,14,26,0.8) !important;
    border: 1px dashed rgba(0,245,255,0.2) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* ─── SLIDER ─────────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
    background: #00F5FF !important;
    box-shadow: 0 0 8px rgba(0,245,255,0.6) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[class*="thumb"] {
    background: #00F5FF !important;
}
</style>
"""

COLORS = {
    "cyan":   "#00F5FF",
    "blue":   "#3B82F6",
    "purple": "#8B5CF6",
    "green":  "#10B981",
    "amber":  "#F59E0B",
    "red":    "#EF4444",
    "pink":   "#EC4899",
}
COLOR_SEQ = list(COLORS.values())

PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(7,11,20,0)",
    plot_bgcolor="rgba(7,11,20,0)",
    font=dict(family="'Rajdhani', sans-serif", color="#94a3b8", size=13),
    xaxis=dict(
        gridcolor="rgba(0,245,255,0.05)",
        zeroline=False,
        linecolor="rgba(0,245,255,0.08)",
        tickfont=dict(family="Rajdhani, sans-serif", size=12),
    ),
    yaxis=dict(
        gridcolor="rgba(0,245,255,0.05)",
        zeroline=False,
        linecolor="rgba(0,245,255,0.08)",
        tickfont=dict(family="Rajdhani, sans-serif", size=12),
    ),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        bgcolor="rgba(7,11,20,0.85)",
        bordercolor="rgba(0,245,255,0.12)",
        borderwidth=1,
        font=dict(family="Rajdhani, sans-serif", size=12),
    ),
    hoverlabel=dict(
        bgcolor="rgba(8,14,26,0.95)",
        bordercolor="rgba(0,245,255,0.3)",
        font=dict(family="Rajdhani, sans-serif", size=13, color="#e2e8f0"),
    ),
)


def inject_css():
    st.markdown(FONT_LINK, unsafe_allow_html=True)
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)


def sidebar_brand():
    st.sidebar.markdown("""
        <div style="padding:0.5rem 0 1.25rem 0;">
            <div style="font-family:'Orbitron',monospace;font-size:0.95rem;font-weight:800;
                        color:#00F5FF;letter-spacing:0.1em;
                        text-shadow:0 0 15px rgba(0,245,255,0.5);">
                NASSAU CANDY
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.68rem;
                        color:#2d3f5a;margin-top:4px;letter-spacing:0.15em;
                        text-transform:uppercase;">
                Logistics Intelligence Platform
            </div>
        </div>
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(0,245,255,0.2),transparent);margin-bottom:0.75rem;"></div>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    icon_html = f'<span style="margin-right:0.4rem;">{icon}</span>' if icon else ""
    st.markdown(f"""
        <div style="margin-bottom:1.75rem;padding-bottom:1rem;
                    border-bottom:1px solid rgba(0,245,255,0.08);">
            <div style="font-family:'Orbitron',monospace;font-size:1.55rem;font-weight:700;
                        color:#f1f5f9;letter-spacing:0.06em;line-height:1.2;
                        text-shadow:0 0 20px rgba(0,245,255,0.15);">
                {icon_html}{title}
            </div>
            {"<div style='font-family:Rajdhani,sans-serif;color:#4a5568;font-size:0.85rem;margin-top:0.4rem;letter-spacing:0.08em;text-transform:uppercase;'>" + subtitle + "</div>" if subtitle else ""}
        </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="nc-section-header">{title}</div>', unsafe_allow_html=True)


def chart_label(title: str, sub: str = ""):
    st.markdown(
        f'<div class="nc-chart-label">{title}</div>'
        + (f'<div class="nc-chart-sub">{sub}</div>' if sub else ""),
        unsafe_allow_html=True,
    )


def kpi_card(col, title: str, value: str, delta: str = "", icon: str = "", color: str = "#00F5FF"):
    with col:
        st.markdown(f"""
            <div class="nc-kpi-card" style="border-color:{color};
                 box-shadow:0 0 20px {color}18,0 4px 20px rgba(0,0,0,0.5);">
                <span class="nc-kpi-icon">{icon}</span>
                <span class="nc-kpi-label">{title}</span>
                <span class="nc-kpi-value" style="color:{color};
                      text-shadow:0 0 12px {color}60;">{value}</span>
                {"<span class='nc-kpi-delta'>" + delta + "</span>" if delta else ""}
            </div>
        """, unsafe_allow_html=True)


def insight_card(text: str, kind: str = "info"):
    palettes = {
        "success": ("#10B981", "rgba(16,185,129,0.07)"),
        "warning": ("#F59E0B", "rgba(245,158,11,0.07)"),
        "error":   ("#EF4444", "rgba(239,68,68,0.07)"),
        "info":    ("#3B82F6", "rgba(59,130,246,0.07)"),
    }
    bc, bg = palettes.get(kind, palettes["info"])
    st.markdown(
        f'<div class="nc-insight" style="border-color:{bc};background:{bg};">{text}</div>',
        unsafe_allow_html=True
    )


def apply_plot_layout(fig, height: int = 380):
    fig.update_layout(height=height, **PLOT_LAYOUT)
    return fig


def footer():
    st.markdown("""
        <div style="margin-top:3.5rem;padding-top:1rem;
                    border-top:1px solid rgba(0,245,255,0.06);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-family:'Orbitron',monospace;font-size:0.6rem;
                            color:#1e2d3d;letter-spacing:0.15em;">
                    © 2025 NASSAU CANDY DISTRIBUTING
                </div>
                <div style="font-family:'Orbitron',monospace;font-size:0.6rem;
                            color:#1e2d3d;letter-spacing:0.15em;">
                    WHOLESALE INTELLIGENCE PLATFORM
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
