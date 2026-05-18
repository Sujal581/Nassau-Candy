import streamlit as st
import plotly.express as px
import pandas as pd
from data_manager import apply_filters
from utils import ship_mode_analysis
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS, COLOR_SEQ)

st.set_page_config(page_title="Ship Mode | Nassau Candy", layout="wide", page_icon="🚛")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Ship Mode Analysis", "Delivery mode performance, distribution, and trend analysis", "🚛")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

mode_df = ship_mode_analysis(df)

if "Avg_Lead_Time" in mode_df.columns:
    mode_df = mode_df.sort_values("Avg_Lead_Time")

mode_df["Rank"] = range(1, len(mode_df) + 1)
mode_df["Efficiency_Score"] = (
    (1 / mode_df["Avg_Lead_Time"]) * 0.7 +
    (mode_df["Shipments"] / mode_df["Shipments"].max()) * 0.3
).round(3)

best_mode  = mode_df.sort_values("Efficiency_Score", ascending=False).iloc[0]
worst_mode = mode_df.sort_values("Avg_Lead_Time", ascending=False).iloc[0]
fastest    = mode_df.nsmallest(1, 'Avg_Lead_Time').iloc[0]

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Ship Modes",       f"{len(mode_df)}",                         icon="🚛", color=COLORS["cyan"])
kpi_card(c2, "Fastest Mode",     fastest['Ship Mode'],                       icon="⚡",  color=COLORS["green"])
kpi_card(c3, "Best Efficiency",  best_mode['Ship Mode'],                     icon="🏆",  color=COLORS["blue"])
kpi_card(c4, "Most Used",        mode_df.nlargest(1,'Shipments').iloc[0]['Ship Mode'], icon="📦", color=COLORS["purple"])

section_header("Speed & Volume")
col1, col2 = st.columns(2)

with col1:
    chart_label("Avg Lead Time by Ship Mode", "Lower is faster")
    fig1 = px.bar(
        mode_df, x="Ship Mode", y="Avg_Lead_Time",
        color="Avg_Lead_Time", text="Rank",
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]]
    )
    fig1.update_traces(texttemplate='#%{text}', textposition="outside")
    fig1.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Avg Days")
    apply_plot_layout(fig1, 340)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    chart_label("Shipment Distribution by Mode")
    fig2 = px.pie(
        mode_df, names="Ship Mode", values="Shipments",
        hole=0.55, color_discrete_sequence=COLOR_SEQ
    )
    fig2.update_traces(
        textinfo='percent+label',
        marker=dict(line=dict(color='rgba(7,11,20,0.8)', width=2))
    )
    apply_plot_layout(fig2, 340)
    st.plotly_chart(fig2, use_container_width=True)

section_header("Delay Rate by Ship Mode")
chart_label("Delay Rate Comparison", "% of shipments exceeding threshold")
fig_delay = px.bar(
    mode_df.sort_values('Delay_Rate', ascending=False),
    x='Ship Mode', y='Delay_Rate',
    color='Delay_Rate',
    color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
    text='Delay_Rate'
)
fig_delay.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_delay.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Delay Rate (%)")
apply_plot_layout(fig_delay, 320)
st.plotly_chart(fig_delay, use_container_width=True)

section_header("Performance Trend Over Time")
chart_label("Monthly Avg Lead Time by Ship Mode")
trend = df.copy()
trend["Order Date"] = pd.to_datetime(trend["Order Date"], errors="coerce")
trend["Month"] = trend["Order Date"].dt.to_period("M").astype(str)
trend_df = trend.groupby(["Month", "Ship Mode"])["Lead Time"].mean().reset_index()

fig3 = px.line(
    trend_df, x="Month", y="Lead Time", color="Ship Mode",
    markers=True, color_discrete_sequence=COLOR_SEQ,
    labels={"Lead Time": "Avg Lead (days)", "Month": ""}
)
fig3.update_traces(line=dict(width=2.5), marker=dict(size=7))
apply_plot_layout(fig3, 380)
st.plotly_chart(fig3, use_container_width=True)

section_header("Efficiency Score Ranking")
chart_label("Composite Efficiency Score", "Higher = better (speed + volume weighted)")
fig_eff = px.bar(
    mode_df.sort_values('Efficiency_Score'),
    x='Efficiency_Score', y='Ship Mode', orientation='h',
    color='Efficiency_Score',
    color_continuous_scale=[[0, COLORS["red"]], [0.5, COLORS["amber"]], [1, COLORS["green"]]],
    text='Efficiency_Score'
)
fig_eff.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig_eff.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Efficiency Score")
apply_plot_layout(fig_eff, 300)
st.plotly_chart(fig_eff, use_container_width=True)

section_header("Ship Mode Performance Table")
tbl = mode_df[["Rank", "Ship Mode", "Avg_Lead_Time", "Shipments", "Delay_Rate", "Efficiency_Score"]].copy()
tbl.columns = ["Rank", "Ship Mode", "Avg Lead (days)", "Shipments", "Delay Rate (%)", "Efficiency Score"]
st.dataframe(
    tbl.style
        .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
        .background_gradient(subset=['Delay Rate (%)'], cmap='Reds')
        .background_gradient(subset=['Efficiency Score'], cmap='Greens')
        .format({'Avg Lead (days)': '{:.1f}', 'Delay Rate (%)': '{:.1f}%', 'Efficiency Score': '{:.3f}'}),
    use_container_width=True
)

section_header("Key Insights")
insight_card(
    f"🏆 Most efficient mode: <strong>{best_mode['Ship Mode']}</strong> — efficiency score <strong>{best_mode['Efficiency_Score']:.3f}</strong>, avg lead <strong>{best_mode['Avg_Lead_Time']:.1f} days</strong>.",
    "success"
)
insight_card(
    f"⚠️ Slowest mode: <strong>{worst_mode['Ship Mode']}</strong> — avg lead time <strong>{worst_mode['Avg_Lead_Time']:.1f} days</strong>, rank #{int(worst_mode['Rank'])}.",
    "warning"
)
insight_card(
    f"📦 Most used mode: <strong>{mode_df.nlargest(1,'Shipments').iloc[0]['Ship Mode']}</strong> handles <strong>{mode_df['Shipments'].max():,}</strong> shipments.",
    "info"
)

footer()
