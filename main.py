import json
from datetime import datetime, timedelta
import forecast
import imp_rec
from geopy.geocoders import Nominatim

def add_days_to_date(date_str, days):
    """
    Given a date string in YYYY-MM-DD format and a number of days,
    returns a new date string in YYYY-MM-DD format after adding the days.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    new_date_obj = date_obj + timedelta(days=days)
    return new_date_obj.strftime("%Y-%m-%d")

def get_total_fertilizer(fertilizer_timeline):
    """
    Loops through the fertilizer timeline events and attempts to extract a numeric fertilizer dose
    from the instructions. Sums up these doses. If none are found, returns a default message.
    """
    total = 0.0
    for event in fertilizer_timeline:
        instructions = event.get("instructions", "")
        # Look for a numeric value in the instructions. For example:
        # "Amount: 5.91 liters" → extract 5.91.
        words = instructions.split()
        for word in words:
            clean_word = word.replace("(", "").replace(")", "").replace(":", "").replace(",", "")
            try:
                val = float(clean_word)
                total += val
                break  # assume only one numeric value per event is needed
            except ValueError:
                continue
    return round(total, 2) if total > 0 else None

def main():
    print("Welcome to the Optimal Planting and Fertilizer Recommendation System!")
    
    # Ask for a town name instead of coordinates.
    town = input("Enter the name of the nearest town: ").strip()
    geolocator = Nominatim(user_agent="optimal_planting_app")
    location = geolocator.geocode(town)
    if not location:
        print(f"Could not find coordinates for {town}.")
        return
    latitude = str(location.latitude)
    longitude = str(location.longitude)
    print(f"Coordinates for {town}: {latitude}, {longitude}")
    
    crop = input("Enter the preferred crop (Wheat, Rice, Cotton): ").strip().title()
    try:
        field_size = float(input("Enter the size of your field in acres: ").strip())
    except ValueError:
        print("Invalid field size. Please enter a numeric value.")
        return
    
    print("\nFetching historical weather data for candidate planting period (next 30 days)...")
    # For demonstration, we use a fixed candidate period.
    candidate_start_date = "2025-03-01"
    candidate_end_date = "2025-03-30"
    
    # Retrieve simulated historical weather data.
    weather_data = forecast.get_historical_weather(latitude, longitude, candidate_start_date, candidate_end_date, years=5)
    if not weather_data:
        print("Failed to retrieve historical weather data.")
        return

    # Now call the planting schedule recommendation function from imp_rec.py.
    schedule = imp_rec.recommend_planting_schedule(crop, weather_data, field_size)
    
    # Convert fertilizer timeline 'day' offsets into actual action dates based on the planting start date.
    planting_start = schedule["optimal_planting_interval"]["start_date"]
    for event in schedule["fertilizer_timeline"]:
        day_offset = event.get("day", 0)
        event["action_date"] = add_days_to_date(planting_start, day_offset)
    
    # Calculate total fertilizer needed.
    total_fertilizer = get_total_fertilizer(schedule["fertilizer_timeline"])
    total_fertilizer_str = f"{total_fertilizer} liters" if total_fertilizer is not None else "Refer to product guidelines"
    schedule["total_fertilizer_needed"] = total_fertilizer_str

    print("\n########## OPTIMAL PLANTING SCHEDULE ##########")
    print(json.dumps(schedule, indent=4))

if __name__ == "__main__":
    main()