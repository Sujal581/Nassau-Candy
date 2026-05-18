import streamlit as st
import pandas as pd
import plotly.express as px
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout,
                   footer, COLORS, COLOR_SEQ)
from data_manager import apply_filters

st.set_page_config(page_title="Factory & Division | Nassau Candy", layout="wide", page_icon="🏭")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Factory & Division Analysis", "Origin division performance — volume, lead time, and delay risk", "🏭")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

if 'Division' not in df.columns:
    st.warning("The dataset does not contain a 'Division' column.")
    st.stop()

div_df = (
    df.groupby('Division')
    .agg(
        Shipments=('Order ID', 'count'),
        Avg_Lead=('Lead Time', 'mean'),
        Delay_Rate=('Delayed', 'mean'),
        States=('State/Province', 'nunique')
    )
    .reset_index()
)
div_df['Avg_Lead']   = div_df['Avg_Lead'].round(1)
div_df['Delay_Rate'] = (div_df['Delay_Rate'] * 100).round(1)
div_df['Risk_Score'] = (div_df['Avg_Lead'] * 0.5 + div_df['Delay_Rate'] * 0.5).round(1)

best_div  = div_df.nsmallest(1, 'Avg_Lead').iloc[0]
worst_div = div_df.nlargest(1, 'Avg_Lead').iloc[0]
high_vol  = div_df.nlargest(1, 'Shipments').iloc[0]
high_risk = div_df.nlargest(1, 'Risk_Score').iloc[0]

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Divisions",      f"{len(div_df)}",           icon="🏭",  color=COLORS["cyan"])
kpi_card(c2, "Best Division",  best_div['Division'],        icon="🏆",  color=COLORS["green"])
kpi_card(c3, "Highest Volume", high_vol['Division'],        icon="📦",  color=COLORS["blue"])
kpi_card(c4, "Highest Risk",   high_risk['Division'],       icon="⚠️", color=COLORS["red"])

section_header("Division Performance")
cl, cr = st.columns(2)

with cl:
    chart_label("Avg Lead Time by Division")
    fig = px.bar(
        div_df.sort_values('Avg_Lead'),
        x='Division', y='Avg_Lead',
        color='Avg_Lead',
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
        text='Avg_Lead',
        labels={'Avg_Lead': 'Avg Lead (days)', 'Division': ''}
    )
    fig.update_traces(texttemplate='%{text:.1f}d', textposition='outside')
    fig.update_layout(coloraxis_showscale=False)
    apply_plot_layout(fig, 340)
    st.plotly_chart(fig, use_container_width=True)

with cr:
    chart_label("Shipment Volume by Division")
    fig2 = px.pie(
        div_df, names='Division', values='Shipments',
        color_discrete_sequence=COLOR_SEQ, hole=0.55
    )
    fig2.update_traces(
        textinfo='percent+label',
        marker=dict(line=dict(color='rgba(7,11,20,0.8)', width=2))
    )
    apply_plot_layout(fig2, 340)
    st.plotly_chart(fig2, use_container_width=True)

section_header("Risk & Delay Analysis")
cl2, cr2 = st.columns(2)

with cl2:
    chart_label("Delay Rate by Division", "% shipments delayed")
    fig3 = px.bar(
        div_df.sort_values('Delay_Rate', ascending=False),
        x='Division', y='Delay_Rate',
        color='Delay_Rate',
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
        text='Delay_Rate',
        labels={'Delay_Rate': 'Delay Rate (%)', 'Division': ''}
    )
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.update_layout(coloraxis_showscale=False)
    apply_plot_layout(fig3, 340)
    st.plotly_chart(fig3, use_container_width=True)

