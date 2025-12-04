# src/predict.py
import pandas as pd
import joblib
from preprocess import transform_preprocess

# Load trained model and encoder
model = joblib.load("models/flood_xgb_model.pkl")
le_subdistrict = joblib.load("models/kelurahan_encoder.pkl")

def clean_input(df):
    """Clean the input to match training-time formatting"""
    df = df.copy()

    if "subdistrict_name" in df.columns:
        df["subdistrict_name"] = df["subdistrict_name"].str.lower()

    numeric_cols = [
        "t", "hu", "ws", "tcc", "visibility",
        "rain_level", "sea_level", "tide_height"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def predict_flood(input_df):
    """
    Takes a DataFrame with raw features and returns prediction + probability
    """
    # === CLEAN RAW INPUT FIRST ===
    input_df = clean_input(input_df)

    # === APPLY TRANSFORM PIPELINE ===
    X = transform_preprocess(input_df, le_subdistrict)

    # === MODEL PREDICT ===
    prediction = model.predict(X)
    prob = model.predict_proba(X)[:, 1]

    return prediction, prob


# --------------------------
# MANUAL TESTING EXAMPLE
# --------------------------
sample = pd.DataFrame([{
    "adm4": 3173060004,
    "local_datetime": "2024-01-02 15:00:00",
    "subdistrict_name": "Kembangan Utara",   
    "t": 30,
    "hu": 95,
    "ws": 20,
    "wd": "SE",            
    "tcc": 95,
    "visibility": "1000",  
    "rain_level": "2",     
    "sea_level": 1,
    "tide_height": 0,
}])

pred, prob = predict_flood(sample)
print(f"Flood prediction: {pred[0]}  |  confidence: {prob[0]*100:.1f}%")
