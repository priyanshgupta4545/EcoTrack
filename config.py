"""
EcoTrack - Configuration & Static Knowledge Base
Contains constants, emission factors, activity presets, badge definitions,
challenge templates, daily tips, and scientific methodology notes.
"""

from datetime import datetime, date

APP_NAME = "EcoTrack"
APP_TAGLINE = "Smart Sustainability & Environmental Impact Tracker 🌱"
APP_VERSION = "2.1.0"

# ---------------------------------------------------------
# Theme & Visual Palette (Forest Green, Emerald, Mint & White)
# ---------------------------------------------------------
THEME = {
    "primary": "#10B981",       # Emerald Green
    "primary_dark": "#065F46",  # Deep Forest Green
    "primary_light": "#D1FAE5", # Mint tint
    "secondary": "#059669",    # Mid Emerald
    "accent_blue": "#0284C7",   # Water Blue
    "accent_amber": "#F59E0B",  # Sun / Energy Amber
    "accent_purple": "#7C3AED", # Innovation Purple
    "bg_main": "#F8FAFC",       # Ultra-light crisp background
    "bg_card": "#FFFFFF",       # Card background
    "text_main": "#0F172A",     # Slate dark text
    "text_muted": "#64748B",    # Slate muted text
    "border": "#E2E8F0",        # Subtle border
}

# ---------------------------------------------------------
# Scientifically Grounded Impact Conversion Factors
# Documented assumptions based on EPA, DEFRA, and IEA averages:
# - Transport: ~0.17 kg CO2e / km saved vs average petrol passenger car (DEFRA/EPA)
# - Water: ~9 L / min shower flow rate; saving 1 min = 9 L water; pumping/heating water = ~0.003 kg CO2e / L
# - Electricity: Grid average emissions factor ~0.40 kg CO2e / kWh (US EPA eGRID / IEA average)
# - Plastic: ~1.50 kg CO2e saved & 1 kg plastic waste diverted per kg plastic (EPA WARM model)
# - Plant-based Meal: ~1.80 kg CO2e avoided & ~1,200 L water conserved compared to average red meat meal
# ---------------------------------------------------------
METHODOLOGY_NOTES = {
    "co2": "Estimates based on US EPA GHG Equivalencies Calculator and UK DEFRA Greenhouse Gas Conversion Factors.",
    "water": "Based on standard residential flow rates (~9 L/min showerheads) and municipal water processing energy profiles.",
    "waste": "Based on EPA Waste Reduction Model (WARM) material life-cycle analysis factors.",
    "electricity": "Calculated using regional average grid emission factor of ~0.40 kg CO2e per kWh consumed.",
    "disclaimer": "All figures provided are calibrated estimates for personal awareness and habit optimization, not ISO-certified corporate lifecycle assessments."
}

# ---------------------------------------------------------
# Master Activity Catalog
# ---------------------------------------------------------
CATEGORIES = [
    "Transportation",
    "Energy Conservation",
    "Water Conservation",
    "Waste & Recycling",
    "Sustainable Food",
    "Eco Lifestyle"
]

CATEGORY_ICONS = {
    "Transportation": "🚲",
    "Energy Conservation": "⚡",
    "Water Conservation": "💧",
    "Waste & Recycling": "♻️",
    "Sustainable Food": "🥗",
    "Eco Lifestyle": "🌿"
}

