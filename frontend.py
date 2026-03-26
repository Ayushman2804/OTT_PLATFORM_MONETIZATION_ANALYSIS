import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import requests

# --- Config & Page Setup ---
st.set_page_config(page_title="OTT AI Neural Engine", page_icon="🧠", layout="wide")

# --- Modern AI CSS Injection ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Grotesk:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .st-emotion-cache-10trrnm {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.5px;
    }
    
    /* Neon glow effect for AI vibe */
    .stButton>button {
        background: rgba(0, 229, 255, 0.1) !important;
        border: 1px solid #00E5FF !important;
        color: #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: #00E5FF !important;
        color: #0A0E17 !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Glassmorphism panels */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(17, 24, 39, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* AI Terminal typing animation base */
    .ai-typing {
        border-right: 2px solid #00E5FF;
        white-space: nowrap;
        overflow: hidden;
        animation: typing 2s steps(40, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #00E5FF; } }
    
    /* Hide Deploy */
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🧠 Neural Core Active")
    st.markdown("---")
    st.markdown("**Operator:** AYUSHMAN BANERJEE")
    st.markdown("**Clearance:** 2305613")
    st.markdown("**Sector:** OTT Monetization AI")
    st.markdown("---")
    st.success("🟢 System Online")
    scan_btn = st.button("Initialize Deep Scan")
    if scan_btn:
        with st.spinner("Calibrating Neural Pathways..."):
            time.sleep(1)
        st.success("Scan Complete. Algorithms Optimized.")

# --- Header ---
st.markdown("<h1 style='color:#00E5FF; text-shadow: 0 0 10px rgba(0,229,255,0.5);'>OTT Monetization Neural Engine v2.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='ai-typing' style='color:#8b9eb3; font-family: monospace; font-size: 1.1em;'>Initializing big data matrix... Loading OTT user behavior vectors...</p>", unsafe_allow_html=True)

# --- Mock Data Generation ---
@st.cache_data
def generate_revenue_data():
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=60, freq="ME")
    base_ad = np.linspace(20000, 95000, 60)
    base_sub = np.linspace(50000, 320000, 60)
    return pd.DataFrame({
        "Month": dates.strftime('%b %Y'),
        "Ad_Revenue": base_ad + np.random.randint(-8000, 12000, 60),
        "Subscription_Revenue": base_sub + np.random.randint(-15000, 25000, 60),
        "Churn_Probability": np.random.uniform(0.01, 0.08, 60)
    })

revenue_data = generate_revenue_data()
revenue_data['Total_Revenue'] = revenue_data['Ad_Revenue'] + revenue_data['Subscription_Revenue']

tab1, tab2, tab3 = st.tabs(["⚡ AI Workspace", "💬 Predictor Chat", "📡 Deep Metrics"])

with tab1:
    st.markdown("### 🌐 Live Ecosystem Matrix")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Nodes", "1.4M", "5.2% ↑", delta_color="normal")
    c2.metric("Premium Entitlements", "850K", "12.1% ↑", delta_color="normal")
    c3.metric("Neural Ad Impressions", "14.2M/d", "-1.2% ↓", delta_color="inverse")
    c4.metric("YTD Yield", f"${revenue_data['Total_Revenue'].sum():,.0f}", "8.4% ↑", delta_color="normal")
    
    st.markdown("---")
    
    # Advanced 3D Chart 
    fig = px.scatter_3d(
        revenue_data, x="Ad_Revenue", y="Subscription_Revenue", z="Total_Revenue",
        color="Churn_Probability", hover_name="Month",
        title="Multidimensional Revenue vs Churn Probability Matrix",
        color_continuous_scale="electric", # Modern AI colormap
        size_max=18
    )
    fig.update_layout(
        scene=dict(
            xaxis_title='Ad Signal',
            yaxis_title='Sub Signal',
            zaxis_title='Total Yield Matrix'
        ), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 💬 Neural Interaction Terminal")
    st.markdown("Configure target demographic vectors. The AI will compute the expected lifetime value.")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("#### ⚙️ Input Vectors")
        watch_mins = st.slider("Daily Matrix Connect Time (m)", 10, 300, 120, 10)
        ad_clicks = st.slider("Ad Interaction Frequency (/wk)", 0, 50, 15, 1)
        sub_tier = st.selectbox("Tier Designation", [
            "Tier 0: Ad-Supported Mobile",
            "Tier 1: Basic Node", 
            "Tier 2: Standard Interface",
            "Tier 3: Premium Uplink",
            "Tier 4: Family Master Node"
        ], index=2)
        
        predict_trigger = st.button("Initialize Deep Prediction")

    with col2:
        st.markdown("#### 🤖 AI Output Console")
        
        # Simulated Chatbot interface
        chat_container = st.container(height=350)
        
        with chat_container:
            with st.chat_message("ai", avatar="🧠"):
                st.write("Awaiting vector input parameters to calculate user monetization yield...")
            
            if predict_trigger:
                with st.chat_message("user", avatar="👨‍💻"):
                    st.write(f"Compute LTV for: {watch_mins} mins watched, {ad_clicks} ad clicks, {sub_tier}.")
                
                with st.chat_message("ai", avatar="🧠"):
                    status = st.empty()
                    status.write("Running Gradient Boosting Inference...")
                    time.sleep(1) # Fake inference time
                    status.write("Cross-referencing Kaggle Demographic Nodes...")
                    time.sleep(1)
                    
                    tier_idx = int(sub_tier[5])
                    
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/api/v1/predict_revenue",
                            json={
                                "user_id": "sim_user",
                                "age": 30,
                                "daily_watch_mins": watch_mins,
                                "ad_clicks_per_week": ad_clicks,
                                "sub_tier": tier_idx
                            }
                        )
                        if response.status_code == 200:
                            res = response.json()
                            estimated = res["predicted_revenue_usd"]
                            conf = res["confidence_score"] * 100
                            
                            status.markdown(f"""
                            **✅ API INFERENCE COMPLETE**
                            
                            * **Projected Monthly MRR:** <span style='color:#00E5FF; font-weight:bold;'>${estimated:.2f}</span>
                            * **Projected Yearly LTV:** <span style='color:#00FFAA; font-weight:bold;'>${(estimated * 12):,.2f}</span>
                            * **Confidence Interval:** `{conf:.1f}%`
                            
                            _Data processed via OTT Monetization Backend Engine._
                            """, unsafe_allow_html=True)
                        else:
                            status.error(f"API Error {response.status_code}: Please check backend.")
                    except Exception as e:
                        status.error(f"Backend Connection Failed. Please ensure you have started backend.py (FastAPI) on port 8000. Error: {e}")

with tab3:
    st.markdown("### 📡 Deep Metrics & Architecture")
    st.write("Neural Net Decision Weights")
    
    # Radar chart for AI feel
    df = pd.DataFrame(dict(
        r=[45, 25, 15, 10, 5],
        theta=['Sub Tier Weight', 'Engage Time', 'Ad Gravity', 'Demographic Bias', 'Loyalty Factor']
    ))
    fig2 = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig2.update_traces(fill='toself', fillcolor='rgba(0, 229, 255, 0.2)', line_color='#00E5FF')
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 50], gridcolor='#111827'),
            angularaxis=dict(gridcolor='#111827')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0')
    )
    st.plotly_chart(fig2, use_container_width=True)
