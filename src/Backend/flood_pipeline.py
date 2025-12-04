# src/backend/flood_pipeline.py

import pandas as pd
import joblib
from bmkg_fetcher import fetch_bmkg_forecast
from preprocess import transform_preprocess

# ===================================================
# LOAD TRAINED COMPONENTS
# ===================================================
model = joblib.load("models/flood_xgb_model.pkl")
le_kelurahan = joblib.load("models/kelurahan_encoder.pkl")

adm_map = pd.read_csv("data/AreaCodes.csv")    



# ===================================================
# WEATHER -> RAIN INTENSITY MAPPER
# ===================================================
def map_weather_to_rain_level(desc: str) -> int:
    d = desc.lower()
    if any(x in d for x in ["petir", "thunder", "badai"]):
        return 4
    if any(x in d for x in ["hujan lebat", "hujan deras"]):
        return 3
    if "hujan sedang" in d:
        return 2
    if any(x in d for x in ["hujan ringan", "gerimis"]):
        return 1
    return 0


# ===================================================
# MAIN PIPELINE
# ===================================================
def predict_flood_for_kelurahan(kelurahan_name: str):

    kel_name_norm = kelurahan_name.lower()

    # -----------------------------------------
    # FIND ADM4 CODE FROM MAPPING CSV
    # -----------------------------------------
    row = adm_map[
        adm_map["kelurahan"].str.lower() == kel_name_norm
    ]

    if row.empty:
        raise ValueError(f"Kelurahan '{kelurahan_name}' not found in ADM mapping CSV.")

    adm4_code = row.iloc[0]["adm4"]

    # -----------------------------------------
    # FETCH BMKG FORECAST
    # -----------------------------------------
    data = fetch_bmkg_forecast(adm4_code)

    cuaca_blocks = data["data"][0]["cuaca"]
    forecast_slots = []
    for block in cuaca_blocks:
        forecast_slots.extend(block)

    results = []

    # -----------------------------------------
    # PROCESS EACH FORECAST SLOT
    # -----------------------------------------
    for slot in forecast_slots:

        row = {
            "local_datetime": slot["local_datetime"],
            "subdistrict_name": kelurahan_name,  
            "adm4": adm4_code,
            "t": slot.get("t"),
            "hu": slot.get("hu"),
            "ws": slot.get("ws"),
            "wd": slot.get("wd_deg"),
            "tcc": slot.get("tcc"),
            "visibility": slot.get("vs_text"),

            "rain_level": map_weather_to_rain_level(slot["weather_desc"]),

            # rightnow we use a placeholder value of 0 for sea_level and tide_height beucase we couldnt find a good data source
            "sea_level": 0,
            "tide_height": 0,
        }

        df = pd.DataFrame([row])

        # -----------------------------------------
        # APPLY TRANSFORM
        # -----------------------------------------
        X = transform_preprocess(df, le_kelurahan)

        # -----------------------------------------
        # PREDICT
        # -----------------------------------------
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

        results.append({
            "datetime": row["local_datetime"],
            "weather": slot["weather_desc"],
            "temperature": slot.get("t"),
            "humidity": slot.get("hu"),  
            "flood_prediction": int(pred),
            "probability": float(prob*100)
        })

    return results
