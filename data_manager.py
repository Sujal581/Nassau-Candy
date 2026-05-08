import streamlit as st
import pandas as pd
import io
from utils import clean_data, feature_engineering


# ─────────────────────────────────────────────────────────────
# FAST CSV PARSER + CACHE
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _parse_csv(raw_bytes: bytes) -> pd.DataFrame:

    df = pd.read_csv( io.BytesIO(raw_bytes), low_memory=False)

    # Date conversion
    for col in ['Order Date', 'Ship Date']:
        if col in df.columns: df[col] = pd.to_datetime( df[col], errors='coerce')

    # Memory optimization
    categorical_cols = ['Ship Mode', 'State/Province','Country/Region', 'City','Category','Sub-Category']

    for col in categorical_cols:
        if col in df.columns: df[col] = df[col].astype('category')

    # Cleaning
    df = clean_data(df)

    # Feature engineering
    df = feature_engineering(df)

    # Remove empty rows
    df = df.dropna(how="all")

    return df

# ─────────────────────────────────────────────────────────────
# UPLOAD SCREEN
# ─────────────────────────────────────────────────────────────
def upload_screen():

    st.markdown("""
        <div style="background:#1e293b; border:1px dashed #334155; border-radius:14px; padding:3rem; text-align:center; max-width:520px; margin:3rem auto;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">📂 </div>
            <div style="font-size:1rem; font-weight:700; color:#f1f5f9; margin-bottom:0.4rem;">Upload Shipping Data</div>
            <div style="font-size:0.82rem; color:#94a3b8;">Upload Nassau Candy Distributor.csv to unlock all analytics pages.</div>
        </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    if uploaded:
        try: 
            with st.spinner("Processing dataset..."):
                raw_bytes = uploaded.read()
                df = _parse_csv(raw_bytes)
                # Store globally
                st.session_state.master_df = df
                # Optional filename
                st.session_state.file_name = uploaded.name
            st.success("Dataset loaded successfully")
            st.rerun()
        except Exception as e:
            st.error(f"Could not parse CSV: {e}")
    st.stop()
# ─────────────────────────────────────────────────────────────
# INITIALIZE DATA
# ─────────────────────────────────────────────────────────────
def init_data():
    return st.session_state.get("master_df", None)
# ─────────────────────────────────────────────────────────────
# GLOBAL FILTERS
# ─────────────────────────────────────────────────────────────
def apply_filters():
    df = st.session_state.get("master_df", None)
    # IMPORTANT
    # Do NOT show upload screen here
    if df is None:
        return None
    # ─── SIDEBAR FILTERS ───────────────────────────────
    with st.sidebar:
        st.markdown("""
            <div style="font-size:0.7rem; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.6rem;">🔍 Global Filters</div>
        """, unsafe_allow_html=True)
        # Default states
        defaults = { "state": "All", "mode": "All", "delay": 5, "reset": False}
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        # Date defaults
        if "start_date" not in st.session_state:
            st.session_state.start_date = (
                df['Order Date'].min().date()
            )
        if "end_date" not in st.session_state:
            st.session_state.end_date = (
                df['Order Date'].max().date()
            )
        # Reset filters
        if st.session_state.reset:
            st.session_state.start_date = (
                df['Order Date'].min().date()
            )
            st.session_state.end_date = (
                df['Order Date'].max().date()
            )
            st.session_state.state = "All"
            st.session_state.mode = "All"
            st.session_state.delay = 5
            st.session_state.reset = False

        # ─── FILTER UI ─────────────────────────────────
        st.date_input( "📅 Start Date", key="start_date")
        st.date_input("📅 End Date",key="end_date")
        states = (
            ["All"] +
            sorted(
                df['State/Province']
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )
        modes = (
            ["All"] +
            sorted(
                df['Ship Mode']
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )
        st.selectbox("🌍 State / Province", states, key="state")
        st.selectbox( "🚚 Ship Mode",modes, key="mode")
        st.slider("⏱ Delay Threshold (days)", 1, 15, key="delay")
        st.markdown("<br>", unsafe_allow_html=True)
        # Reset button
        if st.button(
            "🔄 Reset Filters",
            use_container_width=True
        ):
            st.session_state.reset = True
            st.rerun()
        st.markdown("""
            <hr style='border-color:#1e293b;margin:0.75rem 0;'>
        """, unsafe_allow_html=True)
        # Upload new file
        if st.button(
            "↑ Upload New CSV",
            use_container_width=True
        ):
            keys_to_remove = [
                "master_df",
                "file_name",
                "start_date",
                "end_date",
                "state",
                "mode",
                "delay"
            ]
            for key in keys_to_remove:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # ─── APPLY FILTERS ─────────────────────────────────

    filtered = df
    # Date filtering
    try:
        start = pd.Timestamp(
            st.session_state.start_date
        )
        end = pd.Timestamp(
            st.session_state.end_date
        )
        filtered = filtered[
            (filtered['Order Date'] >= start) &
            (filtered['Order Date'] <= end)
        ]
    except Exception:
        pass
    # State filter
    if st.session_state.state != "All":
        filtered = filtered[
            filtered['State/Province']
            == st.session_state.state
        ]
    # Ship mode filter
    if st.session_state.mode != "All":
        filtered = filtered[
            filtered['Ship Mode']
            == st.session_state.mode
        ]
    # Delayed flag
    if "Lead Time" in filtered.columns:
        filtered = filtered.copy()
        filtered['Delayed'] = (
            filtered['Lead Time']
            > st.session_state.delay
        )
    return filtered

# ─────────────────────────────────────────────────────────────
# CLEAR CACHE
# ─────────────────────────────────────────────────────────────
def clear_cache():
    st.cache_data.clear()
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]
    st.success("Cache cleared")
    st.rerun()