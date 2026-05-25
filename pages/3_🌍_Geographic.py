import streamlit as st
import plotly.express as px
import numpy as np
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS)
from data_manager import apply_filters
from utils import geo_analysis

st.set_page_config(page_title="Geographic | Nassau Candy", layout="wide", page_icon="🌍",initial_sidebar_state="expanded")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Geographic Analysis", "State-level shipping performance and regional intelligence", "🌍")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

geo = geo_analysis(df)
best    = geo.nsmallest(1, 'Avg_Lead_Time').iloc[0]
worst   = geo.nlargest(1, 'Avg_Lead_Time').iloc[0]
top_vol = geo.nlargest(1, 'Shipments').iloc[0]

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "States Covered", f"{len(geo)}",                  icon="🌍", color=COLORS["cyan"])
kpi_card(c2, "Best State",     best['State/Province'],          icon="🏆", color=COLORS["green"])
kpi_card(c3, "Slowest State",  worst['State/Province'],         icon="🐢", color=COLORS["red"])
kpi_card(c4, "Highest Volume", top_vol['State/Province'],       icon="📦", color=COLORS["amber"])

section_header("Lead Time Heatmap — United States")
us_state_abbrev = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO',
    'Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID',
    'Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
    'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
    'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ',
    'New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK',
    'Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD',
    'Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA',
    'West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY',
}
valid_abbrevs = set(us_state_abbrev.values())

def resolve_state_code(val):
    if not isinstance(val, str):
        return None
    v = val.strip()
    if v.upper() in valid_abbrevs:
        return v.upper()
    return us_state_abbrev.get(v.title())

geo_map = geo.copy()
geo_map['Code'] = geo_map['State/Province'].apply(resolve_state_code)
geo_map = geo_map.dropna(subset=['Code'])

# Statebins grid layout — geographic approximation, no geo engine needed
STATE_GRID = {
    'AK': (0, 0),  'ME': (0, 10),
    'VT': (1, 9),  'NH': (1, 10),
    'WA': (2, 0),  'ID': (2, 1),  'MT': (2, 2),  'ND': (2, 3),  'MN': (2, 4),
    'WI': (2, 5),  'MI': (2, 6),  'NY': (2, 8),  'MA': (2, 9),
    'OR': (3, 0),  'NV': (3, 1),  'WY': (3, 2),  'SD': (3, 3),  'IA': (3, 4),
    'IL': (3, 5),  'IN': (3, 6),  'OH': (3, 7),  'PA': (3, 8),  'NJ': (3, 9),  'CT': (3, 10),
    'CA': (4, 0),  'UT': (4, 1),  'CO': (4, 2),  'NE': (4, 3),  'MO': (4, 4),
    'KY': (4, 5),  'WV': (4, 6),  'VA': (4, 7),  'MD': (4, 8),  'DE': (4, 9),  'RI': (4, 10),
    'AZ': (5, 1),  'NM': (5, 2),  'KS': (5, 3),  'AR': (5, 4),  'TN': (5, 5),
    'NC': (5, 6),  'SC': (5, 7),
    'OK': (6, 3),  'LA': (6, 4),  'MS': (6, 5),  'AL': (6, 6),  'GA': (6, 7),  'FL': (6, 8),
    'HI': (7, 0),  'TX': (7, 2),
}

ROWS, COLS = 8, 11
grid_z     = np.full((ROWS, COLS), np.nan)
grid_text  = [['' for _ in range(COLS)] for _ in range(ROWS)]
grid_hover = [['' for _ in range(COLS)] for _ in range(ROWS)]

state_lookup = {
    row['Code']: (row['Avg_Lead_Time'], int(row['Shipments']), row['State/Province'])
    for _, row in geo_map.iterrows()
}

for code, (r, c) in STATE_GRID.items():
    grid_text[r][c] = code
    if code in state_lookup:
        lt, sh, name = state_lookup[code]
        grid_z[r][c] = lt
        grid_hover[r][c] = f'<b>{name} ({code})</b><br>Avg Lead: {lt:.1f} days<br>Shipments: {sh:,}'
    else:
        grid_hover[r][c] = f'<b>{code}</b><br>No data'

# Flip so north (row 0) appears at the top
z_display     = grid_z[::-1].tolist()
text_display  = grid_text[::-1]
hover_display = grid_hover[::-1]

fig_map = go.Figure(go.Heatmap(
    z=z_display,
    text=text_display,
    hovertext=hover_display,
    texttemplate='%{text}',
    textfont=dict(size=10, color='white', family='Inter, sans-serif'),
    colorscale=[
        [0,   '#00e5ff'],
        [0.5, COLORS["amber"]],
        [1,   COLORS["red"]],
    ],
    showscale=True,
    colorbar=dict(
        title=dict(text='Avg Lead (days)', font=dict(color='#94a3b8', size=11)),
        tickfont=dict(color='#94a3b8'),
        bgcolor='rgba(11,17,32,0.85)',
        thickness=14,
    ),
    xgap=4,
    ygap=4,
    hovertemplate='%{hovertext}<extra></extra>',
))

