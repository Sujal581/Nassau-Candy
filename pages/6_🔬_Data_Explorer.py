import streamlit as st
import pandas as pd
import plotly.express as px
from style import (inject_css, sidebar_brand, page_header, section_header,
                   kpi_card, chart_label, insight_card, apply_plot_layout, footer, COLORS, COLOR_SEQ)
from data_manager import apply_filters

st.set_page_config(page_title="Data Explorer | Nassau Candy", layout="wide", page_icon="🔬",initial_sidebar_state="expanded")
inject_css()
sidebar_brand()

df = apply_filters()
page_header("Data Explorer", "Interactive analytics laboratory — explore, filter, and export your data", "🔬")

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

total_rows = len(df)
total_cols = df.shape[1]
missing = df.isnull().sum().sum()
missing_pct = (missing / (total_rows * total_cols)) * 100

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Total Records",  f"{total_rows:,}",         icon="📋", color=COLORS["cyan"])
kpi_card(c2, "Columns",        f"{total_cols}",            icon="📐", color=COLORS["blue"])
kpi_card(c3, "Missing Values", f"{missing:,}",             icon="⚠️", color=COLORS["amber"])
kpi_card(c4, "Data Quality",   f"{100-missing_pct:.1f}%",  icon="✅", color=COLORS["green"])

tab1, tab2, tab3, tab4 = st.tabs(["Data Table", "Column Analysis", "Correlation", "Statistics"])

with tab1:
    section_header("Interactive Data Table")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        search_col = st.selectbox("Search Column", ["None"] + list(df.columns))
    with col_b:
        search_term = st.text_input("Search Value", "")
    with col_c:
        rows_to_show = st.selectbox("Rows to Display", [50, 100, 250, 500, 1000], index=1)

    display_df = df.copy()
    if search_col != "None" and search_term:
        display_df = display_df[
            display_df[search_col].astype(str).str.contains(search_term, case=False, na=False)
        ]

    st.dataframe(display_df.head(rows_to_show), use_container_width=True, height=440)
    insight_card(
        f"Showing <strong>{min(rows_to_show, len(display_df)):,}</strong> of "
        f"<strong>{len(display_df):,}</strong> matching records.", "info"
    )

    st.download_button(
        "Download Filtered Data",
        data=display_df.to_csv(index=False),
        file_name="nassau_filtered_data.csv",
        mime="text/csv"
    )

with tab2:
    section_header("Column-Level Analysis")
    col_select = st.selectbox("Select Column", list(df.columns))

    if col_select:
        series = df[col_select].dropna()
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.markdown(f"""
                <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                            border-radius:10px;padding:1rem;">
                    <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">Type</div>
                    <div style="font-size:1rem;color:#00F5FF;font-weight:700;">{series.dtype}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_info2:
            st.markdown(f"""
                <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                            border-radius:10px;padding:1rem;">
                    <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">Unique Values</div>
                    <div style="font-size:1rem;color:#8B5CF6;font-weight:700;">{series.nunique():,}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_info3:
            missing_col = df[col_select].isnull().sum()
            st.markdown(f"""
                <div style="background:rgba(17,24,39,0.8);border:1px solid rgba(0,245,255,0.1);
                            border-radius:10px;padding:1rem;">
                    <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem;">Missing</div>
                    <div style="font-size:1rem;color:#F59E0B;font-weight:700;">{missing_col:,}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if pd.api.types.is_numeric_dtype(series):
            fig_dist = px.histogram(
                df, x=col_select, nbins=40,
                color_discrete_sequence=[COLORS["cyan"]],
                marginal="box"
            )
            fig_dist.update_traces(marker_line_color="rgba(7,11,20,0.8)", marker_line_width=1)
            apply_plot_layout(fig_dist, 380)
            st.plotly_chart(fig_dist, use_container_width=True)

            stats = series.describe()
            stat_cols = st.columns(4)
            labels = ["Mean", "Std Dev", "Min", "Max"]
            values = [f"{stats['mean']:.2f}", f"{stats['std']:.2f}",
                      f"{stats['min']:.2f}", f"{stats['max']:.2f}"]
            colors = [COLORS["cyan"], COLORS["purple"], COLORS["green"], COLORS["red"]]
            for i, (lbl, val, col_c) in enumerate(zip(labels, values, colors)):
                with stat_cols[i]:
                    st.markdown(f"""
                        <div style="background:rgba(17,24,39,0.8);border-left:3px solid {col_c};
                                    border-radius:8px;padding:0.75rem;text-align:center;">
                            <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;">{lbl}</div>
                            <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;color:{col_c};font-weight:700;margin-top:0.25rem;">{val}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            vc = series.value_counts().head(20).reset_index()
            vc.columns = [col_select, 'Count']
            fig_bar = px.bar(
                vc, x=col_select, y='Count',
                color='Count',
                color_continuous_scale=[[0, '#1a3a5c'], [1, COLORS["cyan"]]]
            )
            fig_bar.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
            apply_plot_layout(fig_bar, 380)
            st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    section_header("Correlation Analysis")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        chart_label("Correlation Matrix", "Pearson correlation between numeric columns")
        corr = df[numeric_cols].corr()
        fig_corr = px.imshow(
            corr, text_auto='.2f',
            color_continuous_scale=[[0, COLORS["red"]], [0.5, '#1a3a5c'], [1, COLORS["cyan"]]],
            zmin=-1, zmax=1
        )
        fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        apply_plot_layout(fig_corr, 480)
        st.plotly_chart(fig_corr, use_container_width=True)

        col_x = st.selectbox("X Axis", numeric_cols, index=0, key="scatter_x")
        col_y = st.selectbox("Y Axis", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")
        if col_x != col_y:
            chart_label(f"{col_x} vs {col_y}", "Scatter relationship")
            color_by = None
            if 'Ship Mode' in df.columns:
                color_by = 'Ship Mode'
            fig_sc = px.scatter(
                df.sample(min(2000, len(df))),
                x=col_x, y=col_y,
                color=color_by,
                color_discrete_sequence=COLOR_SEQ,
                opacity=0.6
            )
            apply_plot_layout(fig_sc, 400)
            st.plotly_chart(fig_sc, use_container_width=True)
    else:
        insight_card("Not enough numeric columns for correlation analysis.", "info")

with tab4:
    section_header("Statistical Summary")
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        stats_display = numeric_df.describe().T
        stats_display = stats_display.round(2)
        st.dataframe(
            stats_display.style
                .background_gradient(cmap='Blues', subset=['mean'])
                .background_gradient(cmap='Oranges', subset=['std'])
                .format('{:.2f}'),
            use_container_width=True, height=400
        )

    section_header("Missing Value Report")
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': df.isnull().sum().values,
        'Missing %': (df.isnull().sum().values / len(df) * 100).round(1)
    }).sort_values('Missing %', ascending=False)
    missing_df = missing_df[missing_df['Missing Count'] > 0]

    if len(missing_df) > 0:
        st.dataframe(
            missing_df.style
                .background_gradient(subset=['Missing %'], cmap='Reds')
                .format({'Missing %': '{:.1f}%'}),
            use_container_width=True
        )
        fig_miss = px.bar(
            missing_df, x='Column', y='Missing %',
            color='Missing %',
            color_continuous_scale=[[0, COLORS["amber"]], [1, COLORS["red"]]]
        )
        fig_miss.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
        apply_plot_layout(fig_miss, 300)
        st.plotly_chart(fig_miss, use_container_width=True)
    else:
        insight_card("No missing values detected. Dataset is complete.", "success")

footer()
