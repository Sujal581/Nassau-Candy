import streamlit as st
import plotly.express as px
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS, COLOR_SEQ)
from data_manager import apply_filters
from utils import route_analysis

st.set_page_config(page_title="Route Analysis | Nassau Candy", layout="wide", page_icon="🗺️",initial_sidebar_state="expanded")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Route Analysis", "Lead time and delay rate breakdown by origin → destination", "🗺️")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

route_df = route_analysis(df)
best_route  = route_df.nsmallest(1, 'Avg_Lead_Time').iloc[0]
worst_route = route_df.nlargest(1, 'Avg_Lead_Time').iloc[0]
high_delay  = route_df.nlargest(1, 'Delay_Rate').iloc[0]
avg_lead_overall = route_df['Avg_Lead_Time'].mean()

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Total Routes",       f"{len(route_df)}",                     icon="🗺️", color=COLORS["cyan"])
kpi_card(c2, "Fastest Route",      f"{best_route['Avg_Lead_Time']} days",  icon="⚡",  color=COLORS["green"])
kpi_card(c3, "Slowest Route",      f"{worst_route['Avg_Lead_Time']} days", icon="🐢",  color=COLORS["red"])
kpi_card(c4, "Highest Delay Rate", f"{high_delay['Delay_Rate']}%",         icon="⚠️", color=COLORS["amber"])

section_header("Lead Time by Route")
cl, cr = st.columns(2)
with cl:
    chart_label("Top 12 Fastest Routes", "Avg lead time (days)")
    fast = route_df.nsmallest(12, 'Avg_Lead_Time')
    fig = px.bar(fast, x='Avg_Lead_Time', y='Route', orientation='h',
                 color='Avg_Lead_Time',
                 color_continuous_scale=[[0, COLORS["green"]], [1, COLORS["cyan"]]],
                 text='Avg_Lead_Time')
    fig.update_traces(texttemplate='%{text}d', textposition='outside')
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Avg Days")
    apply_plot_layout(fig, 420)
    st.plotly_chart(fig, use_container_width=True)

with cr:
    chart_label("Top 12 Slowest Routes", "Avg lead time (days)")
    slow = route_df.nlargest(12, 'Avg_Lead_Time').sort_values('Avg_Lead_Time')
    fig2 = px.bar(slow, x='Avg_Lead_Time', y='Route', orientation='h',
                  color='Avg_Lead_Time',
                  color_continuous_scale=[[0, COLORS["amber"]], [1, COLORS["red"]]],
                  text='Avg_Lead_Time')
    fig2.update_traces(texttemplate='%{text}d', textposition='outside')
    fig2.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Avg Days")
    apply_plot_layout(fig2, 420)
    st.plotly_chart(fig2, use_container_width=True)

section_header("Delay Rate Analysis")
chart_label("Routes by Delay Rate", "Top 10 most delayed routes")
fig3 = px.bar(
    route_df.nlargest(10, 'Delay_Rate').sort_values('Delay_Rate'),
    x='Delay_Rate', y='Route', orientation='h',
    color='Delay_Rate',
    color_continuous_scale=[[0, COLORS["amber"]], [1, COLORS["red"]]],
    text='Delay_Rate'
)
fig3.update_traces(texttemplate='%{text}%', textposition='outside')
fig3.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Delay Rate (%)")
apply_plot_layout(fig3, 360)
st.plotly_chart(fig3, use_container_width=True)

section_header("Route Volume vs Performance")
chart_label("Shipment Count vs Avg Lead Time", "Bubble size = total shipments")
fig4 = px.scatter(
    route_df.head(30), x='Avg_Lead_Time', y='Delay_Rate',
    size='Total_Shipments', color='Avg_Lead_Time',
    hover_name='Route',
    color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
    labels={'Avg_Lead_Time': 'Avg Lead (days)', 'Delay_Rate': 'Delay Rate (%)'}
)
apply_plot_layout(fig4, 420)
st.plotly_chart(fig4, use_container_width=True)

section_header("Full Route Ranking Table")
display = route_df.copy()
display.columns = ['Route', 'Avg Lead (days)', 'Total Shipments', 'Delay Rate (%)']
display = display.sort_values('Avg Lead (days)')
st.dataframe(
    display.style
        .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
        .background_gradient(subset=['Delay Rate (%)'], cmap='Reds')
        .background_gradient(subset=['Total Shipments'], cmap='Blues')
        .format({'Avg Lead (days)': '{:.0f}', 'Delay Rate (%)': '{:.0f}%'}),
    use_container_width=True, height=380
)
st.download_button(
    "Download Route Data",
    data=display.to_csv(index=False),
    file_name="nassau_route_analysis.csv",
    mime="text/csv"
)

section_header("Key Insights")
insight_card(
    f"⚡ Fastest route: <strong>{best_route['Route']}</strong> at <strong>{best_route['Avg_Lead_Time']} days</strong> avg lead time.",
    "success"
)
insight_card(
    f"🐢 Slowest route: <strong>{worst_route['Route']}</strong> at <strong>{worst_route['Avg_Lead_Time']} days</strong> — investigate carrier delays.",
    "warning"
)
insight_card(
    f"🔴 Highest delay route: <strong>{high_delay['Route']}</strong> with <strong>{high_delay['Delay_Rate']}%</strong> delayed shipments.",
    "error"
)
insight_card(
    f"📊 Portfolio average: <strong>{avg_lead_overall:.1f} days</strong> across all <strong>{len(route_df)}</strong> active routes.",
    "info"
)

footer()
