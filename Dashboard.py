import streamlit as st
import pandas as pd
import plotly.express as px
import io
from style import inject_css, sidebar_brand, page_header, kpi_card, section_header, insight_card, footer, COLORS, apply_plot_layout, chart_label
from data_manager import _parse_csv

st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
sidebar_brand()

page_header(
    "Nassau Candy",
    "Wholesale Intelligence Platform · Shipping & Distribution Analytics",
    "🍪",
)

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Products",             "25,000+",       icon="📦", color=COLORS["cyan"])
kpi_card(c2, "Distribution Centers", "6 Nationwide",  icon="🏭", color=COLORS["green"])
kpi_card(c3, "Years in Business",    "80+ Years",     icon="📅", color=COLORS["amber"])
kpi_card(c4, "Global Brands",        "Jelly Belly+",  icon="🌍", color=COLORS["purple"])

section_header("Data Setup")

if "master_df" in st.session_state:
    df = st.session_state.master_df

    date_min = df["Order Date"].min().strftime("%b %d, %Y") if "Order Date" in df.columns else "—"
    date_max = df["Order Date"].max().strftime("%b %d, %Y") if "Order Date" in df.columns else "—"

    insight_card(
        f"✅ <strong>{len(df):,} shipments</strong> loaded · {df.shape[1]} columns · "
        f"Period: <strong>{date_min}</strong> → <strong>{date_max}</strong>. "
        "Use the sidebar to navigate analytics pages.",
        "success",
    )

    section_header("Live KPI Dashboard")

    total        = len(df)
    avg_lead     = df["Lead Time"].mean() if "Lead Time" in df.columns else 0
    delayed_pct  = df["Delayed"].mean() * 100 if "Delayed" in df.columns else 0
    on_time_pct  = 100 - delayed_pct
    routes       = df["Route"].nunique() if "Route" in df.columns else 0
    states       = df["State/Province"].nunique() if "State/Province" in df.columns else 0
    ship_modes   = df["Ship Mode"].nunique() if "Ship Mode" in df.columns else 0
    divisions    = df["Division"].nunique() if "Division" in df.columns else 0

    k1, k2, k3, k4 = st.columns(4)
    kpi_card(k1, "Total Shipments", f"{total:,}",          icon="📦", color=COLORS["cyan"])
    kpi_card(k2, "Avg Lead Time",   f"{avg_lead:.1f}d",    icon="⏱",  color=COLORS["blue"])
    kpi_card(k3, "On-Time Rate",    f"{on_time_pct:.1f}%", icon="✅",  color=COLORS["green"])
    kpi_card(k4, "Delayed Rate",    f"{delayed_pct:.1f}%", icon="⚠️", color=COLORS["amber"])
    
    k5, k6, k7, k8 = st.columns(4)
    kpi_card(k5, "Active Routes",   f"{routes}",           icon="🗺️", color=COLORS["purple"])
    kpi_card(k6, "States Covered",  f"{states}",           icon="🌍",  color=COLORS["pink"])
    kpi_card(k7, "Ship Modes",      f"{ship_modes}",       icon="🚛",  color=COLORS["red"])
    kpi_card(k8, "Divisions",       f"{divisions}",        icon="🏭",  color=COLORS["cyan"])

    section_header("Shipment Trend")

    cl, cr = st.columns([3, 2])

    with cl:
        chart_label("Monthly Shipment Volume", "Orders placed per month")
        if "Order Date" in df.columns:
            monthly = (
                df.groupby(df["Order Date"].dt.to_period("M"))
                .size()
                .reset_index(name="Shipments")
            )
            monthly["Order Date"] = monthly["Order Date"].astype(str)
            fig_trend = px.area(
                monthly, x="Order Date", y="Shipments",
                color_discrete_sequence=[COLORS["cyan"]],
            )
            fig_trend.update_traces(fillcolor="rgba(0,245,255,0.08)", line=dict(width=2))
            fig_trend.update_xaxes(title="")
            fig_trend.update_yaxes(title="")
            apply_plot_layout(fig_trend, 280)
            st.plotly_chart(fig_trend, use_container_width=True)

    with cr:
        chart_label("On-Time vs Delayed", "Overall shipment split")
        if "Delayed" in df.columns:
            pie_df = pd.DataFrame({
                "Status": ["On-Time", "Delayed"],
                "Count": [df["Delayed"].eq(False).sum(), df["Delayed"].sum()],
            })
            fig_pie = px.pie(
                pie_df, names="Status", values="Count",
                color_discrete_sequence=[COLORS["green"], COLORS["red"]],
                hole=0.6,
            )
            fig_pie.update_traces(
                textfont_size=12, textinfo="percent+label",
                marker=dict(line=dict(color="rgba(7,11,20,0.8)", width=2)),
            )
            apply_plot_layout(fig_pie, 280)
            st.plotly_chart(fig_pie, use_container_width=True)

    section_header("Performance Snapshot")

    s1, s2 = st.columns(2)

    with s1:
        chart_label("Lead Time Distribution", "Days from order to shipment")
        if "Lead Time" in df.columns:
            fig_hist = px.histogram(df, x="Lead Time", nbins=30,
                                    color_discrete_sequence=[COLORS["blue"]])
            fig_hist.update_traces(marker_line_color="rgba(7,11,20,0.8)", marker_line_width=1)
            apply_plot_layout(fig_hist, 260)
            st.plotly_chart(fig_hist, use_container_width=True)

    with s2:
        chart_label("Top Routes by Volume", "Shipment count per route")
        if "Route" in df.columns:
            route_vol = df.groupby("Route", observed=True).size().nlargest(8).reset_index(name="Shipments")
            fig_bar = px.bar(
                route_vol, x="Shipments", y="Route", orientation="h",
                color="Shipments",
                color_continuous_scale=[[0, "#1e3a5f"], [1, COLORS["cyan"]]],
            )
            fig_bar.update_layout(coloraxis_showscale=False, yaxis_title="")
            apply_plot_layout(fig_bar, 260)
            st.plotly_chart(fig_bar, use_container_width=True)

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("Upload Different CSV", use_container_width=True):
            for k in ["master_df", "file_name", "start_date", "end_date",
                      "state_filter", "mode_filter", "delay_threshold"]:
                if k in st.session_state:
                    del st.session_state[k]
            _parse_csv.clear()
            st.rerun()

