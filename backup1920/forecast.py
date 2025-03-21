import requests
import json
import datetime
import random

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
    
    # Coordinates for Sankt Gallen, Switzerland (you might later adjust this per user input)
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
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching forecast data:", e)
        return None

def get_historical_weather(lat, lon, start_date, end_date, years=5):
    """
    Simulates retrieving historical weather data for the given location (lat, lon)
    by averaging the same period over the past 'years' years.
    
    In a real implementation, replace the simulation with a call to a historical weather API
    or a database query.
    """
    date_format = "%Y-%m-%d"
    start_dt = datetime.datetime.strptime(start_date, date_format)
    end_dt = datetime.datetime.strptime(end_date, date_format)
    num_days = (end_dt - start_dt).days + 1

    simulated_data = []
    for i in range(num_days):
        current_date = start_dt + datetime.timedelta(days=i)
        # For each day, simulate averages based on historical data (here with random noise)
        tmax = 25 + random.uniform(-3, 3)
        tmin = 15 + random.uniform(-3, 3)
        rainfall = 2 + random.uniform(-1, 1)
        humidity = 60 + random.uniform(-10, 10)
        wind_speed = 2 + random.uniform(-0.5, 0.5)
        cloudcover = 50 + random.uniform(-20, 20)
        evap = 5 + random.uniform(-1, 1)
        soil_moisture = 30 + random.uniform(-5, 5)
        sunshine = 300 + random.uniform(-50, 50)
        simulated_data.append({
            "date": current_date.strftime(date_format),
            "TMAX": tmax,
            "TMIN": tmin,
            "TempAir_DailyAvg (C)": (tmax + tmin) / 2,
            "Precip_DailySum (mm)": rainfall,
            "HumidityRel_DailyAvg (pct)": humidity,
            "WindSpeed_DailyAvg (m/s)": wind_speed,
            "Cloudcover_DailyAvg (pct)": cloudcover,
            "Evapotranspiration_DailySum (mm)": evap,
            "Soilmoisture_0to10cm_DailyAvg (vol%)": soil_moisture,
            "SunshineDuration_DailySum (min)": sunshine
        })
    return simulated_data

def main():
    """
    Simple test runner if you run forecast.py directly.
    """
    mode = input("Enter 'short' for short-term forecast or 'extended' for historical average forecast: ").strip().lower()
    if mode == "short":
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
    else:
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
        data = get_historical_weather("47.4239", "9.3767", start_date, end_date, years=5)
        print("\nSimulated Historical Averages for Extended Forecast from", start_date, "to", end_date)
        print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()