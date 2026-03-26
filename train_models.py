"""
train_models.py
Run once locally (or in CI) to produce the .pkl files.
Uses a realistic synthetic OTT dataset — swap in real Kaggle data anytime.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_absolute_error
import joblib, os

os.makedirs("models", exist_ok=True)
np.random.seed(42)
N = 5000

# ── Synthetic OTT dataset ────────────────────────────────────────────────────
df = pd.DataFrame({
    "age":                        np.random.randint(18, 65, N),
    "monthly_charges":            np.random.uniform(99, 999, N),
    "tenure_months":              np.random.randint(1, 72, N),
    "num_profiles":               np.random.randint(1, 5, N),
    "weekly_watch_hours":         np.random.uniform(1, 40, N),
    "support_tickets":            np.random.randint(0, 10, N),
    "subscription_type":          np.random.randint(0, 3, N),   # 0=basic,1=std,2=prem
    "payment_method":             np.random.randint(0, 3, N),
    "content_categories_watched": np.random.randint(1, 10, N),
    "device_count":               np.random.randint(1, 5, N),
})

# Derived labels (realistic correlations)
churn_score = (
    - 0.03 * df.tenure_months
    - 0.5  * df.subscription_type
    + 0.2  * df.support_tickets
    - 0.05 * df.weekly_watch_hours
    + np.random.normal(0, 1, N)
)
df["churn"] = (churn_score > np.percentile(churn_score, 70)).astype(int)

df["monthly_revenue"] = (
    df.monthly_charges
    + 50 * df.subscription_type
    + 10 * df.weekly_watch_hours
    - 30 * df.support_tickets
    + np.random.normal(0, 50, N)
).clip(50, 2000)

seg_score = df.weekly_watch_hours * 0.4 + df.tenure_months * 0.3 + df.monthly_charges * 0.001
df["segment"] = pd.cut(seg_score, bins=4, labels=[0, 1, 2, 3]).astype(int)

# Content popularity dataset (separate)
content_df = pd.DataFrame({
    "genre_action":      np.random.randint(0, 2, N),
    "genre_drama":       np.random.randint(0, 2, N),
    "genre_comedy":      np.random.randint(0, 2, N),
    "genre_documentary": np.random.randint(0, 2, N),
    "avg_rating":        np.random.uniform(1, 10, N),
    "release_year":      np.random.randint(2010, 2025, N),
    "duration_minutes":  np.random.randint(20, 180, N),
    "language_hindi":    np.random.randint(0, 2, N),
    "language_english":  np.random.randint(0, 2, N),
})
content_score = (
    content_df.avg_rating * 0.4
    + content_df.genre_action * 0.3
    + content_df.genre_drama * 0.2
    + (content_df.release_year - 2010) * 0.05
    + np.random.normal(0, 1, N)
)
content_df["high_revenue"] = (content_score > np.percentile(content_score, 50)).astype(int)


def train_and_save(X, y, feat_cols, name, task="clf"):
    Xt, Xv, yt, yv = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    Xt_s = scaler.fit_transform(Xt)
    Xv_s = scaler.transform(Xv)

    if task == "clf":
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

    model.fit(Xt_s, yt)

    if task == "clf":
        print(f"\n── {name} ──")
        print(classification_report(yv, model.predict(Xv_s)))
    else:
        mae = mean_absolute_error(yv, model.predict(Xv_s))
        print(f"\n── {name} ── MAE: {mae:.2f}")

    joblib.dump(model,  f"models/{name}_model.pkl")
    joblib.dump(scaler, f"models/{name}_scaler.pkl")
    print(f"Saved models/{name}_model.pkl")


# ── Train all 4 ──────────────────────────────────────────────────────────────
churn_feats   = ["age","monthly_charges","tenure_months","num_profiles",
                 "weekly_watch_hours","support_tickets","subscription_type","payment_method"]
revenue_feats = ["age","tenure_months","weekly_watch_hours","num_profiles",
                 "subscription_type","content_categories_watched","device_count"]
segment_feats = ["age","weekly_watch_hours","monthly_charges","tenure_months",
                 "num_profiles","device_count","content_categories_watched","support_tickets"]
content_feats = ["genre_action","genre_drama","genre_comedy","genre_documentary",
                 "avg_rating","release_year","duration_minutes","language_hindi","language_english"]

train_and_save(df[churn_feats].values,   df["churn"].values,         churn_feats,   "churn",   "clf")
train_and_save(df[revenue_feats].values, df["monthly_revenue"].values,revenue_feats,"revenue", "reg")
train_and_save(df[segment_feats].values, df["segment"].values,       segment_feats, "segment", "clf")
train_and_save(content_df[content_feats].values, content_df["high_revenue"].values,
               content_feats, "content", "clf")

print("\n✅ All 4 models trained and saved to models/")