else:
    st.markdown("""
        <div style="background:rgba(17,24,39,0.8);border:1px dashed rgba(0,245,255,0.2);
                    border-radius:14px;padding:2.5rem;text-align:center;margin-bottom:1.5rem;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">📂</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:1rem;font-weight:700;
                        color:#f1f5f9;margin-bottom:0.4rem;">Upload Your Shipping Data</div>
            <div style="font-size:0.82rem;color:#475569;">
                Upload <strong style="color:#94a3b8;">Nassau Candy Distributor.csv</strong>
                to unlock all analytics pages and live KPIs.
            </div>
        </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    if uploaded:
        try:
            with st.spinner("Processing dataset..."):
                raw_bytes = uploaded.read()
                df = _parse_csv(raw_bytes)
                st.session_state.master_df = df
                st.session_state.file_name = uploaded.name
            st.success(f"Dataset loaded — {len(df):,} shipments ready.")
            st.rerun()
        except Exception as e:
            st.error(f"Could not parse CSV: {e}")

section_header("About Nassau Candy")
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Brands & Products", "Seasonal", "Distribution"])

with tab1:
    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
            <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                        border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Product Categories</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.45rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🍫 Chocolate & Bulk Candy</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🍭 Specialty Sweets & Confectionery</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🥤 Gourmet Soda & Beverages</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🌰 Dried Fruits, Nuts & Natural Foods</li>
                    <li style="padding:0.45rem 0;">🧴 Natural Health & Household Care</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with cr:
        st.markdown("""
            <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                        border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Manufacturing</h3>
                <p style="color:#94a3b8;font-size:0.875rem;">Nassau Candy operates production facilities in
                <strong style="color:#cbd5e1;">Hicksville, NY</strong> alongside global manufacturing partners.</p>
                <div style="margin-top:0.75rem;padding:0.7rem;background:rgba(7,11,20,0.8);border-radius:8px;
                            border-left:3px solid #00F5FF;">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:0.78rem;color:#00F5FF;font-weight:700;">
                        Fast Nationwide Delivery
                    </div>
                    <div style="font-size:0.78rem;color:#475569;margin-top:2px;">
                        6 distribution centers ensure industry-leading logistics.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
            <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                        border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Global Partner Brands</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🟡 Jelly Belly®</li>
                    <li style="padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🟤 Godiva®</li>
                    <li style="padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">🍫 Ghirardelli®</li>
                    <li style="padding:0.4rem 0;">🍬 Lindt®</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with cr:
        st.markdown("""
            <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                        border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Exclusive In-House Brands</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">✨ Clever Candy®</li>
                    <li style="padding:0.4rem 0;">🍬 Nancy Adams®</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    cols = st.columns(4)
    for col, (icon, name, desc) in zip(cols, [
        ("🎃", "Halloween",   "Rare & nostalgic collections"),
        ("🎄", "Christmas",   "Premium holiday assortments"),
        ("💘", "Valentine's", "Gifting-ready selections"),
        ("🐣", "Easter",      "Spring seasonal candy"),
    ]):
        with col:
            st.markdown(f"""
                <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                            border-radius:12px;padding:1.1rem;text-align:center;">
                    <div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-weight:700;
                                color:#e2e8f0;font-size:0.9rem;">{name}</div>
                    <div style="font-size:0.76rem;color:#475569;margin-top:0.3rem;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
        <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                    border-radius:12px;padding:1.25rem;">
            <h3 style="margin-top:0!important;">Nationwide Distribution Network</h3>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;margin-top:0.75rem;">
                <div style="background:rgba(7,11,20,0.8);border-radius:8px;padding:0.75rem;
                            border:1px solid rgba(0,245,255,0.08);">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:0.8rem;font-weight:700;
                                color:#10B981;">✔ Fast Delivery</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">6 centers across the USA</div>
                </div>
                <div style="background:rgba(7,11,20,0.8);border-radius:8px;padding:0.75rem;
                            border:1px solid rgba(0,245,255,0.08);">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:0.8rem;font-weight:700;
                                color:#10B981;">✔ High Availability</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">25,000+ products in stock</div>
                </div>
                <div style="background:rgba(7,11,20,0.8);border-radius:8px;padding:0.75rem;
                            border:1px solid rgba(0,245,255,0.08);">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:0.8rem;font-weight:700;
                                color:#10B981;">✔ Top Logistics</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">Industry-leading performance</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

footer()
