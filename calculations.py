"""
EcoTrack - Scientific Calculations & Metrics Engine
Provides transparent formulas for environmental impacts, equivalents,
the multi-factor EcoScore algorithm, streaks, and trend analytics.
"""

from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from config import ACTIVITY_PRESETS, ACTIVITY_MAP

# ---------------------------------------------------------
# Equivalencies & Conversion Constants (EPA & DEFRA grounded)
# ---------------------------------------------------------
# 1 mature urban tree absorbs approximately 21.77 kg of CO2 per year (EPA GHG Equivalencies)
CO2_KG_PER_TREE_YEAR = 21.77

# Average single passenger vehicle emits ~0.170 kg CO2 per km (EPA/DEFRA)
CO2_KG_PER_CAR_KM = 0.170

# Average smartphone charge consumes approximately 0.012 kWh of electricity
KWH_PER_PHONE_CHARGE = 0.012

# Standard residential bathtub holds approximately 150 Liters of water
LITERS_PER_BATHTUB = 150.0

# Standard 500ml single-use PET water bottle weighs approx 0.025 kg (25 grams)
KG_PER_PLASTIC_BOTTLE = 0.025

def calculate_activity_impact(activity_id, quantity):
    """
    Given a preset activity_id and quantity, calculate environmental impacts.
    Returns dict: co2_kg, water_l, waste_kg, energy_kwh.
    """
    preset = ACTIVITY_MAP.get(activity_id)
    if not preset:
        return {"co2_kg": 0.0, "water_l": 0.0, "waste_kg": 0.0, "energy_kwh": 0.0}

    q = max(0.0, float(quantity))
    return {
        "co2_kg": round(preset["co2_kg"] * q, 3),
        "water_l": round(preset["water_l"] * q, 2),
        "waste_kg": round(preset["waste_kg"] * q, 3),
        "energy_kwh": round(preset["energy_kwh"] * q, 3),
    }

def calculate_equivalencies(co2_kg, water_l, waste_kg, energy_kwh):
    """
    Convert raw environmental impact metrics into intuitive, human-scale equivalents.
    """
    trees_equivalent = co2_kg / CO2_KG_PER_TREE_YEAR if co2_kg > 0 else 0.0
    car_km_avoided = co2_kg / CO2_KG_PER_CAR_KM if co2_kg > 0 else 0.0
    bathtubs_water = water_l / LITERS_PER_BATHTUB if water_l > 0 else 0.0
    phone_charges = energy_kwh / KWH_PER_PHONE_CHARGE if energy_kwh > 0 else 0.0
    plastic_bottles_equivalent = waste_kg / KG_PER_PLASTIC_BOTTLE if waste_kg > 0 else 0.0

    return {
        "trees_annual": round(trees_equivalent, 2),
        "car_km": round(car_km_avoided, 1),
        "bathtubs": round(bathtubs_water, 1),
        "phone_charges": int(round(phone_charges)),
        "plastic_bottles": int(round(plastic_bottles_equivalent))
    }