fig_map.update_layout(
    height=430,
    paper_bgcolor='#0B1120',
    plot_bgcolor='#0B1120',
    margin=dict(l=10, r=10, t=10, b=10),
    font=dict(family='Inter, sans-serif', color='#94a3b8'),
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, ticks=''),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, ticks=''),
)

st.plotly_chart(fig_map, use_container_width=True)

if geo_map.empty:
    st.info("No states matched — raw values from your data:")
    st.write(geo[['State/Province']].head(20))

section_header("State Performance Detail")
cl, cr = st.columns([3, 2])
with cl:
    chart_label("Avg Lead Time by State", "Sorted fastest → slowest")
    sorted_geo = geo.sort_values('Avg_Lead_Time')
    fig_bar = px.bar(
        sorted_geo, x='State/Province', y='Avg_Lead_Time',
        color='Avg_Lead_Time',
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
        labels={'Avg_Lead_Time': 'Avg Lead (days)', 'State/Province': ''}
    )
    fig_bar.update_layout(coloraxis_showscale=False, xaxis_tickangle=-45)
    apply_plot_layout(fig_bar, 360)
    st.plotly_chart(fig_bar, use_container_width=True)

with cr:
    chart_label("Volume vs Lead Time", "Bubble = shipment count")
    fig_sc = px.scatter(
        geo, x='Shipments', y='Avg_Lead_Time',
        size='Shipments', color='Avg_Lead_Time',
        hover_name='State/Province',
        color_continuous_scale=[[0, COLORS["green"]], [0.5, COLORS["amber"]], [1, COLORS["red"]]],
        labels={'Avg_Lead_Time': 'Avg Lead (days)'}
    )
    apply_plot_layout(fig_sc, 360)
    st.plotly_chart(fig_sc, use_container_width=True)

section_header("Shipment Volume by State")
chart_label("Top 15 States by Shipment Volume")
top_states = geo.nlargest(15, 'Shipments').sort_values('Shipments')
fig_vol = px.bar(
    top_states, x='Shipments', y='State/Province', orientation='h',
    color='Shipments',
    color_continuous_scale=[[0, '#1a3a5c'], [1, COLORS["cyan"]]]
)
fig_vol.update_layout(coloraxis_showscale=False, yaxis_title="")
apply_plot_layout(fig_vol, 400)
st.plotly_chart(fig_vol, use_container_width=True)

section_header("Performance Tier Classification")
def tier(d):
    if d <= 3:   return "🟢 Excellent"
    elif d <= 5: return "🟡 Good"
    elif d <= 7: return "🟠 Slow"
    else:        return "🔴 Critical"

geo_tbl = geo.copy()
geo_tbl['Tier'] = geo_tbl['Avg_Lead_Time'].apply(tier)
geo_tbl = geo_tbl.sort_values('Avg_Lead_Time')
geo_tbl.columns = ['State', 'Avg Lead (days)', 'Shipments', 'Tier']
st.dataframe(
    geo_tbl.style
        .background_gradient(subset=['Avg Lead (days)'], cmap='YlOrRd')
        .background_gradient(subset=['Shipments'], cmap='Blues')
        .format({'Avg Lead (days)': '{:.1f}'}),
    use_container_width=True, height=320
)
st.download_button(
    "Download Geographic Data",
    data=geo_tbl.to_csv(index=False),
    file_name="nassau_geographic_analysis.csv",
    mime="text/csv"
)

section_header("Key Insights")
critical = geo_tbl[geo_tbl['Tier'] == "🔴 Critical"]
excellent = geo_tbl[geo_tbl['Tier'] == "🟢 Excellent"]
insight_card(
    f"🏆 Fastest state: <strong>{best['State/Province']}</strong> at <strong>{best['Avg_Lead_Time']} days</strong> avg.",
    "success"
)
insight_card(
    f"🐢 Slowest state: <strong>{worst['State/Province']}</strong> at <strong>{worst['Avg_Lead_Time']} days</strong> — review regional routing.",
    "warning"
)
if len(critical):
    insight_card(
        f"🔴 <strong>{len(critical)}</strong> state(s) in Critical tier (>7 days): <strong>{', '.join(critical['State'].tolist())}</strong>.",
        "error"
    )
insight_card(
    f"✅ <strong>{len(excellent)}</strong> state(s) in Excellent tier (≤3 days avg).",
    "info"
)

footer()