ACTIVITY_PRESETS = [
    # Transportation
    {
        "id": "walk_cycle",
        "name": "Walked or Cycled instead of Driving",
        "category": "Transportation",
        "unit": "km",
        "co2_kg": 0.170,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.0,
        "icon": "🚲",
        "description": "Replaced private motor vehicle travel with self-powered mobility.",
        "default_qty": 5.0
    },
    {
        "id": "public_transit",
        "name": "Took Bus, Metro or Train",
        "category": "Transportation",
        "unit": "km",
        "co2_kg": 0.100,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.0,
        "icon": "🚆",
        "description": "Chose mass public transit over a single-occupancy personal car trip.",
        "default_qty": 10.0
    },
    {
        "id": "carpool",
        "name": "Carpool / Shared Ride",
        "category": "Transportation",
        "unit": "km",
        "co2_kg": 0.080,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.0,
        "icon": "🚗",
        "description": "Shared a ride with peers, splitting emissions across multiple passengers.",
        "default_qty": 15.0
    },

    # Energy Conservation
    {
        "id": "led_switch",
        "name": "Switched Off Idle Electronics / Lights",
        "category": "Energy Conservation",
        "unit": "hours",
        "co2_kg": 0.040,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.10,
        "icon": "💡",
        "description": "Turned off unoccupied room lighting, computer monitors, or phantom loads.",
        "default_qty": 4.0
    },
    {
        "id": "air_dry_clothes",
        "name": "Air-Dried Laundry (No Tumble Dryer)",
        "category": "Energy Conservation",
        "unit": "loads",
        "co2_kg": 1.200,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 3.00,
        "icon": "👕",
        "description": "Hung wet laundry on a drying rack instead of using an electric tumble dryer.",
        "default_qty": 1.0
    },
    {
        "id": "thermostat_eco",
        "name": "Eco Thermostat / Natural Ventilation",
        "category": "Energy Conservation",
        "unit": "hours",
        "co2_kg": 0.250,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.65,
        "icon": "🌡️",
        "description": "Kept AC set at 24°C+ or relied on natural cross-breeze instead of heating/cooling.",
        "default_qty": 6.0
    },

    # Water Conservation
    {
        "id": "short_shower",
        "name": "Short 5-Minute Shower",
        "category": "Water Conservation",
        "unit": "showers",
        "co2_kg": 0.150,
        "water_l": 45.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.35,
        "icon": "🚿",
        "description": "Halved standard shower time from 10 minutes to 5 minutes, saving hot water.",
        "default_qty": 1.0
    },
    {
        "id": "tap_off_brushing",
        "name": "Turned Tap Off While Brushing/Shaving",
        "category": "Water Conservation",
        "unit": "times",
        "co2_kg": 0.015,
        "water_l": 12.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.02,
        "icon": "🚰",
        "description": "Prevented potable clean water from running down the drain continuously.",
        "default_qty": 2.0
    },
    {
        "id": "rainwater_reuse",
        "name": "Used Rainwater or Greywater for Plants",
        "category": "Water Conservation",
        "unit": "liters",
        "co2_kg": 0.003,
        "water_l": 1.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.005,
        "icon": "🌧️",
        "description": "Captured rainwater or veggie wash water to irrigate house and garden plants.",
        "default_qty": 15.0
    },

    # Waste & Recycling
    {
        "id": "reusable_bottle",
        "name": "Used Reusable Water Bottle / Coffee Mug",
        "category": "Waste & Recycling",
        "unit": "refills",
        "co2_kg": 0.082,
        "water_l": 3.0,
        "waste_kg": 0.025,
        "energy_kwh": 0.12,
        "icon": "🍶",
        "description": "Avoided single-use PET bottled water or disposable wax-lined beverage cups.",
        "default_qty": 3.0
    },
    {
        "id": "recycled_materials",
        "name": "Recycled Plastic, Paper or Cans",
        "category": "Waste & Recycling",
        "unit": "kg",
        "co2_kg": 1.400,
        "water_l": 20.0,
        "waste_kg": 1.000,
        "energy_kwh": 1.80,
        "icon": "📦",
        "description": "Properly segregated and placed recyclable packaging in municipal bins.",
        "default_qty": 1.5
    },
    {
        "id": "reusable_shopping_bag",
        "name": "Brought Reusable Grocery Tote",
        "category": "Waste & Recycling",
        "unit": "bags",
        "co2_kg": 0.035,
        "water_l": 0.5,
        "waste_kg": 0.015,
        "energy_kwh": 0.05,
        "icon": "🛍️",
        "description": "Declined single-use LDPE plastic shopping bags at checkout.",
        "default_qty": 2.0
    },
    {
        "id": "compost_organics",
        "name": "Composted Organic Kitchen Waste",
        "category": "Waste & Recycling",
        "unit": "kg",
        "co2_kg": 0.500,
        "water_l": 0.0,
        "waste_kg": 1.000,
        "energy_kwh": 0.0,
        "icon": "🍂",
        "description": "Diverted food scraps from landfills, preventing anaerobic methane generation.",
        "default_qty": 1.0
    },

    # Sustainable Food
    {
        "id": "plant_based_meal",
        "name": "Chose Plant-Based / Vegetarian Meal",
        "category": "Sustainable Food",
        "unit": "meals",
        "co2_kg": 1.800,
        "water_l": 1200.0,
        "waste_kg": 0.100,
        "energy_kwh": 0.80,
        "icon": "🥗",
        "description": "Substituted high-emission animal protein with legumes, tofu, or grains.",
        "default_qty": 2.0
    },
    {
        "id": "zero_food_waste",
        "name": "Zero Plate Waste / Used Leftovers",
        "category": "Sustainable Food",
        "unit": "meals",
        "co2_kg": 0.850,
        "water_l": 300.0,
        "waste_kg": 0.350,
        "energy_kwh": 0.20,
        "icon": "🍲",
        "description": "Ate planned leftovers and prevented edible food from being thrown away.",
        "default_qty": 1.0
    },

    # Eco Lifestyle
    {
        "id": "planted_tree_seedling",
        "name": "Planted Tree / Nurtured Garden",
        "category": "Eco Lifestyle",
        "unit": "plants",
        "co2_kg": 2.500,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.0,
        "icon": "🌱",
        "description": "Planted a native sapling, bush, or container vegetable to enhance bio-cover.",
        "default_qty": 1.0
    },
    {
        "id": "digital_cleanup",
        "name": "Digital Cleanup (Deleted Inactive Cloud Files)",
        "category": "Eco Lifestyle",
        "unit": "GB",
        "co2_kg": 0.020,
        "water_l": 0.0,
        "waste_kg": 0.0,
        "energy_kwh": 0.05,
        "icon": "💻",
        "description": "Trimmed bloated cloud backups and unneeded emails, lowering data center load.",
        "default_qty": 5.0
    }
]

