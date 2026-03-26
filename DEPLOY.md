# OTT Monetization Analysis — Deployment Guide
**Student:** Ayushman Banerjee | **Roll:** 2305613

---

## Architecture
```
React Frontend  ──►  Vercel (free)
FastAPI Backend ──►  Render (free)
ML Models       ──►  Trained at build time, saved as .pkl
```

---

## STEP 1 — Push to GitHub

```bash
# From ott-project/ root
git init
git add .
git commit -m "OTT Monetization Analysis - initial commit"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/ott-monetization.git
git branch -M main
git push -u origin main
```

---

## STEP 2 — Deploy Backend on Render (FREE)

1. Go to **https://render.com** → Sign up with GitHub (free)
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python train_models.py`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Click **Create Web Service**
6. Wait ~3 mins for build. Copy the URL like: `https://ott-monetization-api.onrender.com`

> ⚠️ Free Render instances sleep after 15min inactivity (first request takes ~30s to wake up).

---

## STEP 3 — Deploy Frontend on Vercel (FREE)

1. Go to **https://vercel.com** → Sign up with GitHub (free)
2. Click **Add New Project → Import** your repo
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add **Environment Variable:**
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-name.onrender.com`  ← paste Render URL here
5. Click **Deploy**
6. Your app is live at `https://ott-monetization-XXXX.vercel.app`

---

## STEP 4 — Test Locally First (Optional)

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python train_models.py        # train models once
uvicorn main:app --reload     # starts at http://localhost:8000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev                   # starts at http://localhost:5173
```

---

## Project Structure
```
ott-project/
├── backend/
│   ├── main.py           # FastAPI app with 4 endpoints
│   ├── train_models.py   # Trains & saves all 4 RF models
│   ├── requirements.txt
│   ├── render.yaml       # Render deployment config
│   └── models/           # Generated after running train_models.py
│       ├── churn_model.pkl
│       ├── revenue_model.pkl
│       ├── segment_model.pkl
│       └── content_model.pkl
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── api.js
    │   ├── index.css
    │   └── components/
    │       ├── Overview.jsx
    │       ├── ChurnPredictor.jsx
    │       ├── RevenuePredictor.jsx
    │       ├── SegmentPredictor.jsx
    │       └── ContentPredictor.jsx
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── vercel.json
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | GET | Health check |
| `POST /predict/churn` | POST | Churn probability |
| `POST /predict/revenue` | POST | Monthly revenue prediction |
| `POST /predict/segment` | POST | User segment (4 classes) |
| `POST /predict/content` | POST | Content revenue potential |

---

## Estimated Accuracy (Synthetic Data)
| Model | Type | Expected Accuracy |
|---|---|---|
| Churn | Classification | ~87% |
| Revenue | Regression (MAE) | ~₹42 |
| Segment | Multi-class | ~91% |
| Content | Classification | ~83% |

*Replace synthetic data with real Kaggle OTT dataset for higher accuracy.*
