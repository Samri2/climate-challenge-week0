import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
import os
import sys

# Ensure local imports work
curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from utils import load_data, run_anova, filter_by_date

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COP32 Climate Intelligence Dashboard",
    page_icon="🌍",
    layout="wide"
)

# --- TAILWIND-INSPIRED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
    }

    /* Professional Sidebar (Slate-800) */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
    }

    /* KPI Metric Cards with Tailwind Shadows */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8) !important;
       border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(8px);
        padding: 1.5rem !important;
       border-radius: 12px !important;
       box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s ease-in-out !important;;
    }
    /* 2. THE HOVER EFFECT */
    [data-testid="stMetric"]:hover {
        /* This creates the "lift" */
        transform: translateY(-8px) scale(1.02) !important;
        
        /* This makes the shadow deeper as it lifts */
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        
        /* This adds a professional blue border glow on hover */
        border-color: #3b82f6 !important;
    [data-testid="stMetricLabel"] p {
        color: #475569 !important; /* Muted Slate */
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #0f172a !important; /* Deep Navy */
        font-weight: 800 !important;
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* ANOVA and Info Box Styling */
    .stAlert {
        border: none !important;
        background-color: white !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border-left: 5px solid #3b82f6 !important;
        border-radius: 8px !important;
    }
/* 5. TABS - PRO LOOK */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
    /* Clean Table Styling */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_t, col_l = st.columns([4, 1])
with col_t:
    st.title("🌍 COP32 Climate Vulnerability Hub")
    st.markdown("**Evidence-based policy insights for the 32nd Conference of the Parties.**")

st.divider()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Analysis Filters")
    
    selected_countries = st.multiselect(
        "Compare Nations",
        options=["Ethiopia", "Kenya", "Nigeria", "Sudan", "Tanzania"],
        default=["Ethiopia", "Sudan"] # Added default for immediate view
    )

    selected_metric = st.selectbox(
        "Climate Variable",
        options=["T2M", "PRECTOTCORR", "RH2M", "T2M_MAX"],
        format_func=lambda x: {"T2M": "Avg Temperature", "PRECTOTCORR": "Precipitation", 
                               "RH2M": "Humidity", "T2M_MAX": "Peak Heat"}[x]
    )

    start_init = datetime(2015, 1, 1)
    end_init = datetime(2026, 12, 31)
    date_range = st.slider("Time Horizon", min_value=start_init, max_value=end_init, 
                           value=(start_init, end_init), format="YYYY")

# --- DATA LOADING ---
if not selected_countries:
    st.warning("Please select at least one country to begin.")
    st.stop()

with st.spinner("Processing Climate Records..."):
    df_raw = load_data(selected_countries)
    
    if df_raw.empty:
        st.error("No cleaned data found! Please check notebooks/data/ folder.")
        st.stop()
        
    df = filter_by_date(df_raw, date_range[0].date(), date_range[1].date())

# --- KPI SECTION ---
st.subheader("Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)

# Dynamic labeling for metrics
metric_label = {"T2M": "°C", "PRECTOTCORR": "mm", "RH2M": "%", "T2M_MAX": "°C"}[selected_metric]

k1.metric(f"Average {selected_metric}", f"{df[selected_metric].mean():.2f} {metric_label}")
k2.metric(f"Peak {selected_metric}", f"{df[selected_metric].max():.2f}")
k3.metric("Data Points", f"{len(df):,}")
k4.metric("Risk Lead", df.groupby("Country")[selected_metric].mean().idxmax())

# --- TABS FOR ANALYSIS ---
tab_summary, tab_charts, tab_dist = st.tabs([
    "📝 Summary & Stats", "📈 Time Series Explorer", "📊 Variance Analysis"
])

# -- TAB 1: SUMMARY & ANOVA (The Requested Change) --
with tab_summary:
    st.markdown("### 📊 Descriptive Statistics")
    # Generating summary directly for clean display
    summary = df.groupby("Country")[selected_metric].agg(["mean", "median", "std", "min", "max"]).round(2)
    st.dataframe(summary, use_container_width=True)

    st.divider()
    
    st.markdown("### 🧪 Statistical Significance (ANOVA)")
    with st.container():
        anova_res = run_anova(df, selected_metric)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("F-Statistic", f"{anova_res['f_stat']:.2f}")
        with col_res2:
            p_val = anova_res['p_value']
            st.metric("P-Value", f"{p_val:.4e}")

        if p_val < 0.05:
            st.success(f"**Significant Result:** The variance between {', '.join(selected_countries)} is statistically confirmed at 95% confidence.")
        else:
            st.warning("**Non-Significant:** Climate metrics appear uniform across selected regions.")

# -- TAB 2: TIME SERIES --
with tab_charts:
    st.markdown(f"### {selected_metric} Trend Analysis")
    fig_line = px.line(df, x="Date", y=selected_metric, color="Country", 
                      template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

# -- TAB 3: DISTRIBUTION --
with tab_dist:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Regional Variance (Box Plot)")
        fig_box = px.box(df, x="Country", y=selected_metric, color="Country", 
                         template="plotly_white", points=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col_b:
        st.markdown("### Data Density (Histogram)")
        fig_hist = px.histogram(df, x=selected_metric, color="Country", 
                                barmode="overlay", template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)

# --- FOOTER ---
st.divider()
st.caption(f"COP32 Intelligence Dashboard | Build: {datetime.now().strftime('%Y-%m-%d')} | Data Source: Cleaned NASA POWER Records")