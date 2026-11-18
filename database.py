"""
EcoTrack - Database Layer (SQLite)
Handles schema initialization, CRUD operations for activities, challenges,
goals, badges, and automated demo data seeding/resetting.
"""

import sqlite3
import os
from datetime import datetime, date, timedelta
import pandas as pd
from config import ACTIVITY_PRESETS, CHALLENGE_TEMPLATES, BADGE_DEFINITIONS

DB_FILE = os.path.join(os.path.dirname(__file__), "data", "ecotrack.db")

def get_connection():
    """Create and return a SQLite database connection with row factory."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables with indexes and initial state."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Activities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        activity_id TEXT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT NOT NULL,
        co2_kg REAL NOT NULL DEFAULT 0.0,
        water_l REAL NOT NULL DEFAULT 0.0,
        waste_kg REAL NOT NULL DEFAULT 0.0,
        energy_kwh REAL NOT NULL DEFAULT 0.0,
        notes TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );
    """)

    # 2. Challenges table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_id TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        target_metric TEXT NOT NULL,
        target_value REAL NOT NULL,
        target_unit TEXT NOT NULL,
        current_value REAL NOT NULL DEFAULT 0.0,
        status TEXT NOT NULL DEFAULT 'active', -- active, completed, abandoned
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        completed_date TEXT,
        points INTEGER NOT NULL DEFAULT 100
    );
    """)

    # 3. Challenge Progress Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenge_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenge_id INTEGER NOT NULL,
        log_date TEXT NOT NULL,
        progress_added REAL NOT NULL,
        notes TEXT DEFAULT '',
        FOREIGN KEY (challenge_id) REFERENCES challenges (id) ON DELETE CASCADE
    );
    """)

    # 4. User Badges table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        badge_id TEXT UNIQUE NOT NULL,
        unlocked_at TEXT NOT NULL
    );
    """)

    # 5. Sustainability Goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_name TEXT NOT NULL,
        metric TEXT NOT NULL, -- co2_kg, water_l, waste_kg, energy_kwh, activities_count
        target_value REAL NOT NULL,
        unit TEXT NOT NULL,
        period TEXT NOT NULL DEFAULT 'monthly', -- monthly, weekly
        created_at TEXT NOT NULL
    );
    """)

    # 6. Settings / Key-Value table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)

    # Create indexes for fast filtering
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activities_date ON activities (date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activities_category ON activities (category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_challenges_status ON challenges (status);")

    conn.commit()

    # Seed demo data if database is brand new
    cursor.execute("SELECT COUNT(*) as cnt FROM activities")
    row = cursor.fetchone()
    if row["cnt"] == 0:
        seed_demo_data(conn)

    conn.close()

def seed_demo_data(conn=None):
    """Populate database with rich, realistic sample records spanning the last 30 days."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    cursor = conn.cursor()
    today = date.today()

    # Clear existing demo data
    cursor.execute("DELETE FROM activities;")
    cursor.execute("DELETE FROM challenges;")
    cursor.execute("DELETE FROM challenge_logs;")
    cursor.execute("DELETE FROM user_badges;")
    cursor.execute("DELETE FROM goals;")

    # Sample activities over the last 28 days
    sample_records = [
        # (days_ago, name, category, quantity, unit, co2_kg, water_l, waste_kg, energy_kwh, notes)
        (28, "Walked or Cycled instead of Driving", "Transportation", 6.0, "km", 1.02, 0.0, 0.0, 0.0, "Cycled to university campus."),
        (27, "Used Reusable Water Bottle / Coffee Mug", "Waste & Recycling", 3.0, "refills", 0.25, 9.0, 0.075, 0.36, "Carried insulated hydro-flask all day."),
        (26, "Short 5-Minute Shower", "Water Conservation", 1.0, "showers", 0.15, 45.0, 0.0, 0.35, "Timed shower with morning playlist."),
        (25, "Chose Plant-Based / Vegetarian Meal", "Sustainable Food", 2.0, "meals", 3.60, 2400.0, 0.20, 1.60, "Tofu stir-fry lunch and lentil curry dinner."),
        (24, "Switched Off Idle Electronics / Lights", "Energy Conservation", 6.0, "hours", 0.24, 0.0, 0.0, 0.60, "Powered off idle desktop monitor and room lamps."),
        (23, "Recycled Plastic, Paper or Cans", "Waste & Recycling", 2.0, "kg", 2.80, 40.0, 2.00, 3.60, "Segregated delivery cardboard and clean plastic bottles."),
        (22, "Took Bus, Metro or Train", "Transportation", 14.0, "km", 1.40, 0.0, 0.0, 0.0, "Public metro commute instead of taxi."),
        (21, "Brought Reusable Grocery Tote", "Waste & Recycling", 3.0, "bags", 0.105, 1.5, 0.045, 0.15, "Weekend grocery run without plastic bags."),
        (20, "Air-Dried Laundry (No Tumble Dryer)", "Energy Conservation", 1.0, "loads", 1.20, 0.0, 0.0, 3.00, "Sun-dried cotton shirts on balcony rack."),
        (19, "Zero Plate Waste / Used Leftovers", "Sustainable Food", 1.0, "meals", 0.85, 300.0, 0.35, 0.20, "Reheated roasted vegetable bake for lunch."),
        (18, "Turned Tap Off While Brushing/Shaving", "Water Conservation", 2.0, "times", 0.03, 24.0, 0.0, 0.04, "Turned faucet off completely while brushing."),
        (17, "Compost Organic Kitchen Waste", "Waste & Recycling", 1.5, "kg", 0.75, 0.0, 1.50, 0.0, "Coffee grounds, apple peels and banana skins composted."),
        (16, "Walked or Cycled instead of Driving", "Transportation", 8.0, "km", 1.36, 0.0, 0.0, 0.0, "Evening bike ride to grocery store."),
        (15, "Chose Plant-Based / Vegetarian Meal", "Sustainable Food", 2.0, "meals", 3.60, 2400.0, 0.20, 1.60, "Black bean burrito bowl and veggie ramen."),
        (14, "Short 5-Minute Shower", "Water Conservation", 1.0, "showers", 0.15, 45.0, 0.0, 0.35, "Quick military-style shower."),
        (13, "Eco Thermostat / Natural Ventilation", "Energy Conservation", 6.0, "hours", 1.50, 0.0, 0.0, 3.90, "Opened windows for cross breeze; AC turned off."),
        (12, "Used Reusable Water Bottle / Coffee Mug", "Waste & Recycling", 4.0, "refills", 0.33, 12.0, 0.10, 0.48, "Refilled at library hydration station."),
        (11, "Planted Tree / Nurtured Garden", "Eco Lifestyle", 2.0, "plants", 5.00, 0.0, 0.0, 0.0, "Planted potted basil and mint on the balcony."),
        (10, "Took Bus, Metro or Train", "Transportation", 18.0, "km", 1.80, 0.0, 0.0, 0.0, "Inter-city electric commuter train."),
        (9,  "Recycled Plastic, Paper or Cans", "Waste & Recycling", 1.8, "kg", 2.52, 36.0, 1.80, 3.24, "Dropped sorted cans at community recycling hub."),
        (8,  "Air-Dried Laundry (No Tumble Dryer)", "Energy Conservation", 1.0, "loads", 1.20, 0.0, 0.0, 3.00, "Air dried bedsheets and towels."),
        (7,  "Short 5-Minute Shower", "Water Conservation", 1.0, "showers", 0.15, 45.0, 0.0, 0.35, "Daily morning 5-minute shower."),
        (6,  "Walked or Cycled instead of Driving", "Transportation", 7.0, "km", 1.19, 0.0, 0.0, 0.0, "Cycled through the city park."),
        (5,  "Chose Plant-Based / Vegetarian Meal", "Sustainable Food", 3.0, "meals", 5.40, 3600.0, 0.30, 2.40, "Fully plant-based day."),
        (4,  "Used Reusable Water Bottle / Coffee Mug", "Waste & Recycling", 4.0, "refills", 0.33, 12.0, 0.10, 0.48, "Coffee in ceramic mug + reusable bottle."),
        (3,  "Switched Off Idle Electronics / Lights", "Energy Conservation", 5.0, "hours", 0.20, 0.0, 0.0, 0.50, "Full study room power down."),
        (2,  "Used Rainwater or Greywater for Plants", "Water Conservation", 18.0, "liters", 0.054, 18.0, 0.0, 0.09, "Used kitchen rinse water on herb garden."),
        (1,  "Walked or Cycled instead of Driving", "Transportation", 5.0, "km", 0.85, 0.0, 0.0, 0.0, "Walked to local market."),
        (0,  "Used Reusable Water Bottle / Coffee Mug", "Waste & Recycling", 3.0, "refills", 0.25, 9.0, 0.075, 0.36, "Tracked refills today at office.")
    ]

    for days_ago, name, category, qty, unit, co2, water, waste, energy, notes in sample_records:
        rec_date = (today - timedelta(days=days_ago)).isoformat()
        cursor.execute("""
        INSERT INTO activities (date, activity_id, name, category, quantity, unit, co2_kg, water_l, waste_kg, energy_kwh, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rec_date, "preset", name, category, qty, unit, co2, water, waste, energy, notes, datetime.now().isoformat()))

    # Seed Sample Challenges (1 active, 1 completed)
    start_c1 = (today - timedelta(days=6)).isoformat()
    end_c1 = (today + timedelta(days=1)).isoformat()
    cursor.execute("""
    INSERT INTO challenges (template_id, title, category, target_metric, target_value, target_unit, current_value, status, start_date, end_date, points)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
    """, ("plastic_free_week", "Plastic-Free Habit Builder", "Waste & Recycling", "plastic_avoided", 15, "items avoided", 11.0, start_c1, end_c1, 100))

    start_c2 = (today - timedelta(days=20)).isoformat()
    end_c2 = (today - timedelta(days=6)).isoformat()
    completed_c2 = (today - timedelta(days=7)).isoformat()
    cursor.execute("""
    INSERT INTO challenges (template_id, title, category, target_metric, target_value, target_unit, current_value, status, start_date, end_date, completed_date, points)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'completed', ?, ?, ?, ?)
    """, ("water_guardian", "H2O Conservation Sprint", "Water Conservation", "water_saved_l", 300, "Liters saved", 320.0, start_c2, end_c2, completed_c2, 120))

    start_c3 = (today - timedelta(days=4)).isoformat()
    end_c3 = (today + timedelta(days=10)).isoformat()
    cursor.execute("""
    INSERT INTO challenges (template_id, title, category, target_metric, target_value, target_unit, current_value, status, start_date, end_date, points)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
    """, ("green_commuter", "Pedal & Stride: Green Commuter", "Transportation", "green_km", 25, "km travelled", 18.0, start_c3, end_c3, 150))

    # Seed Goals
    cursor.execute("""
    INSERT INTO goals (goal_name, metric, target_value, unit, period, created_at)
    VALUES 
    ('Cut 35 kg CO2 this Month', 'co2_kg', 35.0, 'kg CO2', 'monthly', ?),
    ('Save 5,000 Liters Water', 'water_l', 5000.0, 'Liters', 'monthly', ?),
    ('Log 25 Eco-Activities', 'activities_count', 25.0, 'activities', 'monthly', ?),
    ('Save 15 kWh Electricity', 'energy_kwh', 15.0, 'kWh', 'monthly', ?)
    """, (today.isoformat(), today.isoformat(), today.isoformat(), today.isoformat()))

    # Initial Badges
    initial_unlocked = [
        ("green_beginner", (today - timedelta(days=28)).isoformat()),
        ("plastic_warrior", (today - timedelta(days=12)).isoformat()),
        ("water_saver", (today - timedelta(days=7)).isoformat()),
        ("clean_commuter", (today - timedelta(days=6)).isoformat()),
        ("streak_master", (today - timedelta(days=3)).isoformat()),
        ("carbon_conscious", (today - timedelta(days=2)).isoformat())
    ]
    for badge_id, unlocked_at in initial_unlocked:
        cursor.execute("INSERT OR IGNORE INTO user_badges (badge_id, unlocked_at) VALUES (?, ?)", (badge_id, unlocked_at))

    conn.commit()
    if close_after:
        conn.close()

def reset_demo_data():
    """Reset the database back to clean default demonstration data."""
    conn = get_connection()
    seed_demo_data(conn)
    conn.close()

def clear_all_data():
    """Clear all user data for a completely blank state."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities;")
    cursor.execute("DELETE FROM challenges;")
    cursor.execute("DELETE FROM challenge_logs;")
    cursor.execute("DELETE FROM user_badges;")
    cursor.execute("DELETE FROM goals;")
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Activities CRUD Operations
# ---------------------------------------------------------
def get_activities(start_date=None, end_date=None, category=None, search=None):
    """Retrieve filtered activities as a pandas DataFrame."""
    conn = get_connection()
    query = "SELECT * FROM activities WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (name LIKE ? OR notes LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY date DESC, id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_activity_by_id(activity_id):
    """Fetch single activity record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities WHERE id = ?", (activity_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_activity(act_date, activity_id, name, category, quantity, unit, co2_kg, water_l, waste_kg, energy_kwh, notes=""):
    """Insert a new activity record and return inserted ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO activities (date, activity_id, name, category, quantity, unit, co2_kg, water_l, waste_kg, energy_kwh, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (act_date, activity_id, name, category, float(quantity), unit, float(co2_kg), float(water_l), float(waste_kg), float(energy_kwh), notes, datetime.now().isoformat()))
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inserted_id

def update_activity(pk_id, act_date, name, category, quantity, unit, co2_kg, water_l, waste_kg, energy_kwh, notes):
    """Update an existing activity record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE activities
    SET date = ?, name = ?, category = ?, quantity = ?, unit = ?, co2_kg = ?, water_l = ?, waste_kg = ?, energy_kwh = ?, notes = ?
    WHERE id = ?
    """, (act_date, name, category, float(quantity), unit, float(co2_kg), float(water_l), float(waste_kg), float(energy_kwh), notes, pk_id))
    conn.commit()
    conn.close()

def delete_activity(pk_id):
    """Delete an activity record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activities WHERE id = ?", (pk_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Challenges Operations
# ---------------------------------------------------------
def get_challenges(status=None):
    """Retrieve challenges as a list of dicts."""
    conn = get_connection()
    query = "SELECT * FROM challenges"
    params = []
    if status and status != "All":
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def join_challenge(template_id):
    """Join a challenge from template catalog."""
    template = next((t for t in CHALLENGE_TEMPLATES if t["id"] == template_id), None)
    if not template:
        return None

    conn = get_connection()
    cursor = conn.cursor()
    today = date.today()
    end_d = today + timedelta(days=template["duration_days"])

    cursor.execute("""
    INSERT INTO challenges (template_id, title, category, target_metric, target_value, target_unit, current_value, status, start_date, end_date, points)
    VALUES (?, ?, ?, ?, ?, ?, 0.0, 'active', ?, ?, ?)
    """, (template["id"], template["title"], template["category"], template["target_metric"], template["target_value"], template["target_unit"], today.isoformat(), end_d.isoformat(), template["points"]))
    cid = cursor.lastrowid
    conn.commit()
    conn.close()
    return cid

def update_challenge_progress(challenge_id, progress_added, notes=""):
    """Increment progress for an active challenge and check for completion."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM challenges WHERE id = ?", (challenge_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    new_val = row["current_value"] + float(progress_added)
    target = row["target_value"]
    new_status = "active"
    completed_date = None

    if new_val >= target:
        new_status = "completed"
        completed_date = date.today().isoformat()

    cursor.execute("""
    UPDATE challenges
    SET current_value = ?, status = ?, completed_date = ?
    WHERE id = ?
    """, (new_val, new_status, completed_date, challenge_id))

    cursor.execute("""
    INSERT INTO challenge_logs (challenge_id, log_date, progress_added, notes)
    VALUES (?, ?, ?, ?)
    """, (challenge_id, date.today().isoformat(), float(progress_added), notes))

    conn.commit()
    conn.close()
    return new_status == "completed"

def abandon_challenge(challenge_id):
    """Abandon an active challenge."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE challenges SET status = 'abandoned' WHERE id = ?", (challenge_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Goals Operations
# ---------------------------------------------------------
def get_goals():
    """Retrieve all user goals."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals ORDER BY id ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_goal(goal_name, metric, target_value, unit, period="monthly"):
    """Create a new sustainability goal."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO goals (goal_name, metric, target_value, unit, period, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (goal_name, metric, float(target_value), unit, period, date.today().isoformat()))
    conn.commit()
    conn.close()

def delete_goal(goal_id):
    """Delete a goal by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Badges & Achievements Operations
# ---------------------------------------------------------
def get_unlocked_badges():
    """Return dictionary of unlocked badges with their unlock timestamps."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT badge_id, unlocked_at FROM user_badges")
    rows = {r["badge_id"]: r["unlocked_at"] for r in cursor.fetchall()}
    conn.close()
    return rows

def unlock_badge(badge_id):
    """Unlock a badge for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO user_badges (badge_id, unlocked_at)
    VALUES (?, ?)
    """, (badge_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def sync_badges(stats_dict):
    """
    Evaluate all badge conditions against the user's latest statistics.
    Returns list of newly unlocked badge dictionaries.
    """
    unlocked_map = get_unlocked_badges()
    newly_unlocked = []

    for badge in BADGE_DEFINITIONS:
        bid = badge["id"]
        if bid in unlocked_map:
            continue

        metric_key = badge["metric"]
        threshold = badge["threshold"]
        current_val = stats_dict.get(metric_key, 0.0)

        if current_val >= threshold:
            unlock_badge(bid)
            newly_unlocked.append(badge)

    return newly_unlocked
