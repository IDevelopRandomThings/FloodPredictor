# src/train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import joblib
from preprocess import preprocess

# Load dataset
df = pd.read_csv("data/flood_dummy_training_data_cleaned.csv")

# Preprocess
df, le_subdistrict = preprocess(df)

# Split
X = df.drop(columns=["flood"])
y = df["flood"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss"
)
print("Training model...")
model.fit(X_train, y_train)
print("Training complete!")

# Evaluate
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model & encoder
joblib.dump(model, "models/flood_xgb_model.pkl")
joblib.dump(le_subdistrict, "models/subdistrict_encoder.pkl")
print("Model and encoder saved successfully.")
