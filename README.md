# 🚗 Smart Car Price Prediction

![Car Price Prediction Dashboard](assets/readme_home.png)

<p align="center">
  <b>Machine Learning Dashboard for Car Price Prediction</b>
</p>

<p align="center">
  An interactive Streamlit application for exploring car data, analyzing market trends, training machine learning models, and predicting car prices.
</p>

<p align="center">
  <a href="https://smart-car-pricing.streamlit.app/">
    <strong>🚀 Live Demo</strong>
  </a>
</p>

---

## 📌 Overview

**Smart Car Price Prediction** is an interactive machine learning dashboard built with **Python** and **Streamlit**.

The project combines data analysis, visualization, machine learning, and price prediction into a single dashboard. Users can explore the dataset, analyze car characteristics, compare machine learning models, and estimate car prices through an easy-to-use interface.

---

## ✨ Features

- 📊 Interactive KPI dashboard
- 🚘 Detailed car market analysis
- 📋 Dataset description and exploration
- 🤖 Machine learning model comparison
- 💰 Interactive car price prediction
- 📑 Automated project report
- 📈 Visual charts and performance metrics
- 🎨 Clean and interactive Streamlit interface

---

## 🖥️ Dashboard Pages

| Page | Description |
|------|-------------|
| 📊 **KPI Overview** | Main dashboard with key statistics and market insights |
| 🚘 **Car Analysis** | Explore car prices and different vehicle characteristics |
| 📋 **Data Description** | Dataset structure, features, and descriptive statistics |
| 🤖 **ML Models** | Compare machine learning models and their performance |
| 💰 **Predict Price** | Enter car specifications and estimate the expected price |
| 📑 **Report** | Generate a complete project report |

---

## 🤖 Machine Learning Models

The project evaluates several regression models for car price prediction:

- **XGBoost**
- **LightGBM**
- **Random Forest**
- **Decision Tree**
- **Linear Regression**

### Model Performance

| Model | Train R² | Train MAE | Train RMSE | Test R² | Test MAE | Test RMSE |
|------|---------:|----------:|-----------:|--------:|---------:|----------:|
| **XGBoost** | 0.934811 | 0.148137 | 0.232283 | 0.928308 | 0.152985 | 0.242901 |
| **LightGBM** | 0.928567 | 0.153774 | 0.243153 | 0.925363 | 0.156129 | 0.247838 |
| **Random Forest** | 0.899148 | 0.192364 | 0.288916 | 0.884367 | 0.202831 | 0.308485 |
| **Decision Tree** | 0.912052 | 0.166113 | 0.269800 | 0.879025 | 0.192294 | 0.315529 |
| **Linear Regression** | 0.802038 | 0.288921 | 0.404781 | 0.799452 | 0.289783 | 0.406258 |

---

## 🛠️ Tech Stack

### Programming
- Python

### Data Science & Machine Learning
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- LightGBM

### Visualization
- Plotly

### Application
- Streamlit

### Reporting
- FPDF

---

## 📂 Project Structure

```text
car-price-prediction/
│
├── assets/
│   └── hero_car.jpg
│
├── data/
│   └── .gitkeep
│
├── data_prep/
│   ├── __init__.py
│   ├── clean_pipeline.py
│   ├── generate_synthetic_data.py
│   └── train_models.py
│
├── docs/
│   └── screenshots/
│       └── home_preview.png
│
├── models/
│   └── .gitkeep
│
├── pages/
│   ├── 1_KPI_Overview.py
│   ├── 2_Car_Analysis.py
│   ├── 3_Data_Description.py
│   ├── 4_ML_Models.py
│   ├── 5_Predict_Price.py
│   └── 6_Report.py
│
├── utils/
│   ├── __init__.py
│   ├── charts.py
│   ├── data_loader.py
│   ├── inference.py
│   ├── ml_utils.py
│   └── theme.py
│
├── Home.py
├── README.md
└── requirements.txt
