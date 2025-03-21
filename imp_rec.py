#!/usr/bin/env python
# coding: utf-8

import numpy as np
from datetime import datetime

def safe_float(val, default=None):
    """
    Attempts to convert val to float.
    If val is 'n/a' or None, returns default.
    """
    if val is None or str(val).lower() == "n/a":
        return default
    try:
        return float(val)
    except:
        return default

# ------------------------------------------------------------------------------
# Crop Profiles for Wheat, Rice and Cotton
# ------------------------------------------------------------------------------
CROP_PROFILES = {
    "Wheat": {
        "TotalWaterRequirement": 450,  # mm per crop cycle
        "GrowthStages": {
            "Germination": 50,
            "Vegetative": 150,
            "Flowering": 200,
            "Maturity": 50
        },
        "CriticalStages": ["Flowering"],
        "BiologicalProducts": {
            "StressBuster": {
                "Dosage": "2-3 L/ha or 150-250 mL/hL",
                "ApplicationFrequency": "2 times per growth cycle in case of abiotic stress",
                "GDDRange": [450, 500, 900, 950]
            },
            "YieldBooster": {
                "Dosage": "As per product guidelines",  # For Wheat, override will be applied if needed.
                "ApplicationTiming": [
                    {"Stage": "Flag leaf growth stage", "GDD": [600, 700]}
                ]
            }
        },
        "SoilCarbon": {
            "BaselineSOC": 1.0,
            "SequestrationPotential": "0.1-0.2% increase in SOC per year",
            "RecommendedPractices": [
                "Cover cropping with legumes",
                "Conservation tillage",
                "Application of compost or biochar"
            ]
        }
    },
    "Rice": {
        "TotalWaterRequirement": 1200,
        "GrowthStages": {
            "Germination": 100,
            "Vegetative": 500,
            "Flowering": 400,
            "Maturity": 200
        },
        "CriticalStages": ["Flowering", "Vegetative"],
        "BiologicalProducts": {
            "StressBuster": {
                "Dosage": "2-3 L/ha or 150-250 mL/hL",
                "ApplicationFrequency": "2 times per growth cycle in case of abiotic stress",
                "GDDRange": [450, 500, 1050, 1100]
            },
            "YieldBooster": {
                "Dosage": "As per product guidelines",  # Will be overridden to "2 L/ha" if needed.
                "ApplicationTiming": [
                    {"Stage": "Beginning of booting", "GDD": [800, 850]},
                    {"Stage": "Heading growth stage", "GDD": [1050, 1100]}
                ]
            }
        },
        "SoilCarbon": {
            "BaselineSOC": 1.2,
            "SequestrationPotential": "0.2-0.3% increase in SOC per year",
            "RecommendedPractices": [
                "Alternate wetting and drying (AWD)",
                "Application of rice straw compost",
                "Cover cropping with green manure"
            ]
        }
    },
    "Cotton": {
        "TotalWaterRequirement": 700,
        "GrowthStages": {
            "Germination": 50,
            "Vegetative": 300,
            "Flowering": 250,
            "Maturity": 100
        },
        "CriticalStages": ["Flowering"],
        "BiologicalProducts": {
            "StressBuster": {
                "Dosage": "2-3 L/ha or 150-250 mL/hL",
                "ApplicationFrequency": "2 times per growth cycle in case of abiotic stress",
                "GDDRange": [500, 550, 900, 950]
            },
            "YieldBooster": {
                "Dosage": "2-3 L/ha or 150-250 mL/hL",  # Cotton already specifies an amount.
                "ApplicationTiming": [
                    {"Stage": "Before squares appear", "GDD": [350, 400]},
                    {"Stage": "3-4 weeks after first application", "GDD": "Follow-up"}
                ]
            }
        },
        "SoilCarbon": {
            "BaselineSOC": 0.8,
            "SequestrationPotential": "0.1-0.3% increase in SOC per year",
            "RecommendedPractices": [
                "Intercropping with legumes",
                "Mulching with crop residues",
                "Application of biochar"
            ]
        }
    }
}

