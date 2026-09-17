"""
Model training pipeline.

Training utility for the saved estimators. It can train Linear Regression,
Decision Tree, Random Forest, and optional boosted candidates on
`log(SellingPrice)`. The dashboard ships with a fixed benchmark results table
matching the project reference results.

Hyperparameters below are fixed (not grid-searched) so training stays fast
inside the Streamlit app; swap in your own `RandomizedSearchCV` blocks
(same as the notebook) if you want the tuned versions.

Run standalone:  python -m data_prep.train_models
Produces (under models/):
    preprocessor.joblib   -> dict with encoders, scaler, feature column order
    <model_name>.joblib   -> one file per trained model
    results.csv           -> comparison table (Train/Test R2, MAE, RMSE)
"""

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
RANDOM_STATE = 42

CATEGORICAL_ONEHOT = ["Make", "Body", "Transmission", "State", "Color", "Interior"]
DROP_COLS = ["SaleDate", "Id", "VIN", "Year", "SaleMonth", "SaleYear"]


def build_features(df_clean: pd.DataFrame):
    """Reproduce the notebook's encoding steps. Returns (X, y_log, meta)."""
    df = df_clean.copy()

    df = pd.get_dummies(df, columns=CATEGORICAL_ONEHOT, drop_first=True, dtype=int)

    drop_cols = [c for c in DROP_COLS if c in df.columns]
    df.drop(columns=drop_cols, inplace=True)

    le_model = LabelEncoder()
    le_seller = LabelEncoder()
    df["Model"] = le_model.fit_transform(df["Model"].astype(str))
    df["Seller"] = le_seller.fit_transform(df["Seller"].astype(str))

    model_mmr_mean = df.groupby("Model")["MMR"].mean()
    df["MMR_log"] = np.log(df["MMR"] / df["Model"].map(model_mmr_mean))
    df["SellingPrice_log"] = np.log(df["SellingPrice"])

    X = df.drop(columns=["SellingPrice", "SellingPrice_log", "Odometer", "MMR"])
    y = df["SellingPrice_log"]

    meta = {
        "le_model": le_model,
        "le_seller": le_seller,
        "feature_columns": list(X.columns),
        "onehot_source_cols": CATEGORICAL_ONEHOT,
        "model_mmr_mean": model_mmr_mean,          # keyed by label-encoded Model id
        "global_mmr_mean": float(df["MMR"].mean()),
        "category_values": {
            col: sorted(df_clean[col].dropna().unique().tolist())
            for col in CATEGORICAL_ONEHOT
        },
    }
    return X, y, meta


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    results = {
        "Model": model_name,
        "Train_R2": r2_score(y_train, y_train_pred),
        "Train_MAE": mean_absolute_error(y_train, y_train_pred),
        "Train_RMSE": np.sqrt(mean_squared_error(y_train, y_train_pred)),
        "Test_R2": r2_score(y_test, y_test_pred),
        "Test_MAE": mean_absolute_error(y_test, y_test_pred),
        "Test_RMSE": np.sqrt(mean_squared_error(y_test, y_test_pred)),
    }
    return model, results


def _boosted_candidates():
    """The gradient-boosting candidates, only for whichever of
    xgboost/lightgbm are actually importable in this environment."""
    extra = []
    if HAS_XGB:
        extra.append(("XGBoost", XGBRegressor(
            n_estimators=300, max_depth=8, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE
        )))
    if HAS_LGBM:
        extra.append(("LightGBM", LGBMRegressor(
            n_estimators=300, max_depth=8, learning_rate=0.05, num_leaves=63,
            subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE,
            n_jobs=-1, verbose=-1
        )))
    return extra


def train_all(df_clean: pd.DataFrame):
    X, y, meta = build_features(df_clean)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    scale_cols = [
        c for c in X_train.select_dtypes(include=["int64", "float64"]).columns
        if X_train[c].nunique() > 2
    ]
    scaler = RobustScaler()
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[scale_cols] = scaler.fit_transform(X_train[scale_cols])
    X_test[scale_cols] = scaler.transform(X_test[scale_cols])

    meta["scale_cols"] = scale_cols
    meta["scaler"] = scaler

    candidates = [
        ("Linear Regression", LinearRegression()),
        ("Decision Tree", DecisionTreeRegressor(
            max_depth=12, min_samples_leaf=10, min_samples_split=10, random_state=RANDOM_STATE
        )),
        ("Random Forest", RandomForestRegressor(
            n_estimators=200, max_depth=15, min_samples_leaf=5,
            max_features="sqrt", n_jobs=-1, random_state=RANDOM_STATE
        )),
    ] + _boosted_candidates()

    trained_models = {}
    all_results = []
    for name, model in candidates:
        fitted, results = evaluate_model(model, X_train, X_test, y_train, y_test, name)
        trained_models[name] = fitted
        all_results.append(results)

    results_df = pd.DataFrame(all_results).sort_values("Test_R2", ascending=False).reset_index(drop=True)
    return trained_models, results_df, meta, (X_train, X_test, y_train, y_test)


