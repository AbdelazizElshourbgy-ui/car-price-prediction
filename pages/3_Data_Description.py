import streamlit as st
from utils.theme import render_topbar, apply_page_style
from utils.data_loader import load_raw_data, load_clean_data

apply_page_style("Data Description", page_icon="📋")

render_topbar(active="Description")

st.title("📋 Data Description")
st.markdown(
    "<p class='section-caption'>What the raw data looked like, and exactly what the "
    "cleaning pipeline did to it before any chart or model saw it.</p>",
    unsafe_allow_html=True,
)

raw = load_raw_data()
clean = load_clean_data()

st.markdown("### Before vs. after cleaning")
b1, b2, b3, b4 = st.columns(4)
b1.metric("Raw rows", f"{len(raw):,}")
b2.metric("Clean rows", f"{len(clean):,}", delta=f"{len(clean) - len(raw):,}")
b3.metric("Raw missing cells", f"{int(raw.isna().sum().sum()):,}")
b4.metric("Clean missing cells", f"{int(clean.isna().sum().sum()):,}")

st.markdown("### Source columns")
st.dataframe(
    raw.dtypes.rename("dtype").to_frame().join(
        raw.isna().sum().rename("missing_values")
    ).join((raw.isna().mean() * 100).round(2).rename("missing_%")),
    use_container_width=True,
)

st.markdown("---")
st.markdown("### Cleaning pipeline — step by step")

steps = [
    ("1. Drop rows with no identity",
     "Rows with a missing `Make` or `Model` are dropped, because the vehicle cannot be reliably analyzed without its identity. The unused `Trim` column is also dropped."),
    ("2. Manual fixes for known edge cases",
     "A short list of specific Make/Model combinations with a known, unambiguous body style is filled directly before the general recovery step."),
    ("3. Recover Body & Transmission from Model text",
     "Model-name substring lookup rules are used to recover missing `Body` and `Transmission` values. Existing non-null values are preserved. Remaining rows without a `VIN` are then removed."),
    ("4. Normalize text and fill numeric/categorical gaps",
     "`Make` and `Model` are lower-cased and stripped. `ConditionValue`, `Odometer`, `MMR`, and `SellingPrice` are filled with group medians (Make+Model, with broader fallbacks). `Color` and `Interior` use the most common value within Make+Model."),
    ("5. Fill remaining Body & Transmission gaps",
     "If `Body` or `Transmission` is still missing after the model-text lookup, the value is filled using the most common value for that Make, with an overall mode as the final fallback."),
    ("6. Normalize Body categories",
     "Body values are stripped and standardized to title case, with `Suv` normalized to `SUV` so equivalent categories are not split across charts or model features."),
    ("7. Parse SaleDate and engineer time features",
     "`SaleDate` is converted to datetime. Missing dates are filled with the most common date for the Make+Model, then the overall mode if needed. `SaleYear`, `SaleMonth`, and `car_age` (`SaleYear − Year`) are derived."),
]

for title, desc in steps:
    with st.container(key=f"glasscard_{title[:2]}"):
        st.markdown(f"**{title}**")
        st.markdown(f"<span style='color:#C7D2E6'>{desc}</span>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Feature engineering for the ML model")
st.markdown("""
Once the data is clean, a second pipeline (see the **ML Models** page) prepares it for
regression:

- **One-hot encoding** — `Make`, `Body`, `Transmission`, `State`, `Color`, `Interior`
  (first category dropped to avoid redundancy).
- **Label encoding** — `Model` and `Seller` (too many categories for one-hot).
- **Log transform** — the target `SellingPrice` is modeled as `log(SellingPrice)` to tame
  its right-skewed distribution; a `MMR_log` feature (`log(MMR / average MMR for that
  model)`) is engineered the same way.
- **Robust scaling** — all remaining numeric, non-binary columns are scaled with
  `RobustScaler` (median/IQR based, less sensitive to outliers than standard scaling).
""")

with st.expander("Preview cleaned dataset"):
    st.dataframe(clean.head(50), use_container_width=True)
