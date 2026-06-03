"""
generate_model.py
-----------------
Regenerates myapp/house_price_model.pkl using the California housing dataset
from scikit-learn.  Run this script whenever the model file needs to be
rebuilt (e.g. after a joblib / numpy version change):

    python generate_model.py

The saved model expects the eight features used by myapp/views.py:
    medinc, houseage, averooms, avebedrms, population, aveoccup,
    latitude, longitude
"""

import os
import joblib
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# ---------------------------------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------------------------------
print("Loading California housing dataset...")
data = fetch_california_housing(as_frame=True)

# The dataset columns are already in the order expected by views.py:
# MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
X = data.data
y = data.target  # median house value in units of $100,000

print(f"Dataset shape: {X.shape}")
print(f"Features: {list(X.columns)}")

# ---------------------------------------------------------------------------
# 2. Train / test split
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------------------------------------------------------
# 3. Train model
# ---------------------------------------------------------------------------
print("Training RandomForestRegressor...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# ---------------------------------------------------------------------------
# 4. Quick evaluation
# ---------------------------------------------------------------------------
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Test MAE: {mae:.4f} (in $100k units)  →  ~${mae * 100_000:,.0f}")

# ---------------------------------------------------------------------------
# 5. Save model
# ---------------------------------------------------------------------------
output_path = os.path.join(os.path.dirname(__file__), "myapp", "house_price_model.pkl")
joblib.dump(model, output_path)
print(f"Model saved to: {output_path}")