def simulate_lifestyle_shift(transport_km_week, shower_min_saved_day, meatless_meals_week, plastic_avoided_week, led_hours_day):
    """
    Simulate what-if lifestyle shifts on a weekly, monthly, and annual scale.
    Transparent, documented formula based on user input parameters.
    """
    # Weekly impact calculations
    co2_weekly = (
        (transport_km_week * 0.170) +              # Walking/cycling vs driving
        (shower_min_saved_day * 7 * 0.030) +       # Hot water energy CO2 (approx 0.03 kg/min)
        (meatless_meals_week * 1.800) +            # Plant-based protein swap
        (plastic_avoided_week * 0.082) +           # Plastic life-cycle
        (led_hours_day * 7 * 0.040)                # Lighting power reduction
    )

    water_weekly = (
        (shower_min_saved_day * 7 * 9.0) +         # 9 L/min shower flow
        (meatless_meals_week * 1200.0) +           # Diet water footprint savings
        (plastic_avoided_week * 3.0)               # Industrial bottle water footprint
    )

    waste_weekly = (
        (plastic_avoided_week * 0.025) +           # 25g bottle per unit
        (meatless_meals_week * 0.100)              # Food packaging & bone waste
    )

    energy_weekly = (
        (shower_min_saved_day * 7 * 0.07) +        # Water heater power
        (meatless_meals_week * 0.80) +             # Agricultural energy
        (led_hours_day * 7 * 0.10)                 # Direct lighting kWh
    )

    # Annual projections (52 weeks)
    annual_co2 = co2_weekly * 52
    annual_water = water_weekly * 52
    annual_waste = waste_weekly * 52
    annual_energy = energy_weekly * 52

    return {
        "weekly": {
            "co2_kg": round(co2_weekly, 2),
            "water_l": round(water_weekly, 1),
            "waste_kg": round(waste_weekly, 2),
            "energy_kwh": round(energy_weekly, 2)
        },
        "annual": {
            "co2_kg": round(annual_co2, 1),
            "water_l": round(annual_water, 0),
            "waste_kg": round(annual_waste, 1),
            "energy_kwh": round(annual_energy, 1),
            "equivalents": calculate_equivalencies(annual_co2, annual_water, annual_waste, annual_energy)
        }
    }

def calculate_streaks(df):
    """
    Calculate current active streak and maximum historical streak in days.
    """
    if df is None or df.empty or "date" not in df.columns:
        return 0, 0

    dates = pd.to_datetime(df["date"]).dt.date.drop_duplicates().sort_values(ascending=False).tolist()
    if not dates:
        return 0, 0

    today = date.today()
    yesterday = today - timedelta(days=1)

    # Check if the streak is active (logged either today or yesterday)
    latest_date = dates[0]
    if latest_date != today and latest_date != yesterday:
        current_streak = 0
    else:
        current_streak = 0
        expected_date = latest_date
        for d in dates:
            if d == expected_date:
                current_streak += 1
                expected_date = d - timedelta(days=1)
            else:
                break

    # Calculate max historical streak
    sorted_asc = sorted(dates)
    max_streak = 1
    running = 1
    for i in range(1, len(sorted_asc)):
        if sorted_asc[i] == sorted_asc[i-1] + timedelta(days=1):
            running += 1
            if running > max_streak:
                max_streak = running
        else:
            running = 1

    return current_streak, max(max_streak, current_streak)

def calculate_ecoscore(stats):
    """
    Multi-factor EcoScore algorithm (0 to 100):
    1. Habit Consistency (Streak & Log Volume): up to 30 points
    2. Environmental Impact (CO2, Water, Waste, Energy): up to 35 points
    3. Habit Diversity (Category Coverage): up to 20 points
    4. Challenges & Community Milestones: up to 15 points
    """
    # 1. Consistency Score (max 30)
    streak = stats.get("current_streak", 0)
    total_acts = stats.get("total_activities", 0)
    streak_pts = min(15.0, streak * 3.0)
    volume_pts = min(15.0, total_acts * 0.75)
    consistency_score = streak_pts + volume_pts

    # 2. Impact Score (max 35)
    co2 = stats.get("total_co2_kg", 0.0)
    water = stats.get("total_water_l", 0.0)
    waste = stats.get("total_waste_kg", 0.0)
    energy = stats.get("total_energy_kwh", 0.0)

    co2_pts = min(12.0, (co2 / 30.0) * 12.0)
    water_pts = min(10.0, (water / 4000.0) * 10.0)
    waste_pts = min(7.0, (waste / 10.0) * 7.0)
    energy_pts = min(6.0, (energy / 20.0) * 6.0)
    impact_score = co2_pts + water_pts + waste_pts + energy_pts

    # 3. Diversity Score (max 20)
    cats_active = stats.get("active_categories_count", 0)
    diversity_score = min(20.0, cats_active * 3.5)

    # 4. Challenge Score (max 15)
    challenges_done = stats.get("challenges_completed", 0)
    challenges_active = stats.get("challenges_active", 0)
    challenge_score = min(15.0, (challenges_done * 7.5) + (challenges_active * 2.5))

    total_score = int(round(min(100.0, max(0.0, consistency_score + impact_score + diversity_score + challenge_score))))

    if total_score >= 80:
        tier = "Eco Champion 🏆"
        tier_color = "#10B981"
        next_tier = "Top Tier Achieved"
    elif total_score >= 60:
        tier = "Sustainability Leader 🌳"
        tier_color = "#059669"
        next_tier = f"{80 - total_score} pts to Eco Champion"
    elif total_score >= 40:
        tier = "Green Advocate 🌿"
        tier_color = "#0284C7"
        next_tier = f"{60 - total_score} pts to Sustainability Leader"
    else:
        tier = "Eco Scout 🌱"
        tier_color = "#F59E0B"
        next_tier = f"{40 - total_score} pts to Green Advocate"

    return {
        "score": total_score,
        "tier": tier,
        "tier_color": tier_color,
        "next_tier_desc": next_tier,
        "breakdown": {
            "consistency": round(consistency_score, 1),
            "impact": round(impact_score, 1),
            "diversity": round(diversity_score, 1),
            "challenges": round(challenge_score, 1)
        }
    }