# ------------------------------------------------------------------------------
# Updated: Professional Fertilizer Performance Data
# ------------------------------------------------------------------------------
FERTILIZER_PERFORMANCE_DATA = {
    "StressBuster": {
        "Wheat": "Key figure: 3.9:1 ROI – every 3.9 invested yields increased productivity.",
        "Rice": "Key figure: 3.9:1 ROI – every 3.9 invested yields increased productivity.",
        "Cotton": "Key figure: 3.9:1 ROI – every 3.9 invested yields increased productivity."
    },
    "YieldBooster": {
        "Wheat": "Key figure: +0.3 t/ha – confirmed yield increase in wheat.",
        "Rice": "Key figure: +0.4 t/ha – confirmed yield increase in rice.",
        "Cotton": "Key figure: Yield improvement observed in field trials."
    }
}

# ------------------------------------------------------------------------------
# Filter daily data by planting date
# ------------------------------------------------------------------------------
def filter_data_since_planting(daily_temp_data, planting_date_str):
    if not planting_date_str or not daily_temp_data:
        return daily_temp_data
    try:
        planting_dt = datetime.strptime(planting_date_str, "%Y-%m-%d")
    except ValueError:
        return daily_temp_data
    filtered = []
    for day in daily_temp_data:
        day_date_str = day.get("date")
        if day_date_str:
            try:
                day_dt = datetime.strptime(day_date_str, "%Y-%m-%d")
                if day_dt >= planting_dt:
                    filtered.append(day)
            except:
                pass
    return filtered

# ------------------------------------------------------------------------------
# Compute GDD
# ------------------------------------------------------------------------------
def compute_gdd(daily_temp_data, base_temp):
    if not daily_temp_data:
        return None
    total_gdd = 0.0
    for day in daily_temp_data:
        d_tmax = day.get("TMAX")
        d_tmin = day.get("TMIN")
        if d_tmax is not None and d_tmin is not None:
            try:
                avg_temp = (float(d_tmax) + float(d_tmin)) / 2
                daily_gdd = avg_temp - base_temp
                if daily_gdd < 0:
                    daily_gdd = 0
                total_gdd += daily_gdd
            except:
                pass
    return round(total_gdd, 1) if total_gdd > 0 else 0

# ------------------------------------------------------------------------------
# Estimate Growth Stage
# ------------------------------------------------------------------------------
def estimate_growth_stage(crop, gdd_total):
    if gdd_total is None:
        return None
    if crop == "Wheat":
        if gdd_total < 50:
            return "Germination"
        elif gdd_total < 200:
            return "Vegetative"
        elif gdd_total < 400:
            return "Flowering"
        else:
            return "Maturity"
    elif crop == "Rice":
        if gdd_total < 100:
            return "Germination"
        elif gdd_total < 600:
            return "Vegetative"
        elif gdd_total < 1000:
            return "Flowering"
        else:
            return "Maturity"
    elif crop == "Cotton":
        if gdd_total < 50:
            return "Germination"
        elif gdd_total < 350:
            return "Vegetative"
        elif gdd_total < 600:
            return "Flowering"
        else:
            return "Maturity"
    return None

# ------------------------------------------------------------------------------
# Helper: Parse dosage and compute liters needed for the field size
# ------------------------------------------------------------------------------
def parse_dosage_and_compute_amount(dosage_str, field_size_ha):
    """
    If the dosage string contains 'L/ha', parse the lower bound (e.g., '2-3 L/ha' → 2)
    and multiply by field size in hectares to get the total liters.
    The returned string starts with 'Amount:' for easier extraction.
    """
    if "L/ha" in dosage_str:
        try:
            lower_bound_str = dosage_str.split("L/ha")[0].split("-")[0].strip()
            dosage_value = float(lower_bound_str)
            amount_needed = dosage_value * field_size_ha
            return f"Amount: {amount_needed:.2f} liters"
        except:
            return "Dosage calculation unavailable."
    elif "mL/hL" in dosage_str:
        return "Follow product guidelines for mL/hL dosage."
    else:
        return "Follow product guidelines."