with cr2:
    chart_label("Risk Score Matrix", "Composite of lead time + delay rate")
    fig4 = px.scatter(
        div_df, x='Avg_Lead', y='Delay_Rate',
        size='Shipments', color='Risk_Score',
        hover_name='Division', text='Division',
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
        labels={'Avg_Lead': 'Avg Lead (days)', 'Delay_Rate': 'Delay Rate (%)'}
    )
    fig4.update_traces(textposition='top center', textfont_size=10)
    apply_plot_layout(fig4, 340)
    st.plotly_chart(fig4, use_container_width=True)

section_header("Monthly Lead Time Trend by Division")
chart_label("Division Performance Over Time")
df_copy = df.copy()
df_copy['Order Date'] = pd.to_datetime(df_copy['Order Date'], errors='coerce')
monthly_div = (
    df_copy.groupby([pd.Grouper(key='Order Date', freq='ME'), 'Division'])['Lead Time']
    .mean()
    .reset_index()
)
monthly_div = monthly_div.dropna(subset=['Order Date'])
monthly_div['Month'] = monthly_div['Order Date'].dt.strftime('%b %Y')

fig5 = px.line(
    monthly_div, x='Month', y='Lead Time', color='Division',
    markers=True, color_discrete_sequence=COLOR_SEQ,
    labels={'Lead Time': 'Avg Lead (days)', 'Month': ''}
)
fig5.update_traces(line=dict(width=2.5), marker=dict(size=7))
apply_plot_layout(fig5, 340)
st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

section_header("States Served by Division")
chart_label("Geographic Reach per Division")
fig_states = px.bar(
    div_df.sort_values('States', ascending=False),
    x='Division', y='States',
    color='States',
    color_continuous_scale=[[0, '#1a3a5c'], [1, COLORS["cyan"]]],
    text='States',
    labels={'States': 'States Served', 'Division': ''}
)
fig_states.update_traces(texttemplate='%{text}', textposition='outside')
fig_states.update_layout(coloraxis_showscale=False)
apply_plot_layout(fig_states, 300)
st.plotly_chart(fig_states, use_container_width=True)

section_header("Division Summary Table")
def risk_tier(r):
    if r < 25:   return "🟢 Low"
    elif r < 50: return "🟡 Medium"
    elif r < 75: return "🟠 High"
    else:        return "🔴 Critical"

display = div_df.copy()
display['Risk Tier'] = display['Risk_Score'].apply(risk_tier)
display.columns = ['Division', 'Shipments', 'Avg Lead (days)', 'Delay Rate (%)', 'States Served', 'Risk Score', 'Risk Tier']
st.dataframe(
    display.style
        .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
        .background_gradient(subset=['Delay Rate (%)'], cmap='Reds')
        .background_gradient(subset=['Shipments'], cmap='Blues')
        .format({'Avg Lead (days)': '{:.1f}', 'Delay Rate (%)': '{:.1f}%', 'Risk Score': '{:.1f}'}),
    use_container_width=True, height=280
)
st.download_button(
    "Download Division Data",
    data=display.to_csv(index=False),
    file_name="nassau_division_analysis.csv",
    mime="text/csv"
)

section_header("Key Insights")
critical_divs = display[display['Risk Tier'] == "🔴 Critical"]
insight_card(
    f"🏆 Best-performing division: <strong>{best_div['Division']}</strong> — avg lead time <strong>{best_div['Avg_Lead']:.1f} days</strong>.",
    "success"
)
insight_card(
    f"⚠️ Slowest division: <strong>{worst_div['Division']}</strong> — avg <strong>{worst_div['Avg_Lead']:.1f} days</strong>. Investigate factory throughput or scheduling.",
    "warning"
)
insight_card(
    f"⚠️ Highest risk division: <strong>{high_risk['Division']}</strong> — composite risk score <strong>{high_risk['Risk_Score']:.1f}</strong>.",
    "error" if high_risk['Risk_Score'] > 50 else "warning"
)
if len(critical_divs):
    insight_card(
        f"🔴 <strong>{len(critical_divs)}</strong> division(s) in Critical risk tier: <strong>{', '.join(critical_divs['Division'].tolist())}</strong>.",
        "error"
    )

footer()