def get_user_stats(df, challenges_list=None):
    """
    Generate comprehensive user statistics dictionary from activities DataFrame and challenges.
    """
    stats = {
        "total_activities": 0,
        "total_co2_kg": 0.0,
        "total_water_l": 0.0,
        "total_waste_kg": 0.0,
        "total_energy_kwh": 0.0,
        "plastic_avoided_count": 0,
        "transport_km": 0.0,
        "current_streak": 0,
        "max_streak": 0,
        "active_categories_count": 0,
        "categories_list": [],
        "challenges_completed": 0,
        "challenges_active": 0,
        "eco_score": 0,
        "eco_tier": "Eco Scout 🌱",
        "eco_tier_color": "#F59E0B",
        "eco_breakdown": {}
    }

    if df is not None and not df.empty:
        stats["total_activities"] = len(df)
        stats["total_co2_kg"] = round(float(df["co2_kg"].sum()), 2)
        stats["total_water_l"] = round(float(df["water_l"].sum()), 1)
        stats["total_waste_kg"] = round(float(df["waste_kg"].sum()), 2)
        stats["total_energy_kwh"] = round(float(df["energy_kwh"].sum()), 2)

        # Count plastic avoided
        plastic_rows = df[df["name"].str.contains("Reusable Water Bottle|Reusable Grocery|Plastic", case=False, na=False)]
        stats["plastic_avoided_count"] = int(round(plastic_rows["quantity"].sum())) if not plastic_rows.empty else 0

        # Transit km
        transport_rows = df[df["category"] == "Transportation"]
        stats["transport_km"] = round(float(transport_rows["quantity"].sum()), 1) if not transport_rows.empty else 0.0

        # Streaks
        cur_streak, max_streak = calculate_streaks(df)
        stats["current_streak"] = cur_streak
        stats["max_streak"] = max_streak

        # Categories
        unique_cats = df["category"].dropna().unique().tolist()
        stats["active_categories_count"] = len(unique_cats)
        stats["categories_list"] = unique_cats

    if challenges_list:
        stats["challenges_completed"] = sum(1 for c in challenges_list if c.get("status") == "completed")
        stats["challenges_active"] = sum(1 for c in challenges_list if c.get("status") == "active")

    score_data = calculate_ecoscore(stats)
    stats["eco_score"] = score_data["score"]
    stats["eco_tier"] = score_data["tier"]
    stats["eco_tier_color"] = score_data["tier_color"]
    stats["next_tier_desc"] = score_data["next_tier_desc"]
    stats["eco_breakdown"] = score_data["breakdown"]

    return stats

