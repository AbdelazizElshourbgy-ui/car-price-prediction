import os
import streamlit as st
import pandas as pd

_ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW_PATH = os.path.join(_ROOT, "data", "raw_vehicle_sales.csv")
CLEAN_PATH = os.path.join(_ROOT, "data", "vehicle_sales_clean.csv")


def _ensure_data():
    """Build the cleaned dataset (data/vehicle_sales_clean.csv) from the real
    raw data (data/raw_vehicle_sales.csv, sourced from VehicleSales.csv) the
    first time it's needed. Does NOT fall back to synthetic data -- if the raw
    file is missing, this raises so the problem is obvious instead of
    silently training on fake data.
    """
    if os.path.exists(CLEAN_PATH):
        return

    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(
            f"Raw data file not found at {RAW_PATH}. Place VehicleSales.csv "
            f"there (renamed to raw_vehicle_sales.csv) before running the app."
        )

    import sys
    sys.path.append(_ROOT)
    from data_prep.clean_pipeline import clean_data

    os.makedirs(os.path.join(_ROOT, "data"), exist_ok=True)
    raw = pd.read_csv(RAW_PATH)
    clean = clean_data(raw)
    clean.to_csv(CLEAN_PATH, index=False)


@st.cache_data(show_spinner="Loading dataset...")
def load_clean_data() -> pd.DataFrame:
    _ensure_data()
    df = pd.read_csv(CLEAN_PATH, parse_dates=["SaleDate"])
    return df


@st.cache_data(show_spinner="Loading raw dataset...")
def load_raw_data() -> pd.DataFrame:
    _ensure_data()
    df = pd.read_csv(RAW_PATH, parse_dates=["SaleDate"])
    return df
