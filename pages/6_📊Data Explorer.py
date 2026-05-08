import streamlit as st
import pandas as pd
import plotly.express as px

from style import (
    inject_css,
    sidebar_brand,
    page_header,
    section_header,
    kpi_card,
    chart_label,
    insight_card,
    apply_plot_layout,
    footer,
    COLORS,
    COLOR_SEQ
)

from data_manager import apply_filters


# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Explorer | Nassau Candy",
    layout="wide",
    page_icon="🔍"
)

inject_css()
sidebar_brand()

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
df = apply_filters()

if df is None:
    st.warning("Please upload a dataset from the Home page.")
    st.stop()

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────
page_header(
    "Data Explorer",
    "Raw data inspection, outlier detection, and custom analysis",
    "🔍"
)

# ─────────────────────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────────────────────
numeric_cols = df.select_dtypes(include='number').columns.tolist()

cat_cols = (
    df.select_dtypes(
        include=['object', 'category']
    )
    .columns
    .tolist()
)

c1, c2, c3, c4 = st.columns(4)

kpi_card(
    c1,
    "Total Rows",
    f"{len(df):,}",
    icon="📋",
    color=COLORS["blue"]
)

kpi_card(
    c2,
    "Total Columns",
    f"{df.shape[1]}",
    icon="📐",
    color=COLORS["cyan"]
)

kpi_card(
    c3,
    "Numeric Columns",
    f"{len(numeric_cols)}",
    icon="🔢",
    color=COLORS["green"]
)

kpi_card(
    c4,
    "Categorical Cols",
    f"{len(cat_cols)}",
    icon="🏷️",
    color=COLORS["purple"]
)

# ─────────────────────────────────────────────────────────────
# DISTRIBUTION ANALYSIS
# ─────────────────────────────────────────────────────────────
section_header("Distribution Analysis")

cl, cr = st.columns(2)

with cl:

    chart_label(
        "Lead Time Histogram",
        "Distribution of days from order to ship"
    )

    fig = px.histogram(
        df,
        x='Lead Time',
        nbins=30,
        color_discrete_sequence=[
            COLORS["blue"]
        ]
    )

    fig.update_traces(
        marker_line_color="#0f172a",
        marker_line_width=1
    )

    fig.update_xaxes(title="Days")
    fig.update_yaxes(title="Count")

    apply_plot_layout(fig, 300)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with cr:

    chart_label(
        "Lead Time by Ship Mode",
        "Box plot showing spread and outliers"
    )

    fig2 = px.box(
        df,
        x='Ship Mode',
        y='Lead Time',
        color='Ship Mode',
        color_discrete_sequence=COLOR_SEQ,
        labels={
            'Lead Time': 'Days',
            'Ship Mode': ''
        }
    )

    fig2.update_layout(showlegend=False)

    apply_plot_layout(fig2, 300)

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ─────────────────────────────────────────────────────────────
# CUSTOM EXPLORATION
# ─────────────────────────────────────────────────────────────
section_header("Custom Exploration")

cl2, cr2 = st.columns([2, 1])

# ─── CONFIG PANEL ────────────────────────────────────────────
with cr2:

    chart_label("Configure Chart")

    x_col = st.selectbox(
        "Metric",
        numeric_cols,
        index=0
    )

    clr_col = st.selectbox(
        "Group By",
        cat_cols,
        index=0 if cat_cols else None
    )

    chart_t = st.selectbox(
        "Chart Type",
        [
            "Bar",
            "Line",
            "Area",
            "Pie"
        ]
    )

# ─── CHART AREA ──────────────────────────────────────────────
with cl2:

    chart_label(f"{chart_t} Analysis")

    try:

        # ─────────────────────────────────────────
        # BAR CHART
        # ─────────────────────────────────────────
        if chart_t == "Bar":

            agg = (
                df.groupby(clr_col)[x_col]
                .mean()
                .reset_index()
                .sort_values(
                    by=x_col,
                    ascending=False
                )
                .head(15)
            )

            fig3 = px.bar(
                agg,
                x=clr_col,
                y=x_col,
                color=clr_col,
                color_discrete_sequence=COLOR_SEQ,
                text_auto=".2f"
            )

            fig3.update_layout(
                showlegend=False
            )

        # ─────────────────────────────────────────
        # LINE CHART
        # ─────────────────────────────────────────
        elif chart_t == "Line":

            agg = (
                df.groupby(
                    df['Order Date']
                    .dt.to_period('M')
                )[x_col]
                .mean()
                .reset_index()
            )

            agg['Order Date'] = (
                agg['Order Date']
                .astype(str)
            )

            fig3 = px.line(
                agg,
                x='Order Date',
                y=x_col,
                markers=True,
                color_discrete_sequence=[
                    COLORS["blue"]
                ]
            )

        # ─────────────────────────────────────────
        # AREA CHART
        # ─────────────────────────────────────────
        elif chart_t == "Area":

            agg = (
                df.groupby(
                    df['Order Date']
                    .dt.to_period('M')
                )[x_col]
                .sum()
                .reset_index()
            )

            agg['Order Date'] = (
                agg['Order Date']
                .astype(str)
            )

            fig3 = px.area(
                agg,
                x='Order Date',
                y=x_col,
                color_discrete_sequence=[
                    COLORS["cyan"]
                ]
            )

        # ─────────────────────────────────────────
        # PIE CHART
        # ─────────────────────────────────────────
        else:

            agg = (
                df.groupby(clr_col)[x_col]
                .sum()
                .reset_index()
                .sort_values(
                    by=x_col,
                    ascending=False
                )
                .head(10)
            )

            fig3 = px.pie(
                agg,
                names=clr_col,
                values=x_col,
                hole=0.35
            )

        apply_plot_layout(fig3, 340)

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    except Exception as e:

        st.warning(
            f"Could not render chart: {e}"
        )

