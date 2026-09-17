import numpy as np
import pandas as pd


def build_inference_row(user_input: dict, meta: dict) -> pd.DataFrame:
    """Build a single-row, correctly-encoded & scaled feature DataFrame for
    one prediction, mirroring `data_prep/train_models.py::build_features`."""
    feature_columns = meta["feature_columns"]
    row = {col: 0 for col in feature_columns}

    row["ConditionValue"] = float(user_input["ConditionValue"])
    row["car_age"] = int(user_input["car_age"])

    model_id = int(meta["le_model"].transform([user_input["Model"]])[0])
    seller_id = int(meta["le_seller"].transform([user_input["Seller"]])[0])
    row["Model"] = model_id
    row["Seller"] = seller_id

    mmr_mean = meta["model_mmr_mean"].get(model_id, meta["global_mmr_mean"])
    row["MMR_log"] = float(np.log(max(user_input["MMR"], 1) / mmr_mean))

    for col in meta["onehot_source_cols"]:
        dummy_col = f"{col}_{user_input[col]}"
        if dummy_col in row:
            row[dummy_col] = 1
        # if not present, the value is the reference/baseline category
        # dropped by drop_first=True -> leaving all zeros is correct.

    df_row = pd.DataFrame([row], columns=feature_columns)

    scale_cols = meta["scale_cols"]
    df_row[scale_cols] = meta["scaler"].transform(df_row[scale_cols])
    return df_row


def predict_price(model, meta: dict, user_input: dict) -> float:
    df_row = build_inference_row(user_input, meta)
    log_pred = model.predict(df_row)[0]
    return float(np.exp(log_pred))


def error_band_for_model(results_df: pd.DataFrame, model_name: str, predicted_price: float):
    """Approximate a +/- price range around a prediction using that model's
    Test MAE in log space (a simple, interpretable proxy for typical error)."""
    row = results_df[results_df["Model"] == model_name].iloc[0]
    mae_log = float(row["Test_MAE"])
    low = predicted_price * np.exp(-mae_log)
    high = predicted_price * np.exp(mae_log)
    return low, high, float(row["Test_R2"]), float(row["Test_MAE"]), float(row["Test_RMSE"])
