# src/preprocess.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(df):
    # Datetime features
    df["local_datetime"] = pd.to_datetime(df["local_datetime"])
    df["hour"] = df["local_datetime"].dt.hour
    df["day"] = df["local_datetime"].dt.day
    df["month"] = df["local_datetime"].dt.month

    # Subdistrict encoding
    le_subdistrict = LabelEncoder()
    df["subdistrict_id"] = le_subdistrict.fit_transform(df["subdistrict_name"])

    # Wind direction encoding
    wd_map = {"N":0, "NE":1, "E":2, "SE":3, "S":4, "SW":5, "W":6, "NW":7}
    df["wd_code"] = df["wd"].map(wd_map)

    # Drop unused columns
    df = df.drop(columns=["local_datetime", "subdistrict_name", "wd", "weather_desc_en"])
    
    return df, le_subdistrict
