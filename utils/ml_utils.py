import os
import joblib
import pandas as pd
import streamlit as st

from utils.inference import build_inference_row, predict_price, error_band_for_model  # noqa: F401

_ROOT = os.path.join(os.path.dirname(__file__), "..")
MODELS_DIR = os.path.join(_ROOT, "models")
RESULTS_PATH = os.path.join(MODELS_DIR, "results.csv")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.joblib")


def _artifacts_exist() -> bool:
    return os.path.exists(RESULTS_PATH) and os.path.exists(PREPROCESSOR_PATH)


def _train_and_save():
    import sys
    sys.path.append(_ROOT)
    from data_prep.train_models import train_all, save_artifacts
    from utils.data_loader import load_clean_data

    df_clean = load_clean_data()
    models, results_df, meta, _ = train_all(df_clean)
    save_artifacts(models, results_df, meta)


def _add_missing_boosted_models():
    """If XGBoost/LightGBM are installed in this environment but the saved
    models/results.csv predate that (e.g. they were only installed after
    the first run), train just those two and append them -- no need to
    delete anything or retrain Linear Regression/Decision Tree/Random
    Forest. Cheap no-op if there's nothing to add."""
    import sys
    sys.path.append(_ROOT)
    from data_prep.train_models import missing_candidate_names, train_missing_models

    if not missing_candidate_names(MODELS_DIR):
        return

    from utils.data_loader import load_clean_data
    df_clean = load_clean_data()
    train_missing_models(df_clean, MODELS_DIR)


@st.cache_resource(show_spinner="Training models (first run only, this can take a minute)...")
def load_models_and_results():
    if not _artifacts_exist():
        _train_and_save()
    # Keep the shipped benchmark results stable. Optional boosted models are
    # only loaded when their saved estimator files are present.

    meta = joblib.load(PREPROCESSOR_PATH)
    results_df = pd.read_csv(RESULTS_PATH)

    models = {}
    for name in results_df["Model"]:
        safe_name = name.lower().replace(" ", "_")
        path = os.path.join(MODELS_DIR, f"{safe_name}.joblib")
        # The benchmark table uses the label "Random Forest (Best)", while
        # the saved estimator keeps the simpler filename random_forest.joblib.
        if not os.path.exists(path) and name == "Random Forest (Best)":
            path = os.path.join(MODELS_DIR, "random_forest.joblib")
        if os.path.exists(path):
            models[name] = joblib.load(path)

    return models, results_df, meta


def best_model_name(results_df: pd.DataFrame) -> str:
    return results_df.sort_values("Test_R2", ascending=False).iloc[0]["Model"]
