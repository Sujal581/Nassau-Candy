import streamlit as st
import io
import pandas as pd
from utils import clean_data, feature_engineering


@st.cache_data(show_spinner=False)
def _parse_csv(raw_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(raw_bytes), low_memory=False)
    for col in ['Order Date', 'Ship Date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    categorical_cols = ['Ship Mode', 'State/Province', 'Country/Region', 'City',
                        'Category', 'Sub-Category', 'Division']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    df = clean_data(df)
    df = feature_engineering(df)
    df = df.dropna(how="all")
    return df


def init_data():
    return st.session_state.get("master_df", None)


def upload_screen():
    st.markdown("""
        <div style="background:rgba(17,24,39,0.8);border:1px dashed rgba(0,245,255,0.2);
                    border-radius:14px;padding:3rem;text-align:center;max-width:520px;margin:3rem auto;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">📂</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:1rem;font-weight:700;
                        color:#f1f5f9;margin-bottom:0.4rem;">Upload Shipping Data</div>
            <div style="font-size:0.82rem;color:#475569;">
                Upload the Nassau Candy Distributor CSV to unlock all analytics pages.
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
    st.stop()


def apply_filters():
    df = st.session_state.get("master_df", None)
    if df is None:
        return None

    with st.sidebar:
        st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.7rem;font-weight:700;
                        color:#475569;text-transform:uppercase;letter-spacing:0.1em;
                        margin-bottom:0.75rem;">Global Filters</div>
        """, unsafe_allow_html=True)

        defaults = {"state_filter": "All", "mode_filter": "All", "delay_threshold": 5}
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

        if "start_date" not in st.session_state:
            st.session_state.start_date = df['Order Date'].min().date()
        if "end_date" not in st.session_state:
            st.session_state.end_date = df['Order Date'].max().date()

        if st.session_state.get("reset_filters", False):
            st.session_state.start_date = df['Order Date'].min().date()
            st.session_state.end_date = df['Order Date'].max().date()
            st.session_state.state_filter = "All"
            st.session_state.mode_filter = "All"
            st.session_state.delay_threshold = 5
            st.session_state.reset_filters = False

        st.date_input("Start Date", key="start_date")
        st.date_input("End Date", key="end_date")

        states = ["All"] + sorted(df['State/Province'].dropna().astype(str).unique().tolist())
        modes = ["All"] + sorted(df['Ship Mode'].dropna().astype(str).unique().tolist())

        st.selectbox("State / Province", states, key="state_filter")
        st.selectbox("Ship Mode", modes, key="mode_filter")
        st.slider("Delay Threshold (days)", 1, 15, key="delay_threshold")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Reset Filters", use_container_width=True):
            st.session_state.reset_filters = True
            st.rerun()

        st.markdown("""<hr style='border:none;border-top:1px solid rgba(0,245,255,0.1);margin:0.75rem 0;'>""",
                    unsafe_allow_html=True)

        if st.button("Upload New CSV", use_container_width=True):
            for key in ["master_df", "file_name", "start_date", "end_date",
                        "state_filter", "mode_filter", "delay_threshold"]:
                if key in st.session_state:
                    del st.session_state[key]
            _parse_csv.clear()
            st.rerun()

    filtered = df.copy()

    try:
        start = pd.Timestamp(st.session_state.start_date)
        end = pd.Timestamp(st.session_state.end_date)
        filtered = filtered[(filtered['Order Date'] >= start) & (filtered['Order Date'] <= end)]
    except Exception:
        pass

    if st.session_state.state_filter != "All":
        filtered = filtered[filtered['State/Province'].astype(str) == st.session_state.state_filter]

    if st.session_state.mode_filter != "All":
        filtered = filtered[filtered['Ship Mode'].astype(str) == st.session_state.mode_filter]

    if "Lead Time" in filtered.columns:
        filtered['Delayed'] = filtered['Lead Time'] > st.session_state.delay_threshold

    return filtered
