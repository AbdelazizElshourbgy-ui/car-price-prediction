import streamlit as st
from utils.theme import render_topbar, apply_page_style
from utils.data_loader import load_clean_data
from utils import charts

apply_page_style("KPI Overview", page_icon="📊")

render_topbar(active="EDA")

st.title("📊 KPI Overview")
st.markdown(
    "<p class='section-caption'>Headline numbers for the full cleaned dataset, "
    "plus 4 of the 10 requested visualizations.</p>",
    unsafe_allow_html=True,
)

df = load_clean_data()

# ---------------------------------------------------------------- KPIs ----
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Sales", f"{len(df):,}")
k2.metric("Total Revenue", f"${df['SellingPrice'].sum():,.0f}")
k3.metric("Avg Selling Price", f"${df['SellingPrice'].mean():,.0f}")
k4.metric("Avg MMR", f"${df['MMR'].mean():,.0f}")
k5.metric("Avg Odometer", f"{df['Odometer'].mean():,.0f} mi")
top_brand = df["Make"].value_counts().idxmax()
k6.metric("Top Brand", top_brand.title())

st.markdown("---")

# ------------------------------------------------------------- Charts -----
c1, c2 = st.columns(2)
with c1:
    with st.container(key="chart_price_distribution"):
        st.plotly_chart(charts.selling_price_distribution(df), use_container_width=True)
with c2:
    with st.container(key="chart_top_brands"):
        st.plotly_chart(charts.top_brands_by_sales(df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    with st.container(key="chart_top_states"):
        st.plotly_chart(charts.top_states_by_sales(df), use_container_width=True)
with c4:
    with st.container(key="chart_monthly"):
        st.plotly_chart(charts.monthly_sales_trend(df), use_container_width=True)
