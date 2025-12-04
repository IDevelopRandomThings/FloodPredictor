import requests

def fetch_bmkg_forecast(adm4_code: str):
    """
    Fetch BMKG weather forecast for a given ADM4 code using the public BMKG API.
    """
    url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={adm4_code}"

    response = requests.get(url)

    # If BMKG does not support the ADM4, return None gracefully
    if response.status_code == 404:
        return None
    
    

    response.raise_for_status()
    return response.json()
