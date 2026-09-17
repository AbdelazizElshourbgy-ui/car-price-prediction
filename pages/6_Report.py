# 🚗 Smart Car Price Prediction

![Smart Car Price Prediction Dashboard](assets/readme_home.png)

<p align="center">
  <strong>Machine Learning Dashboard for Car Price Prediction</strong>
</p>

<p align="center">
  An interactive Streamlit application for car market analysis, machine learning model evaluation, and car price prediction.
</p>

---

## 📌 Overview

**Smart Car Price Prediction** is an interactive machine learning dashboard built with **Python** and **Streamlit**.

The application brings together **data analysis, visualization, machine learning, model comparison, and interactive price prediction** in a single user-friendly dashboard.

Users can explore the car dataset, analyze market trends, compare regression models, evaluate their performance, and predict the estimated price of a vehicle based on its specifications.

### 🚀 Live Demo

https://smart-car-pricing.streamlit.app/

---

## ✨ Features

- 📊 **Interactive KPI Dashboard**
- 🚘 **Car Market Analysis**
- 📋 **Dataset Exploration & Statistics**
- 🤖 **Machine Learning Model Comparison**
- 💰 **Interactive Car Price Prediction**
- 📈 **Model Performance Evaluation**
- 📑 **Automated Project Report**
- 🎨 **Interactive Streamlit Interface**
- 📉 **Data Visualization with Plotly**

---

## 🖥️ Dashboard Pages

| Page | Description |
|------|-------------|
| 📊 **KPI Overview** | View key statistics and important car market insights |
| 🚘 **Car Analysis** | Analyze car prices, brands, categories, and vehicle characteristics |
| 📋 **Data Description** | Explore the dataset structure, features, and statistical information |
| 🤖 **ML Models** | Compare machine learning models and their performance |
| 💰 **Predict Price** | Estimate a car's price using its specifications |
| 📑 **Report** | Generate and download an automated project report |

---

## 🤖 Machine Learning

The project uses several regression algorithms to predict car prices:

- **XGBoost**
- **LightGBM**
- **Random Forest**
- **Decision Tree**
- **Linear Regression**

### 📊 Model Performance

| Model | Train R² | Train MAE | Train RMSE | Test R² | Test MAE | Test RMSE |
|------|---------:|----------:|-----------:|--------:|---------:|----------:|
| **XGBoost** | 0.934811 | 0.148137 | 0.232283 | 0.928308 | 0.152985 | 0.242901 |
| **LightGBM** | 0.928567 | 0.153774 | 0.243153 | 0.925363 | 0.156129 | 0.247838 |
| **Random Forest** | 0.899148 | 0.192364 | 0.288916 | 0.884367 | 0.202831 | 0.308485 |
| **Decision Tree** | 0.912052 | 0.166113 | 0.269800 | 0.879025 | 0.192294 | 0.315529 |
| **Linear Regression** | 0.802038 | 0.288921 | 0.404781 | 0.799452 | 0.289783 | 0.406258 |

### 📌 Evaluation Metrics

- **R² Score:** Measures how well the model explains the variation in car prices.
- **MAE:** Measures the average absolute prediction error.
- **RMSE:** Measures the square root of the average squared prediction error.

---

## 🛠️ Tech Stack

### 💻 Programming
- Python

### 📊 Data Science & Machine Learning
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- LightGBM

### 📈 Visualization
- Plotly

### 🌐 Application
- Streamlit

### 📑 Reporting
- FPDF

---

## 📂 Project Structure

```text
car-price-prediction/
│
├── assets/
│   ├── hero_car.jpg
│   └── readme_home.png
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
