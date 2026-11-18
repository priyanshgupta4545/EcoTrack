"""
=============================================================================
EcoTrack – Smart Sustainability & Environmental Impact Tracker 🌱
=============================================================================
Main Streamlit Application Controller.
Manages application setup, custom styling, database lifecycle,
and modular page routing.
"""

import streamlit as st
import os

# 1. Page Configuration (Must be first Streamlit call)
st.set_page_config(
    page_title="EcoTrack – Sustainability & Environmental Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Theme Styles
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

load_css()

# 3. Database Initialization & Data Loading
import database
import calculations
from components.sidebar import render_sidebar
from components.dashboard import render_home_dashboard
from pages.activities import render_activities_page
from pages.impact import render_impact_page
from pages.challenges import render_challenges_page
from pages.achievements import render_achievements_page
from pages.tips import render_tips_page
from pages.reports import render_reports_page

# Ensure SQLite schema & initial seed demo records are present
database.init_db()

# Load current state
df_activities = database.get_activities()
challenges_list = database.get_challenges()
stats = calculations.get_user_stats(df_activities, challenges_list)

# Synchronize achievement badges based on latest statistics
newly_unlocked = database.sync_badges(stats)
if newly_unlocked:
    for badge in newly_unlocked:
        st.toast(f"🎉 New Achievement Unlocked: {badge['name']} ({badge['icon']})!", icon="🏆")

# 4. Render Sidebar and Navigation
selected_page = render_sidebar(stats)

# 5. Route to Selected Page
if selected_page == "🏠 Home Dashboard":
    render_home_dashboard(df_activities, challenges_list, stats)
elif selected_page == "📝 Activity Tracker":
    render_activities_page(df_activities, stats)
elif selected_page == "🧮 Environmental Impact":
    render_impact_page(stats)
elif selected_page == "🎯 Eco Challenges":
    render_challenges_page(challenges_list, stats)
elif selected_page == "🏆 Achievements & Badges":
    render_achievements_page(stats)
elif selected_page == "💡 Daily Tips & Recycling":
    render_tips_page()
elif selected_page == "📊 Reports & Analytics":
    render_reports_page(df_activities, stats)
else:
    render_home_dashboard(df_activities, challenges_list, stats)