# Quick lookup dict by activity ID
ACTIVITY_MAP = {act["id"]: act for act in ACTIVITY_PRESETS}
ACTIVITY_NAME_MAP = {act["name"]: act for act in ACTIVITY_PRESETS}

# ---------------------------------------------------------
# Master Challenge Templates
# ---------------------------------------------------------
CHALLENGE_TEMPLATES = [
    {
        "id": "plastic_free_week",
        "title": "Plastic-Free Habit Builder",
        "category": "Waste & Recycling",
        "icon": "🥤",
        "description": "Commit to avoiding disposable single-use plastic bottles, cups, and bags.",
        "target_metric": "plastic_avoided",
        "target_value": 15,
        "target_unit": "items avoided",
        "duration_days": 7,
        "points": 100,
        "difficulty": "Easy"
    },
    {
        "id": "water_guardian",
        "title": "H2O Conservation Sprint",
        "category": "Water Conservation",
        "icon": "💧",
        "description": "Conserve at least 300 Liters of water through 5-min showers and tap mindfulness.",
        "target_metric": "water_saved_l",
        "target_value": 300,
        "target_unit": "Liters saved",
        "duration_days": 10,
        "points": 120,
        "difficulty": "Medium"
    },
    {
        "id": "green_commuter",
        "title": "Pedal & Stride: Green Commuter",
        "category": "Transportation",
        "icon": "🚲",
        "description": "Walk, cycle, or commute sustainably for at least 25 kilometers instead of driving.",
        "target_metric": "green_km",
        "target_value": 25,
        "target_unit": "km travelled",
        "duration_days": 14,
        "points": 150,
        "difficulty": "Medium"
    },
    {
        "id": "power_down",
        "title": "Grid Saver: Power Down Challenge",
        "category": "Energy Conservation",
        "icon": "⚡",
        "description": "Reduce household plug loads and achieve 12 kWh of electricity conservation.",
        "target_metric": "energy_saved_kwh",
        "target_value": 12,
        "target_unit": "kWh conserved",
        "duration_days": 7,
        "points": 110,
        "difficulty": "Easy"
    },
    {
        "id": "zero_waste_week",
        "title": "Zero Waste Warrior",
        "category": "Waste & Recycling",
        "icon": "♻️",
        "description": "Segregate recyclables, compost food scraps, and divert 10 kg of waste from landfills.",
        "target_metric": "waste_diverted_kg",
        "target_value": 10,
        "target_unit": "kg diverted",
        "duration_days": 7,
        "points": 140,
        "difficulty": "Challenging"
    },
    {
        "id": "campus_eco_ambassador",
        "title": "Campus & Community Green Leader",
        "category": "Eco Lifestyle",
        "icon": "🏫",
        "description": "Complete at least one sustainability action across all 5 key environmental categories.",
        "target_metric": "categories_covered",
        "target_value": 5,
        "target_unit": "categories active",
        "duration_days": 14,
        "points": 175,
        "difficulty": "Challenging"
    }
]

