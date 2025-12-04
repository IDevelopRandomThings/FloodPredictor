# src/preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def fit_preprocess(df):
    df = df.copy()

    # ---------------------------
    # Convert adm4 to categorical code
    # ---------------------------
    df["adm4"] = df["adm4"].astype("category").cat.codes

    # ---------------------------
    # Subdistrict (kelurahan) encoder
    # ---------------------------
    le_subdistrict = LabelEncoder()
    df["subdistrict_id"] = le_subdistrict.fit_transform(df["subdistrict_name"])

    # ---------------------------
    # Datetime features
    # ---------------------------
    df["local_datetime"] = pd.to_datetime(df["local_datetime"])
    df["hour"] = df["local_datetime"].dt.hour
    df["day"] = df["local_datetime"].dt.day
    df["month"] = df["local_datetime"].dt.month

    # ---------------------------
    # WIND DIRECTION FIX
    # ---------------------------

    if df["wd"].dtype == object:
        # convert string directions to category codes
        df["wd"] = df["wd"].astype("category").cat.codes
    
    # ---------------------------
    # Force numeric conversion for all numeric-like fields
    # ---------------------------
    numeric_cols = [
        "t", "hu", "ws", "tcc", "visibility",
        "rain_level", "sea_level", "tide_height"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


    # ---------------------------
    # Drop text columns
    # ---------------------------
    df = df.drop(columns=[
        "local_datetime",
        "subdistrict_name",
        "weather_desc_en"
    ], errors='ignore')

    return df, le_subdistrict



def transform_preprocess(df, le_subdistrict):
    df = df.copy()

    # ---------------------------
    # Convert adm4 to same categorical codes
    # ---------------------------
    df["adm4"] = df["adm4"].astype("category").cat.codes

    # ---------------------------
    # Encode kelurahan using saved encoder
    # ---------------------------
    df["subdistrict_id"] = le_subdistrict.transform(df["subdistrict_name"])

    # ---------------------------
    # Datetime features
    # ---------------------------
    df["local_datetime"] = pd.to_datetime(df["local_datetime"])
    df["hour"] = df["local_datetime"].dt.hour
    df["day"] = df["local_datetime"].dt.day
    df["month"] = df["local_datetime"].dt.month

    # ---------------------------
    # WIND DIRECTION FIX
    # ---------------------------

    if df["wd"].dtype == object:
        # convert string directions to category codes
        df["wd"] = df["wd"].astype("category").cat.codes


    numeric_cols = [
        "t", "hu", "ws", "tcc", "visibility",
        "rain_level", "sea_level", "tide_height"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


    df = df.drop(columns=[
        "local_datetime",
        "subdistrict_name",
        "weather_desc_en"
    ], errors='ignore')

    return df
