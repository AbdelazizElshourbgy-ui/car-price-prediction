# 🚗 Car Sales Intelligence Dashboard

An interactive Streamlit dashboard for used-car price analysis and machine-learning prediction,
wrapped in a dark, neon-themed multi-page app. It includes the dataset cleaning pipeline,
10 visualizations, five trained regression models, live price prediction, and a generated report.

## Dashboard Preview

![Car Price Prediction Dashboard](assets/readme_home.png)

## Pages

| Page | What it shows |
|---|---|
| **Home** | Hero image + icon navigation to every section |
| **📊 KPI Overview** | Headline metrics + 4 of the 10 charts |
| **🚗 Car Analysis** | The remaining 6 charts |
| **📋 Data Description** | Step-by-step explanation of the cleaning pipeline, with live before/after stats |
| **🤖 ML Models** | Best model, full metric comparison, Train vs Test R² (overfitting check) |
| **🔮 Predict Price** | Fill in a car's details, get a live price prediction + error range |
| **📄 Report** | Auto-composed written summary, downloadable as Markdown / PDF |

## Quick start

```bash
pip install -r requirements.txt
streamlit run Home.py
```

`data/raw_vehicle_sales.csv` already contains the real `VehicleSales.csv`
dataset (548,434 cleaned rows after the pipeline runs), and
`data/vehicle_sales_clean.csv` / `models/*.joblib` are pre-built from it, so
the app loads instantly — no synthetic data, no first-run wait.

If you ever need to rebuild from scratch (e.g. after editing the cleaning or
training logic, or swapping in a newer export):
1. Delete `data/vehicle_sales_clean.csv` and everything under `models/`.
2. Run `streamlit run Home.py` — the cleaning pipeline
   (`data_prep/clean_pipeline.py`) and the training pipeline
   (`data_prep/train_models.py`) will run automatically against
   `data/raw_vehicle_sales.csv` and re-cache their output.

To point the app at a *different* export later, just overwrite
`data/raw_vehicle_sales.csv` with a CSV that has these columns: `Id, VIN,
Year, Make, Model, Trim, Body, Transmission, State, ConditionValue, Odometer,
Color, Interior, Seller, MMR, SellingPrice, SaleDate`, then do the delete +
rerun above.

**Note on models/**: this repo ships five trained models — `XGBoost`, `LightGBM`,
`Random Forest (Best)`, `Decision Tree`, and `Linear Regression` — together with
the preprocessor and `models/results.csv`. The metrics shown in the app are the
saved results from these trained models.


## Project structure

```
Home.py                          # Landing page (hero + icon navigation)
pages/
  1_KPI_Overview.py
  2_Car_Analysis.py
  3_Data_Description.py
  4_ML_Models.py
  5_Predict_Price.py
  6_Report.py
utils/
  theme.py                       # Colors, CSS, hero banner
  data_loader.py                 # Cached CSV loading (auto-generates on first run)
  charts.py                      # The 10 Plotly chart builders
  ml_utils.py                    # Cached model loading/training (Streamlit layer)
  inference.py                   # Pure-Python feature-building for live predictions
data_prep/
  generate_synthetic_data.py     # No longer used by the app; kept for reference
  clean_pipeline.py              # Cleaning logic, ported from the notebook
  train_models.py                # Encoding + training + comparison, ported from the notebook
data/                            # raw_vehicle_sales.csv (real data) + generated clean CSV
models/                          # Generated .joblib models + results.csv
assets/hero_car.jpg              # Home page hero image
assets/readme_home.png          # README dashboard preview
```

## Notes

- Model hyperparameters in `train_models.py` are fixed (not grid-searched) so
  training stays fast inside the app. The notebook's `RandomizedSearchCV`
  blocks for Decision Tree / Random Forest can be dropped back in if you want
  the tuned versions — just replace the relevant model definitions.
- `XGBoost` and `LightGBM` are included in `requirements.txt` and are part of the
  shipped five-model comparison. If you rebuild the models, make sure both
  packages are installed first.
- The "Predict Price" error range is the model's typical error (± test-set
  MAE, converted from the log-price scale back to dollars) — it's a simple,
  interpretable proxy for uncertainty, not a formal confidence interval.

## Navigation (fixed)

The top navigation bar is rendered by a single shared helper,
`utils.theme.render_topbar(active=...)`, and is called on **every** page.

Streamlit strips the numeric ordering prefix from files in `pages/`, so
`pages/1_KPI_Overview.py` is served at `/KPI_Overview`, not `/1_KPI_Overview`.
Linking to the numbered file name was what caused the "Page not found" errors.
All nav links now use the correct, relative slugs:

| Nav item     | Page file                     | URL                 |
|--------------|-------------------------------|---------------------|
| Home         | `Home.py`                     | `/`                 |
| EDA          | `pages/1_KPI_Overview.py`     | `/KPI_Overview`     |
| Car Analysis | `pages/2_Car_Analysis.py`     | `/Car_Analysis`     |
| Description  | `pages/3_Data_Description.py` | `/Data_Description` |
| Predict Price| `pages/5_Predict_Price.py`    | `/Predict_Price`    |
| Report       | `pages/6_Report.py`           | `/Report`           |
| ML Models    | `pages/4_ML_Models.py`        | `/ML_Models`        |



## 👨‍💻 Author

**Abdelaziz Elshourbgy**

- GitHub: [AbdelazizElshourbgy-ui](https://github.com/AbdelazizElshourbgy-ui)
- LinkedIn: [abdelaziz-elshourbgy](https://www.linkedin.com/in/abdelaziz-elshourbgy-b126a83a2/)