# ------------------------------------------------------------------------------
# Recommend Planting Schedule and Fertilizer Timeline with Additional Recommendations
# ------------------------------------------------------------------------------
def recommend_planting_schedule(crop, weather_data, field_size_acres):
    """
    Determine the optimal 7-day planting interval from historical weather data,
    generate a fertilizer timeline with concise instructions (including a key amount),
    and provide additional recommendations for irrigation, soil management, and disease risk.
    """
    # Convert field size from acres to hectares (1 acre ≈ 0.404686 ha)
    field_size_ha = field_size_acres * 0.404686

    # "Optimal" conditions for demonstration (demo values)
    optimal_conditions = {
        "Wheat": {"temp": 15, "rainfall": 2},
        "Rice": {"temp": 20, "rainfall": 4},
        "Cotton": {"temp": 22, "rainfall": 3}
    }
    if crop not in optimal_conditions:
        return {"error": f"Crop '{crop}' not recognized for optimal planting schedule."}
    opt_temp = optimal_conditions[crop]["temp"]
    opt_rain = optimal_conditions[crop]["rainfall"]

    # Sort weather data by date
    weather_data.sort(key=lambda x: x.get("date"))
    
    best_score = float('-inf')
    best_window_start = None
    best_window_end = None
    best_avg_temp = None
    best_avg_rain = None
    n = len(weather_data)
    for i in range(n - 6):
        window = weather_data[i:i+7]
        temps = [day.get("TempAir_DailyAvg (C)") for day in window if day.get("TempAir_DailyAvg (C)") is not None]
        rains = [day.get("Precip_DailySum (mm)") for day in window if day.get("Precip_DailySum (mm)") is not None]
        if not temps or not rains:
            continue
        avg_temp = sum(temps) / len(temps)
        avg_rain = sum(rains) / len(rains)
        score = -abs(avg_temp - opt_temp) - abs(avg_rain - opt_rain)
        if score > best_score:
            best_score = score
            best_window_start = window[0].get("date")
            best_window_end = window[-1].get("date")
            best_avg_temp = avg_temp
            best_avg_rain = avg_rain

    if best_window_start is None:
        return {"error": "Insufficient weather data to determine optimal planting window."}

    # Compute average daily GDD for the entire period
    crop_base_temp = {"Wheat": 5, "Rice": 10, "Cotton": 12}
    base_temp = crop_base_temp.get(crop, 10)
    daily_gdds = []
    for day in weather_data:
        temp = day.get("TempAir_DailyAvg (C)")
        if temp is not None:
            daily_gdd = max(0, temp - base_temp)
            daily_gdds.append(daily_gdd)
    avg_daily_gdd = sum(daily_gdds) / len(daily_gdds) if daily_gdds else 0

    profile = CROP_PROFILES.get(crop, {})
    bio_products = profile.get("BiologicalProducts", {})

    # Build fertilizer timeline with concise messaging
    timeline = []
    timeline.append({
        "day": 0,
        "event": "Planting",
        "instructions": "Planting: Prepare field and sow seeds."
    })

    # Process each biological product
    for product_name, product_info in bio_products.items():
        dosage_str = product_info.get("Dosage", "")
        # For YieldBooster, ensure an amount is specified
        if product_name == "YieldBooster" and dosage_str.strip().lower() == "as per product guidelines":
            dosage_str = "2 L/ha"  # Use a default dosage value
        
        # For products with a GDDRange
        if "GDDRange" in product_info:
            gdd_range = product_info["GDDRange"]
            if isinstance(gdd_range, list) and len(gdd_range) >= 2:
                est_day = int(round(gdd_range[0] / avg_daily_gdd)) if avg_daily_gdd > 0 else "N/A"
                amount_calc = parse_dosage_and_compute_amount(dosage_str, field_size_ha)
                event = {
                    "day": est_day,
                    "product": product_name,
                    "instructions": f"At ~{gdd_range[0]} GDD, apply {product_name}. {amount_calc}"
                }
                perf_data = FERTILIZER_PERFORMANCE_DATA.get(product_name, {}).get(crop)
                if perf_data:
                    event["data"] = perf_data
                timeline.append(event)
        # For products with ApplicationTiming
        elif "ApplicationTiming" in product_info:
            timings = product_info["ApplicationTiming"]
            # For YieldBooster, only process the first timing to avoid duplicates
            if product_name == "YieldBooster" and timings:
                timing = timings[0]
                est_day = 30  # default approximate day
                amount_calc = parse_dosage_and_compute_amount(dosage_str, field_size_ha)
                stage = timing.get("Stage", "recommended stage")
                event = {
                    "day": est_day,
                    "product": product_name,
                    "instructions": f"At {stage} (~day {est_day}), apply {product_name}. {amount_calc}"
                }
                perf_data = FERTILIZER_PERFORMANCE_DATA.get(product_name, {}).get(crop)
                if perf_data:
                    event["data"] = perf_data
                timeline.append(event)
            else:
                # For other products, process all timings
                for timing in timings:
                    est_day = 30  # default approximate day
                    amount_calc = parse_dosage_and_compute_amount(dosage_str, field_size_ha)
                    stage = timing.get("Stage", "recommended stage")
                    event = {
                        "day": est_day,
                        "product": product_name,
                        "instructions": f"At {stage} (~day {est_day}), apply {product_name}. {amount_calc}"
                    }
                    perf_data = FERTILIZER_PERFORMANCE_DATA.get(product_name, {}).get(crop)
                    if perf_data:
                        event["data"] = perf_data
                    timeline.append(event)

    timeline.sort(key=lambda x: x["day"] if isinstance(x["day"], int) else 9999)
    
    # Analyze weather data for dangerous conditions and add enhanced warnings
    max_TMAX = max(day.get("TMAX", 0) for day in weather_data)
    min_TMIN = min(day.get("TMIN", 100) for day in weather_data)
    warnings = []

    if crop == "Wheat":
        TmaxLimit = 32
        if max_TMAX >= TmaxLimit:
            warnings.append(f"ALERT: Dangerous heat - daily max reached {max_TMAX:.1f}°C (limit {TmaxLimit}°C).")
        if min_TMIN < 0:
            warnings.append(f"ALERT: Frost risk - daily min dropped to {min_TMIN:.1f}°C.")
    elif crop == "Rice":
        TmaxLimit = 38
        if max_TMAX >= TmaxLimit:
            warnings.append(f"ALERT: Dangerous heat - daily max reached {max_TMAX:.1f}°C (limit {TmaxLimit}°C).")
        if min_TMIN < 0:
            warnings.append(f"ALERT: Frost risk - daily min dropped to {min_TMIN:.1f}°C.")
    elif crop == "Cotton":
        TmaxLimit = 38
        if max_TMAX >= TmaxLimit:
            warnings.append(f"ALERT: Dangerous heat - daily max reached {max_TMAX:.1f}°C (limit {TmaxLimit}°C).")
        if min_TMIN < 4:
            warnings.append(f"ALERT: Frost risk - daily min dropped to {min_TMIN:.1f}°C.")
    
    if best_avg_rain < 0.5 * opt_rain:
        warnings.append(f"ALERT: Drought risk - average rainfall was only {best_avg_rain:.1f}mm (optimal {opt_rain}mm).")
    
    if not warnings:
        warnings.append("ALERT: Monitor local forecasts; conditions may change unexpectedly.")
    
    # --- New Recommendations Based on Weather and Crop Data ---
    # Irrigation Recommendation based on average rainfall
    if best_avg_rain < 1:
        irrigation_rec = {
            "Suggestion": "Dry period detected – recommend mulching and drip irrigation.",
            "Effect": "Saves water and can boost yield efficiency by ~10%."
        }
    elif best_avg_rain > 5:
        irrigation_rec = {
            "Suggestion": "Heavy rain period – irrigate on demand.",
            "Effect": "Avoids overwatering and reduces water cost by ~15%."
        }
    else:
        irrigation_rec = {
            "Suggestion": "Standard irrigation as per crop requirements.",
            "Effect": "Maintains optimal soil moisture for steady growth."
        }
    
    # Soil Recommendation based on average temperature compared to optimal
    if best_avg_temp > (opt_temp + 2):
        soil_rec = {
            "Suggestion": "High temperature expected – apply organic mulch and consider cover cropping.",
            "Effect": "Reduces evaporation and can improve yield potential by ~10%."
        }
    else:
        soil_rec = {
            "Suggestion": "Maintain current soil management practices.",
            "Effect": "Sustains soil health and nutrient retention."
        }
    
    # Disease Risk Recommendation based on average rainfall
    if best_avg_rain > 4:
        disease_risk = {
            "Suggestion": "Prolonged wet conditions detected – high disease risk.",
            "Effect": "Recommend fungicide and improved drainage to reduce risk by ~20%."
        }
    elif best_avg_rain < 1:
        disease_risk = {
            "Suggestion": "Dry conditions – low risk of disease outbreak.",
            "Effect": "Minimal pathogen activity expected."
        }
    else:
        disease_risk = {
            "Suggestion": "Moderate wetness – moderate disease risk.",
            "Effect": "Monitor crop health and apply preventive measures if needed."
        }
    
    # Return complete output including additional recommendation categories
    return {
        "optimal_planting_interval": {
            "start_date": best_window_start,
            "end_date": best_window_end,
            "average_temperature": round(best_avg_temp, 2),
            "average_rainfall": round(best_avg_rain, 2),
            "score": best_score
        },
        "fertilizer_timeline": timeline,
        "warnings": warnings,
        "irrigation_rec": irrigation_rec,
        "soil_rec": soil_rec,
        "disease_risk": disease_risk
    }