# ─────────────────────────────────────────────────────────────
# COLUMN STATISTICS
# ─────────────────────────────────────────────────────────────
section_header("Column Statistics")

tab1, tab2 = st.tabs([
    "Numeric Columns",
    "Categorical Columns"
])

# ─── NUMERIC STATS ───────────────────────────────────────────
with tab1:

    desc = (
        df[numeric_cols]
        .describe()
        .T
        .round(2)
    )

    desc.columns = [
        'Count',
        'Mean',
        'Std',
        'Min',
        '25%',
        '50%',
        '75%',
        'Max'
    ]

    st.dataframe(
        desc.style.background_gradient(
            cmap='Blues',
            subset=['Mean']
        ),
        use_container_width=True
    )

# ─── CATEGORICAL STATS ───────────────────────────────────────
with tab2:

    cat_stats = pd.DataFrame({
        'Column': cat_cols,
        'Unique': [
            df[c].nunique()
            for c in cat_cols
        ],
        'Most Common': [
            df[c].mode()[0]
            if not df[c].empty else '—'
            for c in cat_cols
        ],
        'Nulls': [
            df[c].isna().sum()
            for c in cat_cols
        ],
    })

    st.dataframe(
        cat_stats,
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# OUTLIER DETECTION
# ─────────────────────────────────────────────────────────────
section_header("Outlier Detection — Lead Time")

q1, q3 = df['Lead Time'].quantile([0.25, 0.75])

iqr = q3 - q1

upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

outliers = df[
    (df['Lead Time'] < lower) |
    (df['Lead Time'] > upper)
]

cl3, cr3 = st.columns([2, 1])

with cl3:

    chart_label(
        "Lead Time with Outlier Bounds"
    )

    fig_out = px.scatter(
        df.reset_index(),
        x='index',
        y='Lead Time',
        color='Delayed',
        color_discrete_sequence=[
            COLORS["green"],
            COLORS["red"]
        ],
        opacity=0.6,
        labels={'index': 'Row Index'}
    )

    fig_out.add_hline(
        y=upper,
        line_dash="dash",
        line_color=COLORS["amber"],
        annotation_text="Upper Bound"
    )

    fig_out.add_hline(
        y=lower,
        line_dash="dash",
        line_color=COLORS["cyan"],
        annotation_text="Lower Bound"
    )

    apply_plot_layout(fig_out, 320)

    st.plotly_chart(
        fig_out,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with cr3:

    st.markdown("<br>", unsafe_allow_html=True)

    kpi_card(
        cr3,
        "Outlier Shipments",
        f"{len(outliers):,}",
        icon="⚠️",
        color=COLORS["red"]
    )

    insight_card(
        f"IQR: <strong>{iqr:.1f} days</strong>"
        f" · Upper fence: "
        f"<strong>{upper:.1f}</strong>",
        "info"
    )

    if len(outliers) > 0:

        insight_card(
            f"<strong>{len(outliers):,}</strong> "
            "shipments fall outside IQR bounds.",
            "warning"
        )

# ─────────────────────────────────────────────────────────────
# RAW DATA VIEWER
# ─────────────────────────────────────────────────────────────
section_header("Raw Data")

with st.expander(
    "View data table",
    expanded=False
):

    display_df = df.copy()

    # Format dates
    for col in ['Order Date', 'Ship Date']:

        if col in display_df.columns:

            display_df[col] = pd.to_datetime(
                display_df[col],
                errors='coerce'
            ).dt.strftime('%Y-%m-%d')

    cols_to_show = st.multiselect(
        "Select columns to display",
        display_df.columns.tolist(),
        default=display_df.columns.tolist()[:8]
    )

    n_rows = st.slider(
        "Rows to preview",
        10,
        500,
        100
    )

    if cols_to_show:

        st.dataframe(
            display_df[cols_to_show]
            .head(n_rows),
            use_container_width=True
        )

    st.download_button(
        "⬇ Download Filtered Data",
        data=display_df.to_csv(index=False),
        file_name="nassau_candy_filtered.csv",
        mime="text/csv"
    )

# ─────────────────────────────────────────────────────────────
# INSIGHTS
# ─────────────────────────────────────────────────────────────
section_header("Key Insights")

insight_card(
    f"📊 Dataset contains "
    f"<strong>{len(df):,} rows</strong> "
    f"and <strong>{df.shape[1]} columns</strong> "
    f"after filters.",
    "info"
)

insight_card(
    f"⚠️ <strong>{len(outliers):,}</strong> "
    f"lead-time outliers detected.",
    "warning" if len(outliers) > 0 else "success"
)

null_pct = (
    df.isnull()
    .mean()
    .max()
    * 100
)

if null_pct > 5:

    insight_card(
        f"🔴 Maximum null rate: "
        f"<strong>{null_pct:.1f}%</strong>",
        "error"
    )

else:

    insight_card(
        f"✅ Data quality looks good "
        f"(<strong>{null_pct:.1f}%</strong> max null rate).",
        "success"
    )

footer()