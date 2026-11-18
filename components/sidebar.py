"""
EcoTrack - Modern Sidebar Component
Renders the navigation menu, user sustainability summary, and database controls.
"""

import streamlit as st
from config import APP_NAME, APP_TAGLINE, APP_VERSION
import database

def render_sidebar(stats):
    """
    Renders the custom branded sidebar and returns the selected page name.
    """
    with st.sidebar:
        # App Branding Header
        st.markdown(f"""
        <div style="padding: 0.5rem 0 1.2rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.15);">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2.2rem;">🌱</span>
                <div>
                    <h2 style="margin: 0; color: #FFFFFF !important; font-size: 1.55rem; font-weight: 800; letter-spacing: -0.02em;">
                        {APP_NAME}
                    </h2>
                    <span style="font-size: 0.75rem; color: #A7F3D0 !important; font-weight: 600;">v{APP_VERSION} • Smart Tracker</span>
                </div>
            </div>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #D1FAE5 !important; line-height: 1.35;">
                {APP_TAGLINE}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # User Live Snapshot
        streak = stats.get("current_streak", 0)
        score = stats.get("eco_score", 0)
        tier = stats.get("eco_tier", "Eco Scout 🌱")

        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.12);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 0.75rem; text-transform: uppercase; color: #A7F3D0; font-weight: 700;">Member Profile</span>
                <span style="background: rgba(16, 185, 129, 0.3); color: #FFFFFF; font-size: 0.72rem; padding: 2px 7px; border-radius: 12px; font-weight: 600;">Active</span>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">EcoScore: {score}</div>
                    <div style="font-size: 0.75rem; color: #D1FAE5;">{tier}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #F59E0B;">🔥 {streak} Days</div>
                    <div style="font-size: 0.75rem; color: #A7F3D0;">Active Streak</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation Options
        pages = [
            "🏠 Home Dashboard",
            "📝 Activity Tracker",
            "🧮 Environmental Impact",
            "🎯 Eco Challenges",
            "🏆 Achievements & Badges",
            "💡 Daily Tips & Recycling",
            "📊 Reports & Analytics"
        ]

        if "current_page" not in st.session_state:
            st.session_state["current_page"] = pages[0]

        selected_page = st.radio(
            "Navigate",
            pages,
            index=pages.index(st.session_state["current_page"]) if st.session_state["current_page"] in pages else 0,
            label_visibility="collapsed"
        )
        st.session_state["current_page"] = selected_page

        st.markdown("---")

        # Database Management / Reset Demo
        st.markdown("<span style='font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; color: #A7F3D0;'>Data Controls</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Demo", use_container_width=True, help="Re-seed database with realistic 30-day demo activities"):
                database.reset_demo_data()
                st.toast("✅ Demo data refreshed successfully!", icon="🌱")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True, help="Wipe all activities and challenges to start fresh"):
                database.clear_all_data()
                st.toast("🧹 Database reset to clean state.", icon="✨")
                st.rerun()

        # Scientific Methodology Note
        with st.expander("ℹ️ Scientific Assumptions", expanded=False):
            st.markdown("""
            <div style="font-size: 0.75rem; color: #D1FAE5; line-height: 1.4;">
            <b>Assumptions & Sources:</b><br>
            • Transport: EPA / UK DEFRA ~0.17 kg CO2e / km saved vs car.<br>
            • Water: ~9 L/min standard shower; ~0.003 kg CO2e / L water pumping.<br>
            • Electricity: US EPA eGRID grid average ~0.40 kg CO2e / kWh.<br>
            • Plastic: EPA WARM factor ~1.5 kg CO2e saved / kg recycled.<br>
            <i>All values are calibrated estimates for personal habit coaching.</i>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; font-size: 0.72rem; color: #A7F3D0;">
            EcoTrack Platform • Hackathon Portfolio Edition
        </div>
        """, unsafe_allow_html=True)

        return selected_page
