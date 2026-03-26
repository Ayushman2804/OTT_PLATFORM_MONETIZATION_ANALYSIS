import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def generate_ott_data(n=1000):
    np.random.seed(42)
    # 2305613 AYUSHMAN BANERJEE OTT Monetization Analysis
    df = pd.DataFrame({
        'Daily_Watch_Mins': np.random.randint(10, 300, n),
        'Age': np.random.randint(18, 65, n),
        'Ad_Clicks_Per_Week': np.random.randint(0, 50, n),
        'Sub_Tier': np.random.choice([0, 1, 2, 3, 4], n), # 0:Mobile, 1:Basic, 2:Std, 3:Prem, 4:Family
        'Months_Subscribed': np.random.randint(1, 48, n)
    })
    # Target: Predicted Monthly Revenue from this user (ads + subs)
    df['Revenue'] = 5 + (df['Sub_Tier'] * 6.25) + (df['Ad_Clicks_Per_Week'] * 0.5) + (df['Daily_Watch_Mins'] * 0.05) + np.random.normal(0, 3, n)
    return df

if __name__ == "__main__":
    print("-" * 50)
    print("Project: OTT Monetization Analysis")
    print("Author: AYUSHMAN BANERJEE | Roll No: 2305613")
    print("-" * 50)
    
    # 1. Generate Fake Data
    df = generate_ott_data()
    X = df.drop('Revenue', axis=1)
    y = df['Revenue']
    
    # 2. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Define 3 Models to Compare
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_r2 = -float('inf')
    
    print("Evaluating Models...\n")
    for name, model in models.items():
        # Train Model
        model.fit(X_train, y_train)
        
        # Predict
        preds = model.predict(X_test)
        
        # Compare
        r2 = r2_score(y_test, preds)
        mse = mean_squared_error(y_test, preds)
        
        print(f"Model: {name}")
        print(f"  Accuracy (R2 Score): {r2:.4f}")
        print(f"  Error (MSE):         {mse:.4f}\n")
        
        # Keep track of the best
        if r2 > best_r2:
            best_r2 = r2
            best_model = name
            
    print("=" * 50)
    print(f"🏆 Best Performing Model: ** {best_model} **")
    print(f"   Reason: Captured the highest variance (Accuracy: {best_r2:.4f})")
    print("=" * 50)
