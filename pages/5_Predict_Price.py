import datetime
import plotly.graph_objects as go
import streamlit as st

from utils.theme import render_topbar, apply_page_style, PLOTLY_LAYOUT, MAIN_COLOR, ACCENT_COLOR, PINK_COLOR
from utils.data_loader import load_clean_data
from utils.ml_utils import load_models_and_results, best_model_name
from utils.inference import predict_price, error_band_for_model

apply_page_style("Predict Price", page_icon="🔮")

render_topbar(active="Predict Price")

st.title("🔮 Predict Selling Price")
st.markdown(
    "<p class='section-caption'>Fill in a car's details and get a live price prediction "
    "from any of the trained models, with an approximate error range.</p>",
    unsafe_allow_html=True,
)

df = load_clean_data()
models, results_df, meta = load_models_and_results()
default_best = best_model_name(results_df)

with st.form("predict_form"):
    st.markdown("#### Car details")
    col1, col2, col3 = st.columns(3)

    with col1:
        make = st.selectbox("Make", meta["category_values"]["Make"])
        models_for_make = sorted(df.loc[df["Make"] == make, "Model"].unique().tolist())
        model_name_input = st.selectbox("Model", models_for_make if models_for_make else list(meta["le_model"].classes_))
        body = st.selectbox("Body", meta["category_values"]["Body"])

    with col2:
        transmission = st.selectbox("Transmission", meta["category_values"]["Transmission"])
        state = st.selectbox("State", meta["category_values"]["State"])
        color = st.selectbox("Color", meta["category_values"]["Color"])

    with col3:
        interior = st.selectbox("Interior", meta["category_values"]["Interior"])
        seller = st.selectbox("Seller", sorted(meta["le_seller"].classes_))
        condition = st.slider("Condition (0.5 = poor, 5.0 = excellent)", 0.5, 5.0, 3.5, 0.1)

    st.markdown("#### Sale context")
    col4, col5, col6 = st.columns(3)
    with col4:
        year = st.number_input("Manufacture Year", min_value=1990, max_value=datetime.date.today().year,
                                value=2012, step=1)
    with col5:
        sale_year = st.number_input("Sale Year", min_value=1990, max_value=datetime.date.today().year + 1,
                                     value=datetime.date.today().year, step=1)
    with col6:
        mmr = st.number_input("MMR (Manheim Market Report value, $)", min_value=100, max_value=200000,
                               value=12000, step=100)

    # Use the best-performing trained model automatically; no model-selection field.
    model_choice = default_best if default_best in models else next(iter(models))

    submitted = st.form_submit_button("Predict price", use_container_width=True)

if submitted:
    car_age = max(int(sale_year) - int(year), 0)
    user_input = {
        "Make": make, "Model": model_name_input, "Body": body, "Transmission": transmission,
        "State": state, "Color": color, "Interior": interior, "Seller": seller,
        "ConditionValue": condition, "MMR": mmr, "car_age": car_age,
    }

    model = models[model_choice]
    predicted_price = predict_price(model, meta, user_input)
    low, high, r2, mae, rmse = error_band_for_model(results_df, model_choice, predicted_price)

    st.markdown("---")
    st.markdown("### Result")

    r1, r2_col, r3 = st.columns(3)
    r1.metric("Predicted Selling Price", f"${predicted_price:,.0f}")
    r2_col.metric("Typical range", f"${low:,.0f} – ${high:,.0f}")
    r3.metric(f"{model_choice} · Test R²", f"{r2:.3f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Low estimate", "Predicted price", "High estimate"],
        y=[low, predicted_price, high],
        marker_color=[ACCENT_COLOR, MAIN_COLOR, PINK_COLOR],
        text=[f"${low:,.0f}", f"${predicted_price:,.0f}", f"${high:,.0f}"],
        textposition="outside",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=f"Predicted price with typical error range — {model_choice}",
        yaxis_title="Price ($)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"<p class='section-caption'>The range above is the model's typical error "
        f"(± average error on the test set, converted from the log-price scale back to "
        f"dollars) — not a statistical confidence interval. <b>{model_choice}</b> explains "
        f"about <b>{r2*100:.1f}%</b> of the variance in log-price on unseen test data, "
        f"with an average error of <b>{mae:.3f}</b> (MAE) and <b>{rmse:.3f}</b> (RMSE) on "
        f"that same log scale.</p>",
        unsafe_allow_html=True,
    )

    if mmr:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=["Your MMR input", "Predicted Selling Price"],
            y=[mmr, predicted_price],
            marker_color=[ACCENT_COLOR, MAIN_COLOR],
            text=[f"${mmr:,.0f}", f"${predicted_price:,.0f}"],
            textposition="outside",
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, title="Predicted price vs. MMR you entered", yaxis_title="Price ($)")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Fill in the form above and click **Predict price** to see a result.")
