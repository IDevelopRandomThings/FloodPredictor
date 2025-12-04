# src/train.py

import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from preprocess import fit_preprocess

# ================================================
# LOAD DATA
# ================================================
df = pd.read_csv("data/flood_training_data_kelurahan.csv")

# ================================================
# SEPARATE FEATURES & LABEL
# ================================================
target_column = "flood"
y = df[target_column]
X_raw = df.drop(columns=[target_column])


# ================================================
# PREPROCESS + ENCODER FITTING
# ================================================
X, le_kelurahan = fit_preprocess(X_raw)

# Check final feature sample
print("Sample processed features:")
print(X.head())


# ================================================
# TRAIN/TEST SPLIT
# ================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================================================
# TRAIN XGBOOST MODEL
# ================================================
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# ================================================
# FEATURE IMPORTANCE
# ================================================
import numpy as np

feature_names = X.columns
importances = model.feature_importances_

sorted_idx = np.argsort(importances)[::-1]

print("\n===== FEATURE IMPORTANCE RANKING =====")
for idx in sorted_idx:
    print(f"{feature_names[idx]}: {importances[idx]:.4f}")


# ================================================
# EVALUATION
# ================================================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL PERFORMANCE =====")
print(f"Test Accuracy: {accuracy * 100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))


# ================================================
# SAVE MODEL + ENCODER
# ================================================
joblib.dump(model, "models/flood_xgb_model.pkl")
joblib.dump(le_kelurahan, "models/kelurahan_encoder.pkl")

print("\nModel and encoder saved successfully.")