# ------------------------------------------------------------------------------
# Example usage if run directly:
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This file is typically imported by main.py. Example usage:\n")
    sample_data = [
        {"date": "2025-03-01", "TMAX": 25, "TMIN": 15, "TempAir_DailyAvg (C)": 20, "Precip_DailySum (mm)": 0.5},
        {"date": "2025-03-02", "TMAX": 26, "TMIN": 16, "TempAir_DailyAvg (C)": 21, "Precip_DailySum (mm)": 0.3},
        {"date": "2025-03-03", "TMAX": 27, "TMIN": 17, "TempAir_DailyAvg (C)": 22, "Precip_DailySum (mm)": 0.2},
        {"date": "2025-03-04", "TMAX": 24, "TMIN": 14, "TempAir_DailyAvg (C)": 19, "Precip_DailySum (mm)": 1.0},
        {"date": "2025-03-05", "TMAX": 25, "TMIN": 15, "TempAir_DailyAvg (C)": 20, "Precip_DailySum (mm)": 0.8},
        {"date": "2025-03-06", "TMAX": 26, "TMIN": 16, "TempAir_DailyAvg (C)": 21, "Precip_DailySum (mm)": 0.6},
        {"date": "2025-03-07", "TMAX": 27, "TMIN": 17, "TempAir_DailyAvg (C)": 22, "Precip_DailySum (mm)": 0.4},
        {"date": "2025-03-08", "TMAX": 28, "TMIN": 18, "TempAir_DailyAvg (C)": 23, "Precip_DailySum (mm)": 0.5}
    ]
    result = recommend_planting_schedule("Rice", sample_data, 34)
    import json
    print(json.dumps(result, indent=4))