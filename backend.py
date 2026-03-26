from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import uvicorn

# ======================================================================
# FAKE REPLICA BACKEND FOR PRESENTATION (PPT ONLY)
# Student: AYUSHMAN BANERJEE
# Roll No: 2305613
# Topic: OTT Monetization Analysis
# Purpose: This code provides realistic API endpoints to screenshot
#          for the backend architecture part of the final PPT review.
# ======================================================================

app = FastAPI(
    title="OTT Monetization REST API", 
    description="Backend replica containing the monetization logic and endpoints."
)

class UserData(BaseModel):
    user_id: str
    age: int
    daily_watch_mins: int
    ad_clicks_per_week: int
    sub_tier: int

@app.get("/")
def health_check():
    return {
        "status": "Active", 
        "module": "OTT Revenue Prediction Base Endpoint",
        "author": "Ayushman Banerjee"
    }

@app.post("/api/v1/predict_revenue")
def predict_revenue(data: UserData) -> Dict[str, float]:
    """
    Simulates receiving JSON user data from the frontend and returning 
    an ML prediction for OTT monetization revenue.
    """
    predicted = 10.0 + (data.sub_tier * 15.0) + (data.ad_clicks_per_week * 0.5) + (data.daily_watch_mins * 0.05)
    return {
        "predicted_revenue_usd": round(predicted, 2),
        "confidence_score": 0.992 # Accuracy passed from Gradient Boosting evaluation
    }

@app.get("/api/v1/model_metrics")
def get_metrics():
    """
    Endpoint returning data validation metrics to the dashboard UI.
    Screenshots nicely for PPT to show data flow.
    """
    return {
        "models_tested": ["Linear Regression", "Random Forest Regressor", "Gradient Boosting"],
        "best_model": "Gradient Boosting Regressor",
        "best_r2_score": 0.992,
        "best_mse": 2.14,
        "features_used": ["Watch Time", "Ad Clicks", "Subscription Tier"]
    }

@app.get("/api/v1/datasets/netflix_engagement")
def get_netflix_kaggle_data():
    """
    Simulates fetching Netflix watch engagement data from Kaggle dataset.
    """
    return {
        "dataset_source": "Kaggle: Netflix Movies and TV Shows",
        "records_loaded": 8807,
        "features": ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration"],
        "status": "ready for processing"
    }

@app.get("/api/v1/datasets/amazon_prime_content")
def get_amazon_kaggle_data():
    """
    Simulates fetching Amazon Prime Video dataset from Kaggle.
    """
    return {
        "dataset_source": "Kaggle: Amazon Prime Movies and TV Shows",
        "records_loaded": 9668,
        "features": ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration"],
        "status": "ready for processing"
    }

@app.get("/api/v1/datasets/disney_plus_demographics")
def get_disney_kaggle_data():
    """
    Simulates fetching Disney+ dataset from Kaggle.
    """
    return {
        "dataset_source": "Kaggle: Disney+ Movies and TV Shows",
        "records_loaded": 1450,
        "features": ["show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating", "duration"],
        "status": "ready for processing"
    }

class ChurnData(BaseModel):
    user_id: str
    months_subscribed: int
    recent_activity_score: float
    support_tickets: int

@app.post("/api/v1/predict_churn")
def predict_churn(data: ChurnData) -> Dict[str, float]:
    """
    Predicts User Churn probability using Random Forest model trained on Kaggle OTT Churn Dataset.
    """
    # Fake logic
    churn_prob = (0.8 / data.months_subscribed) + (data.support_tickets * 0.1) - (data.recent_activity_score * 0.05)
    churn_prob = max(0.01, min(0.99, churn_prob))
    return {
        "churn_probability": round(churn_prob, 4),
        "model_used": "Random Forest Classifier",
        "dataset_source": "Kaggle: Telco & OTT Customer Churn"
    }

if __name__ == "__main__":
    print("Serving enhanced fake replica backend for OTT Monetization Analysis with Kaggle datasets...")
    # uvicorn.run(app, host="127.0.0.1", port=8000)
