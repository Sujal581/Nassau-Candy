import streamlit as st
import plotly.express as px
import pandas as pd
from data_manager import apply_filters
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS)
from utils import route_analysis, ship_mode_analysis

st.set_page_config(page_title="Overview | Nassau Candy", layout="wide", page_icon="📊")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Overview Dashboard", "High-level shipping performance across all routes and regions", "📊")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

total = len(df)
avg_lead = df['Lead Time'].mean()
delayed_pct = df['Delayed'].mean() * 100
on_time = 100 - delayed_pct
routes = df['Route'].nunique() if 'Route' in df.columns else 0
states = df['State/Province'].nunique() if 'State/Province' in df.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpi_card(c1, "Total Shipments", f"{total:,}",           icon="📦", color=COLORS["cyan"])
kpi_card(c2, "Avg Lead Time",   f"{avg_lead:.1f}d",     icon="⏱",  color=COLORS["blue"])
kpi_card(c3, "On-Time Rate",    f"{on_time:.1f}%",      icon="✅",  color=COLORS["green"])
kpi_card(c4, "Delayed Rate",    f"{delayed_pct:.1f}%",  icon="⚠️", color=COLORS["amber"])
kpi_card(c5, "Active Routes",   f"{routes}",            icon="🗺️", color=COLORS["purple"])
kpi_card(c6, "States Covered",  f"{states}",            icon="🌍",  color=COLORS["pink"])

section_header("Shipment Volume Over Time")
cl, cr = st.columns([3, 2])
with cl:
    chart_label("Monthly Shipment Volume", "Orders placed per month")
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).size().reset_index(name='Shipments')
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    fig = px.area(monthly, x='Order Date', y='Shipments',
                  color_discrete_sequence=[COLORS["cyan"]])
    fig.update_traces(fillcolor="rgba(0,245,255,0.08)", line=dict(width=2))
    fig.update_xaxes(title="")
    fig.update_yaxes(title="")
    apply_plot_layout(fig, 320)
    st.plotly_chart(fig, use_container_width=True)

with cr:
    chart_label("On-Time vs Delayed", "Overall shipment status split")
    pie_df = pd.DataFrame({
        "Status": ["On-Time", "Delayed"],
        "Count": [df['Delayed'].eq(False).sum(), df['Delayed'].sum()]
    })
    fig2 = px.pie(pie_df, names='Status', values='Count',
                  color_discrete_sequence=[COLORS["green"], COLORS["red"]], hole=0.6)
    fig2.update_traces(
        textfont_size=12, textinfo='percent+label',
        marker=dict(line=dict(color='rgba(7,11,20,0.8)', width=2))
    )
    apply_plot_layout(fig2, 320)
    st.plotly_chart(fig2, use_container_width=True)

section_header("Lead Time & Route Breakdown")
cl2, cr2 = st.columns(2)
with cl2:
    chart_label("Lead Time Distribution", "Days from order to shipment")
    fig3 = px.histogram(df, x='Lead Time', nbins=30,
                        color_discrete_sequence=[COLORS["blue"]])
    fig3.update_traces(marker_line_color="rgba(7,11,20,0.8)", marker_line_width=1)
    apply_plot_layout(fig3, 300)
    st.plotly_chart(fig3, use_container_width=True)

with cr2:
    chart_label("Top Routes by Volume", "Shipment count per route")
    if 'Route' in df.columns:
        route_vol = df.groupby('Route').size().nlargest(8).reset_index(name='Shipments')
        fig4 = px.bar(route_vol, x='Shipments', y='Route', orientation='h',
                      color='Shipments',
                      color_continuous_scale=[[0, '#1e3a5f'], [1, COLORS["cyan"]]])
        fig4.update_layout(coloraxis_showscale=False, yaxis_title="")
        apply_plot_layout(fig4, 300)
        st.plotly_chart(fig4, use_container_width=True)

section_header("Performance by Ship Mode")
sm = ship_mode_analysis(df)
cl3, cr3 = st.columns([2, 3])
with cl3:
    fig_sm = px.bar(sm.sort_values('Avg_Lead_Time'), x='Ship Mode', y='Avg_Lead_Time',
                    color='Delay_Rate',
                    color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
                    text='Avg_Lead_Time',
                    labels={'Avg_Lead_Time': 'Avg Lead (days)'})
    fig_sm.update_traces(texttemplate='%{text:.1f}d', textposition='outside')
    fig_sm.update_layout(coloraxis_showscale=False)
    apply_plot_layout(fig_sm, 300)
    st.plotly_chart(fig_sm, use_container_width=True)

with cr3:
    sm_display = sm.copy()
    sm_display.columns = ['Ship Mode', 'Avg Lead (days)', 'Shipments', 'Delay Rate (%)']
    st.dataframe(
        sm_display.style
            .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
            .format({'Avg Lead (days)': '{:.1f}', 'Delay Rate (%)': '{:.1f}%'}),
        use_container_width=True, height=260
    )

section_header("State Performance Summary")
state_df = df.groupby('State/Province').agg(
    Shipments=('Order ID', 'count'),
    Avg_Lead=('Lead Time', 'mean'),
    Delay_Rate=('Delayed', 'mean')
).reset_index()
state_df['Avg_Lead'] = state_df['Avg_Lead'].round(1)
state_df['Delay_Rate'] = (state_df['Delay_Rate'] * 100).round(1)
state_df.columns = ['State', 'Shipments', 'Avg Lead (days)', 'Delay Rate (%)']
state_df = state_df.sort_values('Avg Lead (days)')
st.dataframe(
    state_df.style
        .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
        .background_gradient(subset=['Delay Rate (%)'], cmap='Reds')
        .format({'Avg Lead (days)': '{:.1f}', 'Delay Rate (%)': '{:.1f}%'}),
    use_container_width=True, height=320
)

section_header("Key Insights")
best = state_df.nsmallest(1, 'Avg Lead (days)').iloc[0]
worst = state_df.nlargest(1, 'Avg Lead (days)').iloc[0]
insight_card(
    f"🏆 Best-performing state: <strong>{best['State']}</strong> — avg <strong>{best['Avg Lead (days)']:.1f} days</strong>.",
    "success"
)
insight_card(
    f"⚠️ Slowest state: <strong>{worst['State']}</strong> — avg <strong>{worst['Avg Lead (days)']:.1f} days</strong>. Consider reviewing regional carrier agreements.",
    "warning"
)
if delayed_pct > 30:
    insight_card(
        f"🔴 Overall delay rate <strong>{delayed_pct:.1f}%</strong> exceeds 30% — investigate systemic bottlenecks.",
        "error"
    )
else:
    insight_card(
        f"✅ Overall delay rate <strong>{delayed_pct:.1f}%</strong> is within an acceptable threshold.",
        "info"
    )
insight_card(
    f"📦 Dataset spans <strong>{df['Order Date'].min().strftime('%b %Y')}</strong> → "
    f"<strong>{df['Order Date'].max().strftime('%b %Y')}</strong> covering "
    f"<strong>{states}</strong> states and <strong>{routes}</strong> unique routes.",
    "info"
)

footer()
