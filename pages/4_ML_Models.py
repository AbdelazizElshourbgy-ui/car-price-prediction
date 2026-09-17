import streamlit as st
import plotly.graph_objects as go
from utils.theme import render_topbar, apply_page_style, PLOTLY_LAYOUT, MAIN_COLOR, ACCENT_COLOR
from utils.ml_utils import load_models_and_results, best_model_name

apply_page_style("ML Models", page_icon="🤖")

render_topbar(active="ML Models")

st.title("🤖 ML Models")
st.markdown(
    "<p class='section-caption'>Five regressors are compared on the cleaned vehicle-sales data: "
    "Linear Regression, Decision Tree, Random Forest, XGBoost, and LightGBM. The reported "
    "metrics below are the project benchmark results on the same train/test split.</p>",
    unsafe_allow_html=True,
)

models, results_df, meta = load_models_and_results()
best_name = best_model_name(results_df)
best_row = results_df[results_df["Model"] == best_name].iloc[0]

st.markdown("### Best model")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Best Model", best_name)
k2.metric("Test R²", f"{best_row['Test_R2']:.3f}")
k3.metric("Test MAE (log price)", f"{best_row['Test_MAE']:.3f}")
k4.metric("Test RMSE (log price)", f"{best_row['Test_RMSE']:.3f}")

st.markdown(
    "<p class='section-caption'>The benchmark uses <code>log(SellingPrice)</code>, "
    "so R² is the share of variance in log-price explained by the model, while MAE/RMSE "
    "are average errors on that same log scale (not raw dollars).</p>",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("### Model comparison")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=results_df["Model"], y=results_df["Test_R2"], name="Test R²",
    marker_color=MAIN_COLOR,
    hovertemplate="%{x}<br>Test R²: %{y:.3f}<extra></extra>",
))
fig.update_layout(**PLOTLY_LAYOUT, title="Test R² by Model (higher is better)",
                   yaxis_title="Test R²", xaxis_title="")
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    fig_mae = go.Figure()
    fig_mae.add_trace(go.Bar(
        x=results_df["Model"], y=results_df["Test_MAE"], name="Test MAE",
        marker_color=ACCENT_COLOR,
        hovertemplate="%{x}<br>Test MAE: %{y:.3f}<extra></extra>",
    ))
    fig_mae.update_layout(**PLOTLY_LAYOUT, title="Test MAE by Model (lower is better)", xaxis_title="")
    st.plotly_chart(fig_mae, use_container_width=True)

with c2:
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=results_df["Model"], y=results_df["Train_R2"], name="Train R²", marker_color="#536DFE",
    ))
    fig_gap.add_trace(go.Bar(
        x=results_df["Model"], y=results_df["Test_R2"], name="Test R²", marker_color=MAIN_COLOR,
    ))
    fig_gap.update_layout(**PLOTLY_LAYOUT, title="Train vs Test R² (overfitting check)",
                           barmode="group", xaxis_title="")
    st.plotly_chart(fig_gap, use_container_width=True)

st.markdown("### Full metrics table")
st.dataframe(
    results_df.style.format({
        "Train_R2": "{:.4f}", "Train_MAE": "{:.4f}", "Train_RMSE": "{:.4f}",
        "Test_R2": "{:.4f}", "Test_MAE": "{:.4f}", "Test_RMSE": "{:.4f}",
    }).background_gradient(subset=["Test_R2"], cmap="Blues"),
    use_container_width=True,
)

with st.expander("Which models trained?"):
    st.write(
        "Linear Regression, Decision Tree, and Random Forest always train (scikit-learn). "
        "XGBoost and LightGBM train too if those packages are installed in your "
        "environment — install them (see `requirements.txt`) to include them in the "
        "comparison."
    )
    st.write(f"Models currently loaded: {', '.join(models.keys())}")