def calculate_period_comparisons(df):
    """
    Calculate progress comparisons: last 14 days vs prior 14 days.
    Returns current period sums, previous period sums, and percentage changes.
    """
    if df is None or df.empty or "date" not in df.columns:
        return None

    df_copy = df.copy()
    df_copy["dt"] = pd.to_datetime(df_copy["date"]).dt.date
    today = date.today()

    p1_start = today - timedelta(days=14)
    p2_start = today - timedelta(days=28)

    current_period = df_copy[df_copy["dt"] >= p1_start]
    prev_period = df_copy[(df_copy["dt"] >= p2_start) & (df_copy["dt"] < p1_start)]

    def calc_delta(curr, prev):
        if prev == 0:
            return 100.0 if curr > 0 else 0.0
        return round(((curr - prev) / prev) * 100.0, 1)

    c_acts = len(current_period)
    p_acts = len(prev_period)
    c_co2 = current_period["co2_kg"].sum()
    p_co2 = prev_period["co2_kg"].sum()
    c_water = current_period["water_l"].sum()
    p_water = prev_period["water_l"].sum()
    c_energy = current_period["energy_kwh"].sum()
    p_energy = prev_period["energy_kwh"].sum()

    return {
        "current": {
            "activities": c_acts,
            "co2_kg": round(c_co2, 2),
            "water_l": round(c_water, 1),
            "energy_kwh": round(c_energy, 2)
        },
        "previous": {
            "activities": p_acts,
            "co2_kg": round(p_co2, 2),
            "water_l": round(p_water, 1),
            "energy_kwh": round(p_energy, 2)
        },
        "deltas": {
            "activities_pct": calc_delta(c_acts, p_acts),
            "co2_pct": calc_delta(c_co2, p_co2),
            "water_pct": calc_delta(c_water, p_water),
            "energy_pct": calc_delta(c_energy, p_energy)
        }
    }

def get_personalized_recommendations(stats, df):
    """
    Provide smart heuristic recommendations based on user's lowest impact or missing habits.
    """
    recs = []
    active_cats = set(stats.get("categories_list", []))

    if "Water Conservation" not in active_cats or stats.get("total_water_l", 0) < 100:
        recs.append({
            "category": "Water Conservation",
            "icon": "💧",
            "title": "Boost Water Savings",
            "action": "Try taking a 5-minute shower tomorrow. You will conserve ~45 Liters in one morning!",
            "potential": "+45 L water / day"
        })

    if "Transportation" not in active_cats or stats.get("transport_km", 0) < 15:
        recs.append({
            "category": "Transportation",
            "icon": "🚲",
            "title": "Switch Your Short Trips",
            "action": "Walk or cycle for errands under 3 km. Reduces emissions by 0.17 kg CO2 per kilometer.",
            "potential": "+0.85 kg CO2 avoided / trip"
        })

    if "Energy Conservation" not in active_cats or stats.get("total_energy_kwh", 0) < 10:
        recs.append({
            "category": "Energy Conservation",
            "icon": "⚡",
            "title": "Tackle Standby Power",
            "action": "Unplug phone chargers and idle workspace screens at night to cut phantom draw.",
            "potential": "+0.5 kWh / day saved"
        })

    if "Sustainable Food" not in active_cats:
        recs.append({
            "category": "Sustainable Food",
            "icon": "🥗",
            "title": "Plant-Powered Day",
            "action": "Choose a delicious vegetarian or plant-based meal today to save water and greenhouse gases.",
            "potential": "~1.8 kg CO2 & 1,200 L water"
        })

    if stats.get("current_streak", 0) < 3:
        recs.append({
            "category": "Consistency",
            "icon": "🔥",
            "title": "Build a 3-Day Habit Streak",
            "action": "Log at least 1 simple action daily (e.g. reusable bottle refill) to activate Streak Master badge.",
            "potential": "+10 EcoScore points"
        })

    return recs[:3]