def save_artifacts(trained_models, results_df, meta):
    os.makedirs(MODELS_DIR, exist_ok=True)
    for name, model in trained_models.items():
        safe_name = name.lower().replace(" ", "_")
        joblib.dump(model, os.path.join(MODELS_DIR, f"{safe_name}.joblib"))
    joblib.dump(meta, os.path.join(MODELS_DIR, "preprocessor.joblib"))
    results_df.to_csv(os.path.join(MODELS_DIR, "results.csv"), index=False)


def missing_candidate_names(models_dir: str = MODELS_DIR) -> list:
    """Names of boosted candidates (XGBoost/LightGBM) that are importable in
    this environment but not yet present in models_dir/results.csv. Cheap --
    only reads results.csv, never touches the dataset. Returns [] if there
    are no saved artifacts yet at all (that's a job for train_all/save_artifacts,
    not this incremental path)."""
    results_path = os.path.join(models_dir, "results.csv")
    if not os.path.exists(results_path):
        return []
    existing = set(pd.read_csv(results_path)["Model"])
    available = {name for name, _ in _boosted_candidates()}
    return sorted(available - existing)


def train_missing_models(df_clean: pd.DataFrame, models_dir: str = MODELS_DIR) -> list:
    """Train only the boosted candidates that are supported here (packages
    installed) but missing from models_dir, reusing the *already fitted*
    encoders/scaler from preprocessor.joblib so results stay directly
    comparable with whatever models are already saved -- existing
    models/rows are left untouched. This is what lets `pip install xgboost
    lightgbm` + rerunning the app "just add" those two to an existing
    3-model results table, no full retrain or manual cleanup needed.
    Returns the list of model names that were added (empty if nothing to
    do, or if there are no existing artifacts to extend)."""
    to_add = missing_candidate_names(models_dir)
    if not to_add:
        return []

    preproc_path = os.path.join(models_dir, "preprocessor.joblib")
    results_path = os.path.join(models_dir, "results.csv")
    meta = joblib.load(preproc_path)
    results_df = pd.read_csv(results_path)

    df = df_clean.copy()
    df = pd.get_dummies(df, columns=CATEGORICAL_ONEHOT, drop_first=True, dtype=int)
    drop_cols = [c for c in DROP_COLS if c in df.columns]
    df.drop(columns=drop_cols, inplace=True)
    df["Model"] = meta["le_model"].transform(df["Model"].astype(str))
    df["Seller"] = meta["le_seller"].transform(df["Seller"].astype(str))
    df["MMR_log"] = np.log(df["MMR"] / df["Model"].map(meta["model_mmr_mean"]))
    df["SellingPrice_log"] = np.log(df["SellingPrice"])

    X = df.reindex(columns=meta["feature_columns"], fill_value=0)
    y = df["SellingPrice_log"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    scale_cols = meta["scale_cols"]
    scaler = meta["scaler"]
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[scale_cols] = scaler.transform(X_train[scale_cols])
    X_test[scale_cols] = scaler.transform(X_test[scale_cols])

    candidates = dict(_boosted_candidates())
    added = []
    new_rows = []
    for name in to_add:
        fitted, results = evaluate_model(
            candidates[name], X_train, X_test, y_train, y_test, name
        )
        safe_name = name.lower().replace(" ", "_")
        joblib.dump(fitted, os.path.join(models_dir, f"{safe_name}.joblib"))
        new_rows.append(results)
        added.append(name)

    results_df = pd.concat([results_df, pd.DataFrame(new_rows)], ignore_index=True)
    results_df = results_df.sort_values("Test_R2", ascending=False).reset_index(drop=True)
    results_df.to_csv(results_path, index=False)
    return added


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(__file__))
    from clean_pipeline import clean_data

    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_vehicle_sales.csv")
    clean_path = os.path.join(os.path.dirname(__file__), "..", "data", "vehicle_sales_clean.csv")
    if os.path.exists(clean_path):
        clean = pd.read_csv(clean_path, parse_dates=["SaleDate"])
    else:
        raw = pd.read_csv(raw_path)
        clean = clean_data(raw)
        clean.to_csv(clean_path, index=False)
    models, results, meta, splits = train_all(clean)
    print(results)
    save_artifacts(models, results, meta)
    print("Saved artifacts to", MODELS_DIR)
