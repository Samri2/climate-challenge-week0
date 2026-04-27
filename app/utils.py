import pandas as pd
import numpy as np
from scipy import stats
import os
import streamlit as st

@st.cache_data
def load_data(countries: list[str], data_dir: str = None) -> pd.DataFrame:
    """
    Optimized data loader with correct path sequence.
    """
    if data_dir is None:
        # 1. Define the script path FIRST
        current_script = os.path.abspath(__file__) 
        
        # 2. Get the folder this script is in (the 'app' folder)
        app_folder = os.path.dirname(current_script)
        
        # 3. Go up one level to the project root
        project_root = os.path.dirname(app_folder)
        
        # 4. Point to the notebooks/data directory
        data_dir = os.path.join(project_root, "notebooks", "data")
        
    # Check if directory exists for debugging
    if not os.path.exists(data_dir):
        st.error(f"Directory not found: {data_dir}")
        return pd.DataFrame()

    # Mapping friendly names to your specific cleaned CSV files
    file_map = {
        "Ethiopia": os.path.join(data_dir, "ethiopia_clean.csv"),
        "Kenya": os.path.join(data_dir, "kenya_clean.csv"),
        "Nigeria": os.path.join(data_dir, "nigeria_clean.csv"),
        "Sudan": os.path.join(data_dir, "sudan_clean.csv"),
        "Tanzania": os.path.join(data_dir, "tanzania_clean.csv"),
    }
    
    # Core columns for Climate Analysis
    core_cols = ["Date", "YEAR", "T2M", "T2M_MAX", "PRECTOTCORR", "RH2M"]
    dtype_dict = {col: "float32" for col in ["T2M", "T2M_MAX", "PRECTOTCORR", "RH2M"]}

    frames = []
    for country in countries:
        path = file_map.get(country)
        if path and os.path.exists(path):
            # parse_dates is crucial for time-series charts
            df = pd.read_csv(path, usecols=core_cols, parse_dates=["Date"], dtype=dtype_dict)
            df["Country"] = country
            frames.append(df)
            
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def run_anova(df: pd.DataFrame, metric: str = "T2M") -> dict:
    """
    Performs One-way ANOVA to check if climate differences are statistically significant.
    """
    if df.empty or len(df["Country"].unique()) < 2:
        return {"f_stat": 0, "p_value": 1.0}
    
    groups = []
    for country in df["Country"].unique():
        country_data = df[df["Country"] == country][metric].dropna()
        # Cap data size for performance
        if len(country_data) > 50000:
            country_data = country_data.sample(50000, random_state=42)
        groups.append(country_data.values)
    
    f_stat, p_value = stats.f_oneway(*groups)
    return {"f_stat": round(f_stat, 4), "p_value": p_value}

def filter_by_date(df: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """Helper to filter the master dataframe by the slider's date range."""
    if df.empty:
        return df
    mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
    return df.loc[mask]