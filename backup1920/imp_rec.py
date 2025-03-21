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
# New Crop Profiles for Wheat, Rice and Cotton
# ------------------------------------------------------------------------------
CROP_PROFILES = {
    "Wheat": {
        "TotalWaterRequirement": 450,  # in mm per crop cycle
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
                "GDDRange": [450, 500, 900, 950]  # Two application windows
            },
            "YieldBooster": {
                "Dosage": "As per product guidelines",
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
                "Dosage": "As per product guidelines",
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
                "Dosage": "As per product guidelines",
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
# Short-Term Recommendation Function
# ------------------------------------------------------------------------------
def recommend_biosimulant(
    crop,
    TMAX=None,
    TMIN=None,
    average_temp=None,
    rainfall=None,
    humidity=None,
    wind_speed=None,
    wind_dir=None,
    cloudcover=None,
    sunshine=None,
    soil_moisture=None,
    evap=None,
    pH=None,
    nitrogen_applied=None,
    projected_yield=None,
    previous_yields=None,
    daily_temp_data=None,
    planting_date=None
):
    valid_crops = list(CROP_PROFILES.keys())
    if not crop or crop not in valid_crops:
        return {"error": f"Invalid or missing 'crop'. Must be one of: {', '.join(valid_crops)}."}
    crop_base_temp = {"Wheat": 5, "Rice": 10, "Cotton": 12}
    base_temp = crop_base_temp.get(crop, 10)
    filtered_data = filter_data_since_planting(daily_temp_data, planting_date) if daily_temp_data else None
    gdd_total = compute_gdd(filtered_data, base_temp) if filtered_data else None
    estimated_stage = estimate_growth_stage(crop, gdd_total)

    if TMAX is not None:
        tmax_opt = 32
        tmax_lim = 45
        if TMAX <= tmax_opt:
            daytime_heat_stress = 0
        elif TMAX >= tmax_lim:
            daytime_heat_stress = 9
        else:
            daytime_heat_stress = 9 * ((TMAX - tmax_opt) / (tmax_lim - tmax_opt))
    else:
        daytime_heat_stress = None

    if TMIN is not None:
        tmin_opt = 22
        tmin_lim = 28
        if TMIN < tmin_opt:
            nighttime_heat_stress = 0
        elif TMIN >= tmin_lim:
            nighttime_heat_stress = 9
        else:
            nighttime_heat_stress = 9 * ((TMIN - tmin_opt) / (tmin_lim - tmin_opt))
    else:
        nighttime_heat_stress = None

    if TMIN is not None:
        tmin_no_frost = 4
        tmin_frost = -3
        if TMIN >= tmin_no_frost:
            frost_stress = 0
        elif TMIN <= tmin_frost:
            frost_stress = 9
        else:
            frost_stress = 9 * abs(TMIN - tmin_no_frost) / abs(tmin_frost - tmin_no_frost)
    else:
        frost_stress = None

    if average_temp is not None and rainfall is not None and evap is not None and soil_moisture is not None:
        DI = (rainfall - evap) if average_temp == 0 else (rainfall - evap) + ((soil_moisture / 100.0) / average_temp)
        if DI > 1.0:
            drought_risk = 0
        elif DI > 0.5:
            drought_risk = 5
        else:
            drought_risk = 9
    else:
        drought_risk = None

    profile = CROP_PROFILES[crop]
    bio_products = profile.get("BiologicalProducts", {})

    recommended_products = []
    detailed_recommendations = []

    stress_info = bio_products.get("StressBuster", {})
    stress_gdd_range = stress_info.get("GDDRange")
    if stress_gdd_range and gdd_total is not None:
        if (stress_gdd_range[0] <= gdd_total <= stress_gdd_range[1]) or (stress_gdd_range[2] <= gdd_total <= stress_gdd_range[3]):
            recommended_products.append("StressBuster")
            detailed_recommendations.append({
                "product": "StressBuster",
                "dosage": stress_info.get("Dosage", "N/A"),
                "applicationFrequency": stress_info.get("ApplicationFrequency", "N/A"),
                "recommendedGDDRange": stress_gdd_range
            })

    yield_info = bio_products.get("YieldBooster", {})
    application_timing = yield_info.get("ApplicationTiming")
    if application_timing and gdd_total is not None:
        for timing in application_timing:
            if isinstance(timing.get("GDD"), list) and len(timing["GDD"]) == 2:
                if timing["GDD"][0] <= gdd_total <= timing["GDD"][1]:
                    recommended_products.append("YieldBooster")
                    detailed_recommendations.append({
                        "product": "YieldBooster",
                        "dosage": yield_info.get("Dosage", "N/A"),
                        "recommendedTiming": timing
                    })
                    break

    if not recommended_products:
        recommended_products = ["No biosimulant strongly indicated"]

    # Return only the recommendation details.
    return {
        "weather_stress": {
            "daytime_heat_stress": daytime_heat_stress,
            "nighttime_heat_stress": nighttime_heat_stress,
            "frost_stress": frost_stress,
            "drought_risk": drought_risk
        },
        "gdd_total": gdd_total,
        "estimated_growth_stage": estimated_stage,
        "recommended_products": recommended_products,
        "detailed_recommendations": detailed_recommendations
    }

# ------------------------------------------------------------------------------
# Extended Recommendation Function for Long-Term Predictions
# ------------------------------------------------------------------------------
def recommend_extended(crop, daily_weather_data, planting_date):
    crop_base_temp = {"Wheat": 5, "Rice": 10, "Cotton": 12}
    base_temp = crop_base_temp.get(crop, 10)
    filtered_data = filter_data_since_planting(daily_weather_data, planting_date)
    gdd_total = compute_gdd(filtered_data, base_temp) if filtered_data else None
    estimated_stage = estimate_growth_stage(crop, gdd_total)

    total_rain = 0
    count = 0
    for day in filtered_data:
        total_rain += safe_float(day.get("Precip_DailySum (mm)"), 0)
        count += 1
    avg_rain = total_rain / count if count > 0 else 0

    profile = CROP_PROFILES.get(crop, {})
    bio_products = profile.get("BiologicalProducts", {})
    recommended_products = []
    detailed_recommendations = []

    stress_info = bio_products.get("StressBuster", {})
    stress_gdd_range = stress_info.get("GDDRange")
    if stress_gdd_range and gdd_total is not None:
        if (stress_gdd_range[0] <= gdd_total <= stress_gdd_range[1]) or (stress_gdd_range[2] <= gdd_total <= stress_gdd_range[3]):
            recommended_products.append("StressBuster")
            detailed_recommendations.append({
                "product": "StressBuster",
                "dosage": stress_info.get("Dosage", "N/A"),
                "applicationFrequency": stress_info.get("ApplicationFrequency", "N/A"),
                "recommendedGDDRange": stress_gdd_range
            })
    yield_info = bio_products.get("YieldBooster", {})
    application_timing = yield_info.get("ApplicationTiming")
    if application_timing and gdd_total is not None:
        for timing in application_timing:
            if isinstance(timing.get("GDD"), list) and len(timing["GDD"]) == 2:
                if timing["GDD"][0] <= gdd_total <= timing["GDD"][1]:
                    recommended_products.append("YieldBooster")
                    detailed_recommendations.append({
                        "product": "YieldBooster",
                        "dosage": yield_info.get("Dosage", "N/A"),
                        "recommendedTiming": timing
                    })
                    break
    if not recommended_products:
        recommended_products = ["No biosimulant strongly indicated"]

    if avg_rain < 1:
        irrigation_rec = {
            "Suggestion": "Dry period detected – recommend mulching and consider drip irrigation.",
            "Effect": "Water saving and improved yield efficiency."
        }
    elif avg_rain > 5:
        irrigation_rec = {
            "Suggestion": "Heavy rain period – irrigate on demand.",
            "Effect": "Avoid overwatering and reduce water cost."
        }
    else:
        irrigation_rec = {
            "Suggestion": "Standard irrigation as per crop requirements.",
            "Effect": "Maintain optimal soil moisture."
        }

    soil_rec = {
        "Suggestion": "Enhance soil quality by applying compost/mulch and consider cover crops.",
        "Effect": "Improves CO₂ sequestration, humus formation, and prevents erosion."
    }

    wet_days = sum(1 for day in filtered_data if safe_float(day.get("Precip_DailySum (mm)"), 0) > 2)
    if count > 0 and wet_days > 0.5 * count:
        disease_rec = {
            "Warning": "Prolonged wet conditions detected – increased disease risk. Monitor crop health and consider preventive measures."
        }
    else:
        disease_rec = {"Status": "Disease risk is low."}

    extended_recommendations = {
        "Biosimulants/Fertilizers": {
            "recommended_products": recommended_products,
            "details": detailed_recommendations
        },
        "Irrigation": irrigation_rec,
        "SoilQuality": soil_rec,
        "DiseaseRisk": disease_rec
    }

    return {
        "total_gdd": gdd_total,
        "estimated_growth_stage": estimated_stage,
        "extended_recommendations": extended_recommendations
    }

# ------------------------------------------------------------------------------
# Example usage if you run imp_rec.py directly:
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This file is typically imported by main.py. Example usage:\n")
    sample_data = [
        {"date": "2025-03-01", "TMAX": 25, "TMIN": 15, "Precip_DailySum (mm)": 0.5, "Evapotranspiration_DailySum (mm)": 5},
        {"date": "2025-03-02", "TMAX": 26, "TMIN": 16, "Precip_DailySum (mm)": 0.3, "Evapotranspiration_DailySum (mm)": 5},
        {"date": "2025-03-03", "TMAX": 27, "TMIN": 17, "Precip_DailySum (mm)": 0.2, "Evapotranspiration_DailySum (mm)": 5}
    ]
    result = recommend_extended("Wheat", sample_data, "2025-03-01")
    import json
    print(json.dumps(result, indent=4))