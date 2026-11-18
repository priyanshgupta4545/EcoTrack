"""
EcoTrack - Achievements & Sustainability Goals Page
Badges showcase, unlock milestones, and personal sustainability target management.
"""

import streamlit as st
from config import BADGE_DEFINITIONS
from components.cards import render_badge_card
import database

def render_achievements_page(stats):
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            🏆 Achievements, Badges & Goals
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Celebrate your milestones, unlock prestigious sustainability badges, and manage personal goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_badges, tab_goals = st.tabs(["🎖️ Badge Showcase", "🎯 Personal Sustainability Goals"])

    # -------------------------------------------------------------
    # TAB 1: BADGE SHOWCASE
    # -------------------------------------------------------------
    with tab_badges:
        # Sync badges against user stats
        database.sync_badges(stats)
        unlocked_map = database.get_unlocked_badges()

        unlocked_count = len(unlocked_map)
        total_badges = len(BADGE_DEFINITIONS)
        completion_pct = int((unlocked_count / total_badges) * 100) if total_badges > 0 else 0

        # Badge Progress Header Banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065F46 0%, #059669 100%); border-radius: 18px; padding: 1.5rem 1.8rem; color: #FFFFFF; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #A7F3D0; letter-spacing: 0.08em;">
                        EcoTrack Mastery Room
                    </span>
                    <h3 style="margin: 0.2rem 0; font-size: 1.5rem; font-weight: 800; color: #FFFFFF;">
                        {unlocked_count} of {total_badges} Badges Unlocked ({completion_pct}%)
                    </h3>
                    <p style="margin: 0; font-size: 0.85rem; color: #D1FAE5;">
                        Every badge represents verifiable reductions in real-world carbon emissions and resource depletion.
                    </p>
                </div>
                <div style="font-size: 2.8rem;">🏅</div>
            </div>
            <div style="margin-top: 14px; background: rgba(255, 255, 255, 0.2); border-radius: 6px; height: 8px; overflow: hidden;">
                <div style="background: #34D399; width: {completion_pct}%; height: 100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3-Column Badges Grid
        cols = st.columns(3)
        for i, b in enumerate(BADGE_DEFINITIONS):
            col = cols[i % 3]
            is_unlocked = b["id"] in unlocked_map
            unlocked_at = unlocked_map.get(b["id"])
            current_val = stats.get(b["metric"], 0.0)

            with col:
                render_badge_card(
                    badge_dict=b,
                    is_unlocked=is_unlocked,
                    unlocked_at=unlocked_at,
                    current_val=current_val
                )
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: PERSONAL SUSTAINABILITY GOALS
    # -------------------------------------------------------------
    with tab_goals:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                Monthly Sustainability Goals
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                Set personal targets to challenge yourself each month. Track actual progress against each milestone.
            </p>
        """, unsafe_allow_html=True)

        user_goals = database.get_goals()

        if user_goals:
            for g in user_goals:
                gid = g["id"]
                metric = g["metric"]
                tgt = float(g["target_value"])
                cur = float(stats.get(f"total_{metric}", stats.get(metric, 0.0)))
                # Specific mapping for activities_count
                if metric == "activities_count":
                    cur = float(stats.get("total_activities", 0))

                pct = min(100, int((cur / tgt) * 100)) if tgt > 0 else 0

                g_col1, g_col2 = st.columns([5, 1])
                with g_col1:
                    st.markdown(f"""
                    <div style="margin-bottom: 14px; padding: 12px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px;">
                        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.95rem; color: #0F172A;">
                            <span>🎯 {g['goal_name']}</span>
                            <span style="color: #10B981;">{pct}% Completed</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748B; margin: 4px 0 8px 0;">
                            Current: <b>{cur:.1f}</b> / Target: <b>{tgt:.1f} {g['unit']}</b> ({g['period'].capitalize()})
                        </div>
                        <div style="background: #E2E8F0; border-radius: 4px; height: 8px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #10B981, #059669); width: {pct}%; height: 100%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with g_col2:
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                    if st.button("Delete", key=f"del_goal_{gid}", use_container_width=True):
                        database.delete_goal(gid)
                        st.toast("Goal deleted.", icon="🗑️")
                        st.rerun()

        st.markdown("---")

        # Create New Goal Form
        st.markdown("<h4 style='font-size: 1.05rem; font-weight: 700; color: #0F172A;'>Add a New Goal</h4>", unsafe_allow_html=True)
        with st.form("new_goal_form"):
            g1, g2, g3 = st.columns(3)
            with g1:
                g_name = st.text_input("Goal Name", placeholder="e.g. Save 20 kg CO2 this month")
            with g2:
                g_metric = st.selectbox("Target Metric", [
                    ("CO2 Avoided (kg)", "co2_kg", "kg CO2"),
                    ("Water Saved (L)", "water_l", "Liters"),
                    ("Waste Diverted (kg)", "waste_kg", "kg"),
                    ("Energy Saved (kWh)", "energy_kwh", "kWh"),
                    ("Total Activities Logged", "activities_count", "activities")
                ], format_func=lambda x: x[0])
            with g3:
                g_target = st.number_input("Target Value", min_value=1.0, value=25.0, step=5.0)

            submitted_goal = st.form_submit_button("➕ Save Sustainability Goal", use_container_width=True)
            if submitted_goal:
                if not g_name.strip():
                    st.error("Please enter a goal title.")
                else:
                    database.add_goal(
                        goal_name=g_name.strip(),
                        metric=g_metric[1],
                        target_value=g_target,
                        unit=g_metric[2],
                        period="monthly"
                    )
                    st.success(f"Goal '{g_name}' successfully created!")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
