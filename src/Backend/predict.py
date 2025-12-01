# src/predict.py
import joblib
import pandas as pd

# Load model and encoder
model = joblib.load("models/flood_xgb_model.pkl")
le_subdistrict = joblib.load("models/subdistrict_encoder.pkl")

def preprocess_input(df):
    # Datetime features
    df["local_datetime"] = pd.to_datetime(df["local_datetime"])
    df["hour"] = df["local_datetime"].dt.hour
    df["day"] = df["local_datetime"].dt.day
    df["month"] = df["local_datetime"].dt.month

    # Subdistrict encoding
    df["subdistrict_id"] = le_subdistrict.transform(df["subdistrict_name"])

    # Wind direction encoding
    wd_map = {"N":0, "NE":1, "E":2, "SE":3, "S":4, "SW":5, "W":6, "NW":7}
    df["wd_code"] = df["wd"].map(wd_map)

    # Drop unused columns
    df = df.drop(columns=["local_datetime", "subdistrict_name", "wd", "weather_desc_en"], errors='ignore')
    return df

# Example usage
sample = pd.DataFrame([{
    "local_datetime": "2024-01-02 15:00:00",
    "subdistrict_name": "Kembangan",
    "t": 30,
    "hu": 95,
    "ws": 20,
    "wd": "SE",
    "tcc": 95,
    "visibility": 1,
    "rain_level": 4,
    "sea_level": 1.8,
    "tide_height": 2.5

}])

X_sample = preprocess_input(sample)
prediction = model.predict(X_sample)
prob = model.predict_proba(X_sample)[0][1]  # probability of flood
print(f"Flood prediction: {prediction[0]}, confidence: {prob*100:.1f}%")