# ---------------------------------------------------------
# Master Achievement Badges
# ---------------------------------------------------------
BADGE_DEFINITIONS = [
    {
        "id": "green_beginner",
        "name": "Green Beginner",
        "icon": "🌱",
        "tier": "Bronze",
        "description": "Logged your first eco-friendly action on EcoTrack.",
        "requirement_label": "1 activity logged",
        "threshold": 1,
        "metric": "total_activities"
    },
    {
        "id": "plastic_warrior",
        "name": "Plastic Warrior",
        "icon": "🛡️",
        "tier": "Silver",
        "description": "Diverted or avoided at least 15 single-use plastic items.",
        "requirement_label": "15 plastic units avoided",
        "threshold": 15,
        "metric": "plastic_avoided_count"
    },
    {
        "id": "water_saver",
        "name": "Aqua Protector",
        "icon": "💧",
        "tier": "Silver",
        "description": "Conserved over 200 Liters of water through mindful routines.",
        "requirement_label": "200 Liters water saved",
        "threshold": 200,
        "metric": "total_water_l"
    },
    {
        "id": "carbon_conscious",
        "name": "Carbon Conscious",
        "icon": "🌿",
        "tier": "Gold",
        "description": "Avoided 25+ kg of CO2 equivalent greenhouse emissions.",
        "requirement_label": "25 kg CO2e avoided",
        "threshold": 25.0,
        "metric": "total_co2_kg"
    },
    {
        "id": "clean_commuter",
        "name": "Clean Commuter",
        "icon": "🚲",
        "tier": "Silver",
        "description": "Travelled 30+ km using walking, cycling, or public transit.",
        "requirement_label": "30 km green transit",
        "threshold": 30.0,
        "metric": "transport_km"
    },
    {
        "id": "energy_guardian",
        "name": "Energy Guardian",
        "icon": "⚡",
        "tier": "Silver",
        "description": "Saved 15+ kWh of electrical energy from grid demand.",
        "requirement_label": "15 kWh electricity saved",
        "threshold": 15.0,
        "metric": "total_energy_kwh"
    },
    {
        "id": "streak_master",
        "name": "Habit Builder",
        "icon": "🔥",
        "tier": "Gold",
        "description": "Maintained an active sustainability streak of 4 consecutive days.",
        "requirement_label": "4-day activity streak",
        "threshold": 4,
        "metric": "current_streak"
    },
    {
        "id": "challenge_conqueror",
        "name": "Challenge Conqueror",
        "icon": "🎯",
        "tier": "Gold",
        "description": "Successfully completed at least 2 structured Eco Challenges.",
        "requirement_label": "2 challenges finished",
        "threshold": 2,
        "metric": "challenges_completed"
    },
    {
        "id": "eco_champion",
        "name": "Eco Champion",
        "icon": "🏆",
        "tier": "Platinum",
        "description": "Attained an overall EcoScore of 80 or higher.",
        "requirement_label": "EcoScore >= 80",
        "threshold": 80,
        "metric": "eco_score"
    }
]

