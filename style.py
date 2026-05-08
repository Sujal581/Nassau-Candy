import streamlit as st

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp { background-color: #0f172a !important; color: #f1f5f9 !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem 2.5rem !important; max-width: 1400px; }

[data-testid="stSidebar"] { background: #0b1120 !important; border-right: 1px solid #1e293b !important; }
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
[data-testid="stSidebarNav"] a {
    border-radius: 8px !important; padding: 0.45rem 0.75rem !important;
    font-size: 0.875rem !important; font-weight: 500 !important;
    color: #94a3b8 !important; margin: 2px 0 !important; transition: all 0.15s ease !important;
}
[data-testid="stSidebarNav"] a:hover { background: #1e293b !important; color: #f1f5f9 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #1e3a5f !important; color: #60a5fa !important; border-left: 3px solid #3b82f6 !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown div { color: #94a3b8 !important; font-size: 0.82rem !important; }
[data-testid="stSidebar"] hr { border-color: #1e293b !important; margin: 0.75rem 0 !important; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; }

h1 { font-size: 1.75rem !important; font-weight: 800 !important; color: #f1f5f9 !important; letter-spacing: -0.02em; margin-bottom: 0.25rem !important; }
h2 { font-size: 1.25rem !important; font-weight: 700 !important; color: #e2e8f0 !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; color: #cbd5e1 !important; }
p, li { color: #94a3b8; line-height: 1.7; }

.nc-kpi-card {
    background: linear-gradient(145deg, #1e293b, #162032);
    border-left: 4px solid; border-radius: 12px; padding: 1.1rem 1.25rem;
    margin-bottom: 0.5rem; box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease; cursor: default;
}
.nc-kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.45); }
.nc-kpi-icon { font-size: 1.1rem; margin-bottom: 0.4rem; }
.nc-kpi-label { font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.3rem; }
.nc-kpi-value { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; line-height: 1; }
.nc-kpi-delta { font-size: 0.75rem; color: #64748b; margin-top: 0.3rem; }

.nc-section-header {
    font-size: 0.95rem; font-weight: 700; color: #e2e8f0;
    margin: 1.75rem 0 0.75rem 0; padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e293b; letter-spacing: -0.01em;
}
.nc-chart-label { font-size: 0.85rem; font-weight: 600; color: #cbd5e1; margin-bottom: 0.25rem; }
.nc-chart-sub { font-size: 0.75rem; color: #475569; margin-bottom: 0.5rem; }
.nc-insight {
    border-left: 3px solid; border-radius: 10px; padding: 0.85rem 1.1rem;
    margin-bottom: 0.75rem; font-size: 0.875rem; line-height: 1.65; color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: #1e293b !important; border: 1px solid #334155 !important;
    border-radius: 12px !important; padding: 1rem 1.25rem !important; transition: transform 0.2s ease !important;
}
[data-testid="stMetric"]:hover { transform: translateY(-2px) !important; }
[data-testid="stMetricLabel"] { font-size: 0.72rem !important; font-weight: 600 !important; color: #64748b !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }
[data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 800 !important; color: #f1f5f9 !important; }

.stButton > button {
    background: #1e293b !important; color: #cbd5e1 !important; border: 1px solid #334155 !important;
    border-radius: 8px !important; font-weight: 500 !important; font-size: 0.85rem !important;
    padding: 0.45rem 1.1rem !important; transition: all 0.15s ease !important;
}
.stButton > button:hover { background: #334155 !important; border-color: #3b82f6 !important; color: #f1f5f9 !important; }

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background: #1e293b !important; border: 1px solid #334155 !important;
    border-radius: 8px !important; color: #f1f5f9 !important; font-size: 0.85rem !important;
}
.stSlider .st-bk { background: #3b82f6 !important; }

[data-testid="stDataFrame"] { border: 1px solid #1e293b !important; border-radius: 12px !important; overflow: hidden !important; }

[data-testid="stExpander"] { background: #1e293b !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
[data-testid="stExpander"] summary { color: #cbd5e1 !important; font-weight: 500 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #1e293b; border-radius: 10px; padding: 3px; gap: 3px; border: 1px solid #334155;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #64748b !important; border-radius: 8px !important;
    padding: 0.35rem 0.9rem !important; font-size: 0.85rem !important; font-weight: 500 !important;
}
.stTabs [aria-selected="true"] { background: #0f172a !important; color: #f1f5f9 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important; }

.stDownloadButton > button { background: #2563eb !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
.stDownloadButton > button:hover { background: #3b82f6 !important; }

.stSuccess { background: rgba(22,163,74,0.12) !important; border: 1px solid rgba(22,163,74,0.3) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(37,99,235,0.10) !important; border: 1px solid rgba(37,99,235,0.25) !important; border-radius: 10px !important; }
.stWarning { background: rgba(245,158,11,0.10) !important; border: 1px solid rgba(245,158,11,0.25) !important; border-radius: 10px !important; }
.stError   { background: rgba(220,38,38,0.10) !important; border: 1px solid rgba(220,38,38,0.25) !important; border-radius: 10px !important; }
hr { border-color: #1e293b !important; margin: 1.5rem 0 !important; }
</style>
"""

COLORS = {
    "blue": "#3b82f6", "green": "#22c55e", "amber": "#f59e0b",
    "red": "#ef4444", "purple": "#a855f7", "cyan": "#06b6d4", "pink": "#ec4899",
}
COLOR_SEQ = list(COLORS.values())

PLOT_LAYOUT = dict(
    template="plotly_dark", paper_bgcolor="#1e293b", plot_bgcolor="#1e293b",
    font=dict(family="Inter, sans-serif", color="#94a3b8", size=12),
    xaxis=dict(gridcolor="#334155", zeroline=False, linecolor="#334155"),
    yaxis=dict(gridcolor="#334155", zeroline=False, linecolor="#334155"),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(bgcolor="#0f172a", bordercolor="#334155", borderwidth=1, font=dict(size=11)),
)

def inject_css():
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

def sidebar_brand():
    st.sidebar.markdown("""
        <div style="padding:0.25rem 0 1.25rem 0;">
            <div style="font-size:1.05rem;font-weight:800;color:#f1f5f9;">🍪 Nassau Candy</div>
            <div style="font-size:0.72rem;color:#475569;margin-top:2px;">Wholesale Intelligence Dashboard</div>
        </div>
        <hr style="border-color:#1e293b;margin:0 0 0.75rem 0;">
    """, unsafe_allow_html=True)

def page_header(title: str, subtitle: str = "", icon: str = ""):
    label = f"{icon} {title}" if icon else title
    st.markdown(f"""
        <div style="margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid #1e293b;">
            <h1 style="margin-bottom:0.2rem!important;">{label}</h1>
            {"<p style='color:#475569;font-size:0.875rem;margin:0;'>" + subtitle + "</p>" if subtitle else ""}
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

def kpi_card(col, title: str, value: str, delta: str = "", icon: str = "", color: str = "#3b82f6"):
    with col:
        st.markdown(f"""
            <div class="nc-kpi-card" style="border-color:{color};">
                <div class="nc-kpi-icon">{icon}</div>
                <div class="nc-kpi-label">{title}</div>
                <div class="nc-kpi-value">{value}</div>
                {"<div class='nc-kpi-delta'>" + delta + "</div>" if delta else ""}
            </div>
        """, unsafe_allow_html=True)

def insight_card(text: str, kind: str = "info"):
    palettes = {
        "success": ("#22c55e", "rgba(22,163,74,0.1)"),
        "warning": ("#f59e0b", "rgba(245,158,11,0.1)"),
        "error":   ("#ef4444", "rgba(220,38,38,0.1)"),
        "info":    ("#3b82f6", "rgba(37,99,235,0.1)"),
    }
    bc, bg = palettes.get(kind, palettes["info"])
    st.markdown(f'<div class="nc-insight" style="border-color:{bc};background:{bg};">{text}</div>', unsafe_allow_html=True)

def apply_plot_layout(fig, height: int = 380):
    fig.update_layout(height=height, **PLOT_LAYOUT)
    return fig

def footer():
    st.markdown("""
        <div style="margin-top:3rem;padding-top:1.25rem;border-top:1px solid #1e293b;
                    display:flex;justify-content:space-between;align-items:center;">
            <div style="font-size:0.75rem;color:#334155;">© 2025 Nassau Candy · Wholesale Intelligence Platform</div>
            <div style="font-size:0.75rem;color:#334155;">Powered by Streamlit</div>
        </div>
    """, unsafe_allow_html=True)

    