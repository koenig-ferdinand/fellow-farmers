from flask import Flask, render_template, request, send_from_directory
from geopy.geocoders import Nominatim
import forecast
import imp_rec
from datetime import datetime, timedelta

app = Flask(__name__)

geolocator = Nominatim(user_agent="optimal_planting_app", timeout=7)

# Helper: Add days to a given date string in YYYY-MM-DD format
def add_days_to_date(date_str, days):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    new_date_obj = date_obj + timedelta(days=days)
    return new_date_obj.strftime("%Y-%m-%d")

# Helper: Sum up fertilizer amounts from the timeline
def get_total_fertilizer(fertilizer_timeline):
    total = 0.0
    for event in fertilizer_timeline:
        instructions = event.get("instructions", "")
        words = instructions.split()
        for word in words:
            clean_word = word.replace("(", "").replace(")", "").replace(":", "").replace(",", "")
            try:
                val = float(clean_word)
                total += val
                break  # Only add the first numeric value found
            except ValueError:
                continue
    return round(total, 2) if total > 0 else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # 1. Get form values
    town = request.form.get('town')
    crop = request.form.get('crop')  # e.g., 'Wheat', 'Rice', or 'Cotton'
    field_size_str = request.form.get('field_size')

    # 2. Validate field size
    try:
        field_size = float(field_size_str)
    except ValueError:
        error_msg = "Invalid field size. Please enter a numeric value."
        return render_template('result.html', error=error_msg)

    # 3. Convert town to lat/lon using geopy
    location = geolocator.geocode(town)
    if not location:
        error_msg = f"Could not find coordinates for '{town}'."
        return render_template('result.html', error=error_msg)
    latitude = str(location.latitude)
    longitude = str(location.longitude)

    # 4. Retrieve simulated historical weather data
    candidate_start_date = "2025-03-01"
    candidate_end_date = "2025-03-30"
    weather_data = forecast.get_historical_weather(
        latitude, longitude, candidate_start_date, candidate_end_date, years=5
    )
    if not weather_data:
        error_msg = "Failed to retrieve historical weather data."
        return render_template('result.html', error=error_msg)

    # 5. Generate schedule recommendation (using imp_rec.py)
    schedule = imp_rec.recommend_planting_schedule(crop, weather_data, field_size)
    if "error" in schedule:
        return render_template('result.html', error=schedule["error"])

    # 6. Convert day offsets to actual dates
    planting_start = schedule["optimal_planting_interval"]["start_date"]
    for event in schedule["fertilizer_timeline"]:
        day_offset = event.get("day", 0)
        event["action_date"] = add_days_to_date(planting_start, day_offset)

    # 7. Calculate total fertilizer needed
    total_fertilizer = get_total_fertilizer(schedule["fertilizer_timeline"])
    schedule["total_fertilizer_needed"] = f"{total_fertilizer} liters" if total_fertilizer else "Refer to product guidelines"

    # 8. Render result.html with schedule and user inputs
    return render_template(
        'result.html',
        town=town,
        latitude=latitude,
        longitude=longitude,
        crop=crop,
        field_size=field_size,
        schedule=schedule
    )

# New route for fellow farmers page
@app.route('/fellow')
def fellow():
    return render_template('fellow.html')

# New route for experts page
@app.route('/expert')
def expert():
    return render_template('expert.html')

# NEW: Route to serve images from the templates/pictures folder
@app.route('/pictures/<path:filename>')
def pictures(filename):
    return send_from_directory('templates/pictures', filename)

if __name__ == '__main__':
    app.run(debug=True)