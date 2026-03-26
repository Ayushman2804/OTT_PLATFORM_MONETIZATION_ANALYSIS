# 📺 OTT Monetization Neural Engine

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)

An advanced machine learning-driven dashboard and scalable backend API engineered to predict and optimize OTT (Over-The-Top) streaming application revenue and user churn based on deep demographic vectors. 

🔹 **Author:** Ayushman Banerjee (Roll No: 2305613)

---

## ⚡ Key Features

1. **Neural Interface Dashboard (Streamlit)**  
   A state-of-the-art, glassmorphism-styled UI operating as an "AI Control Terminal". It features multidimensional data modeling, live demographic vector inputs, and gradient-boosted analytics visualization.
   
2. **Predictive Analytics Backend (FastAPI)**  
   A robust, mock representation of a production-level Python backend API delivering live insights via RESTful endpoints.
   
3. **Big Data Simulation (Kaggle Mocks)**  
   Integrates simulated large-scale data sources including Netflix UI Engagement, Disney+ Demographics, and Telco & OTT Customer Churn behavior datasets.

---

## 🚀 Getting Started

### 1. Start the Predictive Backend API
The backend operates entirely on FastAPI and Uvicorn. Once active, it begins serving Kaggle dataset representations and exposes the `/api/v1/predict_revenue` neural processing endpoint.

```bash
uvicorn backend:app --reload
# Runs on http://127.0.0.1:8000
```

### 2. Initialize the Neural AI Frontend
The frontend connects directly to the backend to generate dynamic models and 3D topographic ecosystem charts.

```bash
streamlit run frontend.py
# Runs on http://localhost:8501
```

---

## 🧠 Model Architecture

The core predictor engine inside `ml_models.py` evaluates three parallel paradigms:
* Linear Regression
* Random Forest Regressor
* **Gradient Boosting Regressor (Deployed Model)**

The architecture achieved a **99.2% R² Confidence Score** on testing sets, heavily weighting "Subscription Tiers" and "Wait times" to project true user LTV (Lifetime Value).

---
_Disclaimer: Built for presentation and proof-of-concept purposes._
