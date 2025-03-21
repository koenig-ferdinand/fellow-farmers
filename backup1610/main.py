import json
from datetime import datetime, timedelta
import forecast
import imp_rec

def safe_float(val):
    """Try converting val to float. Return None if not possible."""
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def merge_forecast_measures(data):
    """
    Merge individual forecast measure entries (one per measure) into one dictionary.
    """
    if not isinstance(data, list):
        return {}
    merged = {}
    for i, entry in enumerate(data):
        label = entry.get("measureLabel")
        val = entry.get("dailyValue")
        if label:
            merged[label] = val
        # Also save the date from the first entry
        if i == 0:
            merged["date"] = entry.get("date")
    return merged

def group_forecast_data_by_date(raw_data):
    """
    Group raw forecast data by date.
    Converts the API date format (e.g. "2025/03/19 00:00:00") into "YYYY-MM-DD".
    """
    grouped = {}
    for entry in raw_data:
        date_raw = entry.get("date")
        if date_raw:
            try:
                dt = datetime.strptime(date_raw, "%Y/%m/%d %H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
            except ValueError:
                date_str = date_raw
        else:
            continue
        if date_str not in grouped:
            grouped[date_str] = []
        grouped[date_str].append(entry)
    return grouped

def main():
    print("Welcome to the Crop Recommendation System!")
    planting_date_str = input("Enter the planting date (YYYY-MM-DD): ").strip()
    crop_input = input("Enter the crop you planted (Wheat, Rice, Cotton): ").strip()
    # Convert crop input to title-case to match our crop profiles
    crop = crop_input.title()
    rec_date_str = input("Enter the date for recommendation (YYYY-MM-DD): ").strip()

    # Parse dates and ensure the recommendation date is within the short-range supported by the API
    try:
        planting_date = datetime.strptime(planting_date_str, "%Y-%m-%d")
        rec_date = datetime.strptime(rec_date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format.")
        return

    if rec_date < planting_date:
        print("Error: Recommendation date cannot be earlier than the planting date.")
        return

    # Limit the forecast range to a maximum of 7 days (API limitation)
    max_range = timedelta(days=7)
    if rec_date - planting_date > max_range:
        print("Error: Forecast API supports only up to 7 days range. Please choose a recommendation date within 7 days of the planting date.")
        return

    # Retrieve forecast data for the given date range
    raw_data = forecast.get_daily_forecast(planting_date_str, rec_date_str)
    if raw_data is None or len(raw_data) == 0:
        print("No forecast data returned from the API.")
        return

    # Group raw data by date and merge measurements
    grouped = group_forecast_data_by_date(raw_data)
    merged_records = []
    for date in sorted(grouped.keys()):
        merged = merge_forecast_measures(grouped[date])
        merged["date"] = date
        merged_records.append(merged)

    print("\n########## FULL FORECAST DATA (Merged by Date) ##########")
    print(json.dumps(merged_records, indent=4))

    # Find the record for the recommendation date (or use the last available record)
    rec_record = None
    for record in merged_records:
        if record.get("date") == rec_date_str:
            rec_record = record
            break
    if rec_record is None:
        rec_record = merged_records[-1]

    # Extract weather parameters from the recommendation day's record
    TMAX = safe_float(rec_record.get("TempAir_DailyMax (C)"))
    TMIN = safe_float(rec_record.get("TempAir_DailyMin (C)"))
    average_temp = safe_float(rec_record.get("TempAir_DailyAvg (C)"))
    rainfall = safe_float(rec_record.get("Precip_DailySum (mm)"))
    humidity = safe_float(rec_record.get("HumidityRel_DailyAvg (pct)"))
    wind_speed = safe_float(rec_record.get("WindSpeed_DailyAvg (m/s)"))
    wind_dir = safe_float(rec_record.get("WindDirection_DailyAvg (Deg)"))
    cloudcover = safe_float(rec_record.get("Cloudcover_DailyAvg (pct)"))
    sunshine = safe_float(rec_record.get("SunshineDuration_DailySum (min)"))
    soil_moisture = safe_float(rec_record.get("Soilmoisture_0to10cm_DailyAvg (vol%)"))
    evap = safe_float(rec_record.get("Evapotranspiration_DailySum (mm)"))

    # Build daily temperature data (for cumulative GDD calculation)
    daily_temp_data = []
    for record in merged_records:
        day = {
            "date": record.get("date"),
            "TMAX": safe_float(record.get("TempAir_DailyMax (C)")),
            "TMIN": safe_float(record.get("TempAir_DailyMin (C)"))
        }
        daily_temp_data.append(day)

    # Optional additional parameters (extend these as needed)
    pH = None
    nitrogen_applied = None
    projected_yield = None
    previous_yields = None

    # Call the recommendation function
    recommendation = imp_rec.recommend_biosimulant(
        crop=crop,
        TMAX=TMAX,
        TMIN=TMIN,
        average_temp=average_temp,
        rainfall=rainfall,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_dir=wind_dir,
        cloudcover=cloudcover,
        sunshine=sunshine,
        soil_moisture=soil_moisture,
        evap=evap,
        pH=pH,
        nitrogen_applied=nitrogen_applied,
        projected_yield=projected_yield,
        previous_yields=previous_yields,
        daily_temp_data=daily_temp_data,
        planting_date=planting_date_str
    )

    print("\n########## RECOMMENDATION ##########")
    print(json.dumps(recommendation, indent=4))

if __name__ == "__main__":
    main()