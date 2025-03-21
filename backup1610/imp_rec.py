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
            "BaselineSOC": 1.0,  # Average SOC in %
            "SequestrationPotential": "0.1-0.2% increase in SOC per year",
            "RecommendedPractices": [
                "Cover cropping with legumes",
                "Conservation tillage",
                "Application of compost or biochar"
            ]
        }
    },
    "Rice": {
        "TotalWaterRequirement": 1200,  # in mm per crop cycle
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
                "GDDRange": [450, 500, 1050, 1100]  # Two application windows
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
            "BaselineSOC": 1.2,  # Average SOC in %
            "SequestrationPotential": "0.2-0.3% increase in SOC per year",
            "RecommendedPractices": [
                "Alternate wetting and drying (AWD) for water management",
                "Application of rice straw compost",
                "Cover cropping with green manure"
            ]
        }
    },
    "Cotton": {
        "TotalWaterRequirement": 700,  # in mm per crop cycle
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
                "GDDRange": [500, 550, 900, 950]  # Two application windows
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
            "BaselineSOC": 0.8,  # Average SOC in %
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
# Recommendation Function Using Updated Crop Profiles
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
    # Use the new crop profiles for valid crops
    valid_crops = list(CROP_PROFILES.keys())
    if not crop or crop not in valid_crops:
        return {"error": f"Invalid or missing 'crop'. Must be one of: {', '.join(valid_crops)}."}

    # Compute accumulated GDD since planting
    crop_base_temp = {"Wheat": 5, "Rice": 10, "Cotton": 12}
    base_temp = crop_base_temp.get(crop, 10)
    filtered_data = filter_data_since_planting(daily_temp_data, planting_date) if daily_temp_data else None
    gdd_total = compute_gdd(filtered_data, base_temp) if filtered_data else None
    estimated_stage = estimate_growth_stage(crop, gdd_total)

    # Calculate weather stress metrics (optional)
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

    # Determine product recommendations based on the updated crop profile and accumulated GDD
    profile = CROP_PROFILES[crop]
    bio_products = profile.get("BiologicalProducts", {})

    recommended_products = []
    detailed_recommendations = []

    # Check StressBuster recommendation
    stress_info = bio_products.get("StressBuster", {})
    stress_gdd_range = stress_info.get("GDDRange")
    if stress_gdd_range and gdd_total is not None:
        # Expecting a list of four numbers: [start1, end1, start2, end2]
        if (stress_gdd_range[0] <= gdd_total <= stress_gdd_range[1]) or (stress_gdd_range[2] <= gdd_total <= stress_gdd_range[3]):
            recommended_products.append("StressBuster")
            detailed_recommendations.append({
                "product": "StressBuster",
                "dosage": stress_info.get("Dosage", "N/A"),
                "applicationFrequency": stress_info.get("ApplicationFrequency", "N/A"),
                "recommendedGDDRange": stress_gdd_range
            })

    # Check YieldBooster recommendation
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
        "detailed_recommendations": detailed_recommendations,
        "crop_profile": profile,
        "inputs_used": {
            "TMAX": TMAX,
            "TMIN": TMIN,
            "average_temp": average_temp,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "wind_dir": wind_dir,
            "cloudcover": cloudcover,
            "sunshine": sunshine,
            "soil_moisture": soil_moisture,
            "evap": evap,
            "pH": pH,
            "nitrogen_applied": nitrogen_applied,
            "projected_yield": projected_yield
        }
    }

# ------------------------------------------------------------------------------
# Example usage if you run imp_rec.py directly:
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This file is typically imported by main.py. Example usage:\n")
    recommendation = recommend_biosimulant(
        crop="Wheat",
        TMAX=13.8,
        TMIN=6.12,
        average_temp=9.06,
        rainfall=0,
        humidity=41,
        wind_speed=1.24,
        wind_dir=180,
        cloudcover=12,
        sunshine=612,
        soil_moisture=25,
        evap=0,
        pH=6.5,
        nitrogen_applied=80,
        projected_yield=3000,
        previous_yields=[3200, 3100, 3300],
        daily_temp_data=[
            {"date": "2025-03-19", "TMAX": 10.5, "TMIN": -0.07},
            {"date": "2025-03-20", "TMAX": 13.8, "TMIN": 6.12},
            {"date": "2025-03-21", "TMAX": 16.4, "TMIN": 5.81}
        ],
        planting_date="2025-02-05"
    )
    import json
    print(json.dumps(recommendation, indent=4))