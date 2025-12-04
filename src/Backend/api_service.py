import pandas as pd

ADM_TABLE = pd.read_csv("data/AreaCodes.csv")

def get_adm4_from_kelurahan(kelurahan_name: str):
    """
    Returns ADM4 code given kelurahan name.
    """
    row = ADM_TABLE[ADM_TABLE["kelurahan"].str.lower() == kelurahan_name.lower()]

    if row.empty:
        raise ValueError(f"Kelurahan '{kelurahan_name}' not found in ADM table.")

    return row.iloc[0]["adm4"]