# ---------------------------------------------------------
# Daily Tips Catalog
# ---------------------------------------------------------
DAILY_TIPS = [
    {
        "category": "Water Conservation",
        "icon": "💧",
        "title": "The 5-Minute Shower Trick",
        "tip": "Shortening your shower by just 4 minutes saves up to 36 Liters of water and decreases domestic water heating energy by ~20%.",
        "action": "Set a favorite upbeat song as your shower timer."
    },
    {
        "category": "Water Conservation",
        "icon": "🚰",
        "title": "Fix That Dripping Faucet",
        "tip": "A tap dripping once per second wastes roughly 20 Liters of clean drinking water per day — that's over 7,000 Liters a year!",
        "action": "Check tap aerators and replace worn rubber washers."
    },
    {
        "category": "Energy Efficiency",
        "icon": "⚡",
        "title": "Beware Vampire Power Draws",
        "tip": "Devices plugged in on standby (TV boxes, gaming consoles, microwave clocks) account for 5% to 10% of typical home electricity consumption.",
        "action": "Plug entertainment setups into a switchable smart power strip."
    },
    {
        "category": "Energy Efficiency",
        "icon": "❄️",
        "title": "Optimal Fridge & Freezer Temperatures",
        "tip": "Setting your refrigerator between 3°C and 4°C and your freezer at -18°C maintains food safety while minimizing compressor run-time.",
        "action": "Vacuum behind your fridge coils annually to improve efficiency by 15%."
    },
    {
        "category": "Waste Management",
        "icon": "🍕",
        "title": "The Greasy Pizza Box Dilemma",
        "tip": "Cardboard saturated with cheese grease cannot be recycled with clean paper because oils hinder pulp binding. Tear off the clean top lid to recycle, and compost or trash the greasy base.",
        "action": "Separate clean cardboard flaps from grease-soaked bottoms."
    },
    {
        "category": "Waste Management",
        "icon": "♻️",
        "title": "Rinse Before You Bin",
        "tip": "Residual food in yogurt tubs and sauce jars can contaminate an entire municipal recycling batch, sending viable plastics to landfills.",
        "action": "A quick 5-second cold rinse is all that's required."
    },
    {
        "category": "Sustainable Transportation",
        "icon": "🚲",
        "title": "The 2-Kilometer Rule",
        "tip": "Nearly 40% of urban car trips are under 3 kilometers. Cold car engines emit 2x to 3x more pollutants per kilometer than warmed engines.",
        "action": "Dedicate all trips under 2 km to walking, jogging, or cycling."
    },
    {
        "category": "Sustainable Transportation",
        "icon": "🚗",
        "title": "Tire Pressure Efficiency",
        "tip": "Under-inflated tires increase rolling resistance, burning 2% to 4% more fuel. Keeping tires properly pressurized also prolongs tread life.",
        "action": "Check tire pressure at the gas station once a month."
    },
    {
        "category": "Plastic Reduction",
        "icon": "🥤",
        "title": "Say No to Disposable Drink Lids",
        "tip": "Over 500 billion single-use coffee cups and lids are discarded globally each year, most lined with non-compostable polyethylene plastic.",
        "action": "Keep an insulated travel tumbler in your backpack or car."
    },
    {
        "category": "Plastic Reduction",
        "icon": "🛍️",
        "title": "Produce Bag Independence",
        "tip": "Thin plastic film produce bags tear easily and cannot be recycled in standard curbside bins because they jam sorting machinery.",
        "action": "Use washable mesh produce bags or place fruits loose in your cart."
    },
    {
        "category": "Sustainable Food",
        "icon": "🥗",
        "title": "Plant-Forward Swaps",
        "tip": "Swapping just one beef burger per week with a lentil or bean burger avoids ~3.5 kg of greenhouse emissions and saves ~1,500 L of water.",
        "action": "Try cooking 'Meatless Monday' dinners with legumes or tofu."
    },
    {
        "category": "Sustainable Food",
        "icon": "🍲",
        "title": "The 'Eat Me First' Bin",
        "tip": "Roughly 30% of household food waste happens simply because items get hidden at the back of the fridge past their prime.",
        "action": "Designate a front fridge shelf for produce nearing expiration."
    }
]

