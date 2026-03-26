from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import os
from pathlib import Path

app = FastAPI(title="OTT Monetization Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load models once at startup ──────────────────────────────────────────────
BASE = Path(__file__).parent / "models"

churn_model       = joblib.load(BASE / "churn_model.pkl")
revenue_model     = joblib.load(BASE / "revenue_model.pkl")
segment_model     = joblib.load(BASE / "segment_model.pkl")
content_model     = joblib.load(BASE / "content_model.pkl")
churn_scaler      = joblib.load(BASE / "churn_scaler.pkl")
revenue_scaler    = joblib.load(BASE / "revenue_scaler.pkl")
segment_scaler    = joblib.load(BASE / "segment_scaler.pkl")
content_scaler    = joblib.load(BASE / "content_scaler.pkl")

SEGMENT_NAMES = {0: "Casual Viewer", 1: "Power User", 2: "At-Risk User", 3: "Premium Loyalist"}

# ── Request schemas ──────────────────────────────────────────────────────────

class ChurnRequest(BaseModel):
    age: float
    monthly_charges: float
    tenure_months: float
    num_profiles: float
    weekly_watch_hours: float
    support_tickets: float
    subscription_type: float   # 0=basic 1=standard 2=premium
    payment_method: float      # 0=card 1=wallet 2=bank

class RevenueRequest(BaseModel):
    age: float
    tenure_months: float
    weekly_watch_hours: float
    num_profiles: float
    subscription_type: float
    content_categories_watched: float
    device_count: float

class SegmentRequest(BaseModel):
    age: float
    weekly_watch_hours: float
    monthly_charges: float
    tenure_months: float
    num_profiles: float
    device_count: float
    content_categories_watched: float
    support_tickets: float

class ContentRequest(BaseModel):
    genre_action: float
    genre_drama: float
    genre_comedy: float
    genre_documentary: float
    avg_rating: float
    release_year: float
    duration_minutes: float
    language_hindi: float
    language_english: float

# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "OTT Monetization API is live 🚀"}

@app.post("/predict/churn")
def predict_churn(req: ChurnRequest):
    X = np.array([[req.age, req.monthly_charges, req.tenure_months,
                   req.num_profiles, req.weekly_watch_hours,
                   req.support_tickets, req.subscription_type, req.payment_method]])
    X_scaled = churn_scaler.transform(X)
    prob = churn_model.predict_proba(X_scaled)[0][1]
    label = "High Risk" if prob > 0.6 else "Medium Risk" if prob > 0.35 else "Low Risk"
    fi = dict(zip(
        ["Age","Monthly Charges","Tenure","Profiles","Watch Hours","Support Tickets","Sub Type","Payment"],
        churn_model.feature_importances_.tolist()
    ))
    return {"churn_probability": round(float(prob), 4), "risk_label": label, "feature_importance": fi}

@app.post("/predict/revenue")
def predict_revenue(req: RevenueRequest):
    X = np.array([[req.age, req.tenure_months, req.weekly_watch_hours,
                   req.num_profiles, req.subscription_type,
                   req.content_categories_watched, req.device_count]])
    X_scaled = revenue_scaler.transform(X)
    pred = revenue_model.predict(X_scaled)[0]
    fi = dict(zip(
        ["Age","Tenure","Watch Hours","Profiles","Sub Type","Categories","Devices"],
        revenue_model.feature_importances_.tolist()
    ))
    return {"predicted_monthly_revenue": round(float(pred), 2), "feature_importance": fi}

@app.post("/predict/segment")
def predict_segment(req: SegmentRequest):
    X = np.array([[req.age, req.weekly_watch_hours, req.monthly_charges,
                   req.tenure_months, req.num_profiles, req.device_count,
                   req.content_categories_watched, req.support_tickets]])
    X_scaled = segment_scaler.transform(X)
    seg = int(segment_model.predict(X_scaled)[0])
    probs = segment_model.predict_proba(X_scaled)[0].tolist()
    dist = {SEGMENT_NAMES[i]: round(p, 3) for i, p in enumerate(probs)}
    return {"segment_id": seg, "segment_name": SEGMENT_NAMES[seg], "segment_distribution": dist}

@app.post("/predict/content")
def predict_content(req: ContentRequest):
    X = np.array([[req.genre_action, req.genre_drama, req.genre_comedy,
                   req.genre_documentary, req.avg_rating, req.release_year,
                   req.duration_minutes, req.language_hindi, req.language_english]])
    X_scaled = content_scaler.transform(X)
    prob = content_model.predict_proba(X_scaled)[0][1]
    label = "High Revenue" if prob > 0.65 else "Medium Revenue" if prob > 0.35 else "Low Revenue"
    return {"revenue_potential": round(float(prob), 4), "label": label}

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": 4}
