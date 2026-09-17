import streamlit as st
from utils.theme import render_topbar, apply_page_style
from utils.data_loader import load_clean_data
from utils import charts

apply_page_style("Car Analysis", page_icon="🚗")

render_topbar(active="Car Analysis")

st.title("🚗 Car Analysis")
st.markdown(
    "<p class='section-caption'>The remaining 6 of the 10 requested visualizations — "
    "pricing by brand, transmission, body type, and relationships between price, "
    "age, mileage, and MMR.</p>",
    unsafe_allow_html=True,
)

df = load_clean_data()

c1, c2 = st.columns(2)
with c1:
    with st.container(key="chart_avg_brand"):
        st.plotly_chart(charts.avg_price_by_top_brands(df), use_container_width=True)
with c2:
    with st.container(key="chart_transmission"):
        st.plotly_chart(charts.price_by_transmission(df), use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    with st.container(key="chart_body"):
        st.plotly_chart(charts.price_by_body_type(df), use_container_width=True)
with c4:
    with st.container(key="chart_age"):
        st.plotly_chart(charts.car_age_vs_price(df), use_container_width=True)

c5, c6 = st.columns(2)
with c5:
    with st.container(key="chart_odometer"):
        st.plotly_chart(charts.odometer_vs_price(df), use_container_width=True)
with c6:
    with st.container(key="chart_mmr"):
        st.plotly_chart(charts.mmr_vs_price(df), use_container_width=True)