# ---------------------------------------------------------
# Practical Recycling Search Guide
# ---------------------------------------------------------
RECYCLING_GUIDE = [
    {
        "item": "Plastic Water Bottles (#1 PETE)",
        "recyclable": "Yes - Widely Recycled",
        "badge_color": "green",
        "preparation": "Empty liquid, rinse quickly, crush flat, screw cap back on.",
        "rules": "Accepted in almost all municipal curbside blue bins. Caps should generally remain screwed on modern sorting facilities.",
        "green_alternative": "Stainless steel or glass reusable water bottles."
    },
    {
        "item": "Milk & Detergent Jugs (#2 HDPE)",
        "recyclable": "Yes - High Value",
        "badge_color": "green",
        "preparation": "Rinse completely, replace plastic cap, flatten to save bin volume.",
        "rules": "Highly valuable plastic polymer readily turned into piping, plastic lumber, and new jugs.",
        "green_alternative": "Buy powder detergents in recyclable cardboard or concentrated refills."
    },
    {
        "item": "Cardboard & Shipping Boxes",
        "recyclable": "Yes - Highly Recyclable",
        "badge_color": "green",
        "preparation": "Remove plastic bubble wrap, packing peanuts, and flatten box completely.",
        "rules": "Must remain dry! Wet cardboard breaks down paper fiber lengths and risks mold.",
        "green_alternative": "Reuse clean boxes for storage or gardening mulch weed barrier."
    },
    {
        "item": "Greasy Pizza Boxes",
        "recyclable": "Conditional / Separated",
        "badge_color": "amber",
        "preparation": "Inspect the box: tear off clean top lid for paper bin; place greasy bottom in compost or general waste.",
        "rules": "Food grease and melted cheese cannot be separated from paper fibers during pulping.",
        "green_alternative": "Support local pizzerias that use wax-paper liners or compostable boxes."
    },
    {
        "item": "Plastic Grocery Bags & Soft Film (#4 LDPE)",
        "recyclable": "Special Drop-off Only",
        "badge_color": "amber",
        "preparation": "Must be clean, dry, and bundled into supermarket collection bins.",
        "rules": "DO NOT place in curbside bins! Thin plastic film wraps around conveyor axles in Material Recovery Facilities.",
        "green_alternative": "Durable cotton or hemp reusable tote bags."
    },
    {
        "item": "Styrofoam & Polystyrene (#6 PS)",
        "recyclable": "No (Very Rare Curbside)",
        "badge_color": "red",
        "preparation": "Look for specialized EPS depot drop-offs; otherwise place in household waste.",
        "rules": "Too lightweight and cost-prohibitive to transport for most standard municipal recycling.",
        "green_alternative": "Biodegradable mushroom packaging or molded pulp cardboard."
    },
    {
        "item": "Aluminum Beverage Cans",
        "recyclable": "Yes - Infinitely Recyclable",
        "badge_color": "green",
        "preparation": "Rinse remaining beverage out; no need to crush completely.",
        "rules": "Recycling aluminum uses 95% less energy than producing new metal from bauxite ore. Cans can return to shelves in 60 days.",
        "green_alternative": "Draft / dispenser refills where available."
    },
    {
        "item": "Glass Bottles & Jars",
        "recyclable": "Yes - 100% Infinitely Recyclable",
        "badge_color": "green",
        "preparation": "Rinse residue, remove metal lids (metal lids recycle separately in metal stream).",
        "rules": "Do not mix with pyrex, window glass, or ceramic dishware as their melting temperatures differ.",
        "green_alternative": "Wash jars and reuse for pantry spice and grain storage."
    },
    {
        "item": "Alkaline & Lithium Batteries",
        "recyclable": "Hazardous / Dedicated Depot",
        "badge_color": "red",
        "preparation": "Tape terminal ends with clear scotch or electrical tape to prevent spark hazards.",
        "rules": "NEVER throw in curbside recycling or standard trash. Lithium batteries pose serious fire risks in compacting trucks.",
        "green_alternative": "Switch to NiMH rechargeable batteries with a USB charger."
    },
    {
        "item": "Takeout Coffee Cups",
        "recyclable": "No (General Rule)",
        "badge_color": "red",
        "preparation": "Plastic lid can often be recycled (#5 or #6); cup body goes in general waste.",
        "rules": "Paper cups have an inner polyethylene waterproof lining fused to paper that standard paper mills cannot process.",
        "green_alternative": "Bring your personal reusable ceramic or stainless travel mug."
    },
    {
        "item": "Old Electronics & Cables (E-Waste)",
        "recyclable": "Special E-Waste Collection",
        "badge_color": "amber",
        "preparation": "Factory reset devices to wipe personal data, gather cords neatly.",
        "rules": "Contains precious metals (gold, copper, lithium) and toxic heavy metals (lead, cadmium).",
        "green_alternative": "Donate functional electronics to community centers or trade in."
    }
]

# ---------------------------------------------------------
# Simulated Peer Benchmarks (Clearly marked as Demo Community)
# ---------------------------------------------------------
DEMO_PEERS = [
    {
        "name": "Maya (Eco Ambassador)",
        "avatar": "🌱",
        "score": 92,
        "activities": 48,
        "co2_avoided": 42.5,
        "streak": 12,
        "badge": "Eco Champion",
        "status": "Simulated Demo Benchmark"
    },
    {
        "name": "Alex (Zero Waste Enthusiast)",
        "avatar": "♻️",
        "score": 86,
        "activities": 39,
        "co2_avoided": 36.2,
        "streak": 9,
        "badge": "Plastic Warrior",
        "status": "Simulated Demo Benchmark"
    },
    {
        "name": "Priya (Urban Cyclist)",
        "avatar": "🚲",
        "score": 79,
        "activities": 31,
        "co2_avoided": 31.8,
        "streak": 6,
        "badge": "Clean Commuter",
        "status": "Simulated Demo Benchmark"
    },
    {
        "name": "Jordan (Clean Energy Tech)",
        "avatar": "⚡",
        "score": 74,
        "activities": 25,
        "co2_avoided": 26.0,
        "streak": 4,
        "badge": "Energy Guardian",
        "status": "Simulated Demo Benchmark"
    },
    {
        "name": "Sam (Campus Green Team)",
        "avatar": "🏫",
        "score": 68,
        "activities": 22,
        "co2_avoided": 19.4,
        "streak": 3,
        "badge": "Aqua Protector",
        "status": "Simulated Demo Benchmark"
    }
]
