import streamlit as st
import io
import pandas as pd
from style import inject_css, sidebar_brand, page_header, insight_card, footer, kpi_card, section_header
from utils import clean_data, feature_engineering
from data_manager import init_data, apply_filters

st.set_page_config(page_icon="🍪", page_title="Nassau Candy | Dashboard", layout="wide",initial_sidebar_state="expanded")
inject_css()
sidebar_brand()

page_header("Nassau Candy", "Wholesale Intelligence Platform · Shipping & Distribution Analytics", "🍪")

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Products",            "25,000+",      icon="📦", color="#3b82f6")
kpi_card(c2, "Distribution Centers","6 Nationwide", icon="🏭", color="#22c55e")
kpi_card(c3, "Years in Business",   "80+ Years",    icon="📅", color="#f59e0b")
kpi_card(c4, "Global Brands",       "Jelly Belly+", icon="🌍", color="#a855f7")

section_header("Data Setup")

if "master_df" in st.session_state:
    df = st.session_state.master_df
    date_min = df['Order Date'].min().strftime("%b %d, %Y") if 'Order Date' in df.columns else "—"
    date_max = df['Order Date'].max().strftime("%b %d, %Y") if 'Order Date' in df.columns else "—"
    insight_card(
        f"✅ <strong>{len(df):,} shipments</strong> loaded · {df.shape[1]} columns · "
        f"Period: <strong>{date_min}</strong> → <strong>{date_max}</strong>. "
        "Use the sidebar to navigate analytics pages.", "success")
    if st.button("↑ Upload Different CSV"):
        del st.session_state.master_df
        st.rerun()
else:
    st.markdown("""
        <div style="background:#1e293b;border:1px dashed #334155;border-radius:14px;
                    padding:2.5rem;text-align:center;margin-bottom:1rem;">
            <div style="font-size:2rem;margin-bottom:0.6rem;">📂</div>
            <div style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.35rem;">Upload Your Shipping Data</div>
            <div style="font-size:0.82rem;color:#475569;">
                Upload <strong style="color:#94a3b8;">Nassau Candy Distributor.csv</strong> to unlock all analytics pages.
            </div>
        </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    if uploaded:
        try:
            df = pd.read_csv(io.BytesIO(uploaded.read()))
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df['Ship Date']  = pd.to_datetime(df['Ship Date'],  errors='coerce')
            df = clean_data(df)
            df = feature_engineering(df)
            st.session_state.master_df = df
            st.rerun()
        except Exception as e:
            st.error(f"Could not parse CSV: {e}")

section_header("About Nassau Candy")
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Brands & Products", "Seasonal", "Distribution"])

with tab1:
    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Product Categories</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.45rem 0;border-bottom:1px solid #1e293b;">🍫 Chocolate & Bulk Candy</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid #1e293b;">🍭 Specialty Sweets & Confectionery</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid #1e293b;">🥤 Gourmet Soda & Beverages</li>
                    <li style="padding:0.45rem 0;border-bottom:1px solid #1e293b;">🌰 Dried Fruits, Nuts & Natural Foods</li>
                    <li style="padding:0.45rem 0;">🧴 Natural Health & Household Care</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with cr:
        st.markdown("""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Manufacturing</h3>
                <p style="color:#94a3b8;font-size:0.875rem;">Nassau Candy operates production facilities in
                <strong style="color:#cbd5e1;">Hicksville, NY</strong> alongside global manufacturing partners.</p>
                <div style="margin-top:0.75rem;padding:0.7rem;background:#0f172a;border-radius:8px;border-left:3px solid #3b82f6;">
                    <div style="font-size:0.78rem;color:#3b82f6;font-weight:700;">Fast Nationwide Delivery</div>
                    <div style="font-size:0.78rem;color:#475569;margin-top:2px;">6 distribution centers ensure industry-leading logistics.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    cl, cr = st.columns(2)
    with cl:
        st.markdown("""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Global Partner Brands</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.4rem 0;border-bottom:1px solid #0f172a;">🟡 Jelly Belly®</li>
                    <li style="padding:0.4rem 0;border-bottom:1px solid #0f172a;">🟤 Godiva®</li>
                    <li style="padding:0.4rem 0;border-bottom:1px solid #0f172a;">🍫 Ghirardelli®</li>
                    <li style="padding:0.4rem 0;">🍬 Lindt®</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with cr:
        st.markdown("""
            <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.25rem;">
                <h3 style="margin-top:0!important;">Exclusive In-House Brands</h3>
                <ul style="color:#94a3b8;list-style:none;padding:0;margin:0;">
                    <li style="padding:0.4rem 0;border-bottom:1px solid #0f172a;">✨ Clever Candy®</li>
                    <li style="padding:0.4rem 0;">🍬 Nancy Adams®</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    cols = st.columns(4)
    for col, (icon, name, desc) in zip(cols, [
        ("🎃","Halloween","Rare & nostalgic collections"),
        ("🎄","Christmas","Premium holiday assortments"),
        ("💘","Valentine's","Gifting-ready selections"),
        ("🐣","Easter","Spring seasonal candy"),
    ]):
        with col:
            st.markdown(f"""
                <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.1rem;text-align:center;">
                    <div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-weight:700;color:#e2e8f0;font-size:0.875rem;">{name}</div>
                    <div style="font-size:0.76rem;color:#475569;margin-top:0.3rem;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
        <div style="background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.25rem;">
            <h3 style="margin-top:0!important;">Nationwide Distribution Network</h3>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;margin-top:0.75rem;">
                <div style="background:#0f172a;border-radius:8px;padding:0.75rem;border:1px solid #1e293b;">
                    <div style="font-size:0.8rem;font-weight:700;color:#22c55e;">✔ Fast Delivery</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">6 centers across the USA</div>
                </div>
                <div style="background:#0f172a;border-radius:8px;padding:0.75rem;border:1px solid #1e293b;">
                    <div style="font-size:0.8rem;font-weight:700;color:#22c55e;">✔ High Availability</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">25,000+ products in stock</div>
                </div>
                <div style="background:#0f172a;border-radius:8px;padding:0.75rem;border:1px solid #1e293b;">
                    <div style="font-size:0.8rem;font-weight:700;color:#22c55e;">✔ Top Logistics</div>
                    <div style="font-size:0.75rem;color:#475569;margin-top:2px;">Industry-leading performance</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

footer()