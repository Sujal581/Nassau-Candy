import streamlit as st
import plotly.express as px
import pandas as pd
from data_manager import apply_filters, init_data, init_data
from utils import load_data, ship_mode_analysis
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS, COLOR_SEQ)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)
inject_css(); sidebar_brand(); init_data()
page_header("Ship Mode Analysis", "Distrubition of the products", "🚛")


# ---------------- DATA ----------------
df= init_data()
df = apply_filters()
if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

# Empty after filters
if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()
mode_df = ship_mode_analysis(df)

# ---------------- SAFETY CHECK ----------------
if "Avg_Lead_Time" in mode_df.columns:
    mode_df = mode_df.sort_values(by="Avg_Lead_Time")

# ---------------- 🔥 ENHANCED METRICS ----------------
mode_df["Rank"] = range(1, len(mode_df) + 1)

# Efficiency Score (higher = better)
mode_df["Efficiency Score"] = (
    (1 / mode_df["Avg_Lead_Time"]) * 0.7 +
    (mode_df["Shipments"] / mode_df["Shipments"].max()) * 0.3
).round(3)

# ---------------- ROW 1 ----------------
col1, col2 = st.columns(2, gap="small")

# ---------------- BAR: SPEED ----------------
with col1:
    st.subheader("📊 Avg Lead Time (Speed)")

    fig1 = px.bar(
        mode_df,
        x="Ship Mode",
        y="Avg_Lead_Time",
        color="Avg_Lead_Time",
        text="Rank",
        color_continuous_scale="RdYlGn_r"
    )

    fig1.update_traces(textposition="outside")

    fig1.update_layout(
        height=350,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=20, b=10)
    )

    st.plotly_chart(fig1, use_container_width=True)

# ---------------- PIE: USAGE ----------------
with col2:
    st.subheader("🥧 Shipment Distribution")

    fig2 = px.pie(
        mode_df,
        names="Ship Mode",
        values="Shipments",
        hole=0.5
    )

    fig2.update_layout(
        height=350,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- ROW 2 ----------------
st.markdown("### 📈 Performance Trend Over Time")

trend = df.copy()

if "Order Date" in trend.columns:
    trend["Order Date"] = pd.to_datetime(trend["Order Date"], errors="coerce")
    trend["Month"] = trend["Order Date"].dt.to_period("M").astype(str)
else:
    trend["Month"] = "Unknown"

trend_df = trend.groupby(["Month", "Ship Mode"])["Lead Time"].mean().reset_index()

fig3 = px.line(
    trend_df,
    x="Month",
    y="Lead Time",
    color="Ship Mode",
    markers=True
)

fig3.update_layout(
    height=500,
    template="plotly_dark",
    margin=dict(l=10, r=10, t=20, b=10)
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- 🧠 INSIGHTS PANEL ----------------
st.markdown("### 🧠 Business Insights")

best_mode = mode_df.sort_values("Efficiency Score", ascending=False).iloc[0]
worst_mode = mode_df.sort_values("Avg_Lead_Time", ascending=False).iloc[0]

st.success(f"""
🥇 **Best Performing Ship Mode:** {best_mode['Ship Mode']}  
- Efficiency Score: {best_mode['Efficiency Score']}  
- Avg Lead Time: {best_mode['Avg_Lead_Time']} days
""")

st.error(f"""
⚠️ **Worst Performing Ship Mode:** {worst_mode['Ship Mode']}  
- Avg Lead Time: {worst_mode['Avg_Lead_Time']} days  
- Rank: {worst_mode['Rank']}
""")

# ---------------- FULL TABLE ----------------
st.markdown("### 📋 Ship Mode Performance Table")

st.dataframe(
    mode_df[["Rank", "Ship Mode", "Avg_Lead_Time", "Shipments", "Efficiency Score"]],
    use_container_width=True
)