import requests
import json

def get_daily_forecast(start_date, end_date=None):
    """
    Calls the CE Hub API for the given date range.
    If end_date is None, it uses start_date for both start and end.
    Returns the JSON response if successful, or None on error.
    """
    if end_date is None:
        end_date = start_date

    # API key for forecast
    API_KEY = "d4f087c7-7efc-41b4-9292-0f22b6199215"

    # Base URL for the Forecast Daily endpoint
    base_url = "https://services.cehub.syngenta-ais.com/api/Forecast/ShortRangeForecastDaily"
    
    # Coordinates for Sankt Gallen, Switzerland
    sankt_gallen_coords = {
        "latitude": 47.4239,
        "longitude": 9.3767
    }
    
    # Measure labels for a comprehensive forecast:
    measure_labels = (
        "TempAir_DailyAvg (C);"
        "TempAir_DailyMax (C);"
        "TempAir_DailyMin (C);"
        "HumidityRel_DailyAvg (pct);"
        "Precip_DailySum (mm);"
        "WindSpeed_DailyAvg (m/s);"
        "WindDirection_DailyAvg (Deg);"
        "Cloudcover_DailyAvg (pct);"
        "SunshineDuration_DailySum (min);"
        "Soilmoisture_0to10cm_DailyAvg (vol%);"
        "Evapotranspiration_DailySum (mm)"
    )
    
    # Set up parameters with the provided date range
    params = {
        "format": "json",
        "supplier": "Meteoblue",
        "startDate": start_date,
        "endDate": end_date,
        "measureLabel": measure_labels,
        "latitude": sankt_gallen_coords["latitude"],
        "longitude": sankt_gallen_coords["longitude"],
        "ApiKey": API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print("Error fetching forecast data:", e)
        return None

def main():
    """
    Simple test runner if you run forecast.py directly.
    """
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the end date (YYYY-MM-DD) [press Enter to use start date]: ").strip()
    if not end_date:
        end_date = start_date
    data = get_daily_forecast(start_date, end_date)
    
    if data:
        print("\nDetailed Weather Forecast from", start_date, "to", end_date)
        print(json.dumps(data, indent=4))
    else:
        print("Failed to retrieve forecast data.")

if __name__ == "__main__":
    main()