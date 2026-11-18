"""
EcoTrack - Home Dashboard Component
Main command center showcasing environmental KPIs, EcoScore, quick-log widget,
activity cadence, active challenges, and benchmark leaderboard.
"""

import streamlit as st
import pandas as pd
from datetime import date
from config import CATEGORIES, CATEGORY_ICONS, ACTIVITY_PRESETS, DEMO_PEERS
from components.cards import render_kpi_card, render_ecoscore_card
from components.charts import create_daily_activity_trend, create_category_donut, create_score_radar
from calculations import calculate_activity_impact, calculate_period_comparisons, calculate_equivalencies, get_personalized_recommendations
import database

def render_home_dashboard(df, challenges, stats):
    """
    Renders the complete, polished EcoTrack home dashboard.
    """
    # 1. Hero Banner
    today_str = date.today().strftime("%B %d, %Y")
    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size: 0.88rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.9; margin-bottom: 0.4rem;">
            Welcome back, Eco Warrior • {today_str}
        </div>
        <h1 class="hero-title">Track Habits. Reduce Impact. Inspire Change.</h1>
        <p class="hero-subtitle">
            Every green decision compounds. Monitor your daily environmental stewardship and watch your carbon and resource footprint shrink in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Period Comparisons for KPI Deltas
    comp = calculate_period_comparisons(df)
    deltas = comp["deltas"] if comp else {}

    # 3. Primary KPI Cards Grid (4 columns)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        render_kpi_card(
            title="Total Actions",
            value=f"{stats['total_activities']}",
            unit="logged",
            icon="🌿",
            icon_bg="#D1FAE5",
            subtext="Lifetime activities",
            delta=deltas.get("activities_pct"),
            delta_positive=deltas.get("activities_pct", 0) >= 0
        )

    with kpi_col2:
        render_kpi_card(
            title="CO2 Avoided",
            value=f"{stats['total_co2_kg']:.1f}",
            unit="kg CO2e",
            icon="☁️",
            icon_bg="#E0F2FE",
            subtext="Greenhouse emissions",
            delta=deltas.get("co2_pct"),
            delta_positive=deltas.get("co2_pct", 0) >= 0
        )

    with kpi_col3:
        render_kpi_card(
            title="Water Saved",
            value=f"{stats['total_water_l']:,.0f}",
            unit="Liters",
            icon="💧",
            icon_bg="#E0F2FE",
            subtext="Potable water conserved",
            delta=deltas.get("water_pct"),
            delta_positive=deltas.get("water_pct", 0) >= 0
        )

    with kpi_col4:
        render_kpi_card(
            title="Waste Diverted",
            value=f"{stats['total_waste_kg']:.1f}",
            unit="kg",
            icon="♻️",
            icon_bg="#FEF3C7",
            subtext="Landfill waste prevented",
            delta=None
        )

    # Secondary KPI row (Energy & Streak)
    sec_col1, sec_col2, sec_col3 = st.columns([1, 1, 2])
    with sec_col1:
        render_kpi_card(
            title="Grid Power Saved",
            value=f"{stats['total_energy_kwh']:.1f}",
            unit="kWh",
            icon="⚡",
            icon_bg="#FEF3C7",
            subtext="Electricity conserved",
            delta=deltas.get("energy_pct"),
            delta_positive=deltas.get("energy_pct", 0) >= 0
        )
    with sec_col2:
        render_kpi_card(
            title="Current Habit Streak",
            value=f"{stats['current_streak']}",
            unit="days",
            icon="🔥",
            icon_bg="#FEE2E2",
            subtext=f"Max streak: {stats['max_streak']} days"
        )
    with sec_col3:
        # Equivalencies Banner
        eq = calculate_equivalencies(stats["total_co2_kg"], stats["total_water_l"], stats["total_waste_kg"], stats["total_energy_kwh"])
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.15rem 1.4rem; height: 100%; display: flex; align-items: center; justify-content: space-around; box-shadow: 0 4px 14px rgba(0,0,0,0.03);">
            <div style="text-align: center;">
                <div style="font-size: 1.3rem;">🌲</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #065F46;">{eq['trees_annual']}</div>
                <div style="font-size: 0.72rem; color: #64748B;">Tree-years CO2</div>
            </div>
            <div style="width: 1px; height: 35px; background: #E2E8F0;"></div>
            <div style="text-align: center;">
                <div style="font-size: 1.3rem;">🚗</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #065F46;">{eq['car_km']}</div>
                <div style="font-size: 0.72rem; color: #64748B;">Car km avoided</div>
            </div>
            <div style="width: 1px; height: 35px; background: #E2E8F0;"></div>
            <div style="text-align: center;">
                <div style="font-size: 1.3rem;">🛁</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #0284C7;">{eq['bathtubs']}</div>
                <div style="font-size: 0.72rem; color: #64748B;">Bathtubs water</div>
            </div>
            <div style="width: 1px; height: 35px; background: #E2E8F0;"></div>
            <div style="text-align: center;">
                <div style="font-size: 1.3rem;">📱</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #F59E0B;">{eq['phone_charges']}</div>
                <div style="font-size: 0.72rem; color: #64748B;">Phone charges</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. Main Two-Column Layout
    left_col, right_col = st.columns([7, 5])

    with left_col:
        # EcoScore Showcase
        render_ecoscore_card({
            "score": stats["eco_score"],
            "tier": stats["eco_tier"],
            "next_tier_desc": stats["next_tier_desc"],
            "breakdown": stats["eco_breakdown"]
        })

        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

        # Quick Log Activity Widget
        st.markdown("""
        <div class="content-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;">
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                    ⚡ Quick Log Eco Activity
                </h3>
                <span style="font-size: 0.8rem; color: #10B981; font-weight: 600;">Fast 1-Click Track</span>
            </div>
        """, unsafe_allow_html=True)

        preset_options = [f"{p['icon']} {p['name']} ({p['unit']})" for p in ACTIVITY_PRESETS]
        chosen_preset_label = st.selectbox("Select Activity", preset_options, key="quick_preset_select", label_visibility="collapsed")
        chosen_index = preset_options.index(chosen_preset_label)
        selected_preset = ACTIVITY_PRESETS[chosen_index]

        q_col1, q_col2, q_col3 = st.columns([1.5, 2, 1.2])
        with q_col1:
            q_qty = st.number_input(f"Quantity ({selected_preset['unit']})", min_value=0.1, max_value=500.0, value=float(selected_preset["default_qty"]), step=0.5, key="quick_qty")
        with q_col2:
            q_date = st.date_input("Date", value=date.today(), key="quick_date")
        with q_col3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Log Action", key="quick_log_btn", use_container_width=True):
                impacts = calculate_activity_impact(selected_preset["id"], q_qty)
                database.add_activity(
                    act_date=q_date.isoformat(),
                    activity_id=selected_preset["id"],
                    name=selected_preset["name"],
                    category=selected_preset["category"],
                    quantity=q_qty,
                    unit=selected_preset["unit"],
                    co2_kg=impacts["co2_kg"],
                    water_l=impacts["water_l"],
                    waste_kg=impacts["waste_kg"],
                    energy_kwh=impacts["energy_kwh"],
                    notes="Quick logged from Home Dashboard"
                )
                # Check badges
                database.sync_badges(stats)
                st.toast(f"🌱 Logged: {selected_preset['name']}! Saved {impacts['co2_kg']} kg CO2.", icon="✅")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Recent Activities Feed
        st.markdown("""
        <div class="content-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;">
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                    🕒 Recent Activity Stream
                </h3>
                <span style="font-size: 0.8rem; color: #64748B;">Latest entries</span>
            </div>
        """, unsafe_allow_html=True)

        if df is not None and not df.empty:
            recent_rows = df.head(5)
            for _, r in recent_rows.iterrows():
                icon = CATEGORY_ICONS.get(r["category"], "🌱")
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #F1F5F9;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.4rem;">{icon}</span>
                        <div>
                            <div style="font-weight: 700; font-size: 0.92rem; color: #0F172A;">{r['name']}</div>
                            <div style="font-size: 0.78rem; color: #64748B;">
                                {r['date']} • {r['quantity']} {r['unit']} • {r['category']}
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.88rem; font-weight: 700; color: #10B981;">-{r['co2_kg']:.2f} kg CO2</div>
                        <div style="font-size: 0.75rem; color: #0284C7;">{r['water_l']:.0f} L water</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No activities logged yet. Use the quick logger above to log your first action!")

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        # Daily Activity Trend Plotly
        st.plotly_chart(create_daily_activity_trend(df, days=14), use_container_width=True)

        # Category Donut Plotly
        st.plotly_chart(create_category_donut(df, metric="activities"), use_container_width=True)

        # Active Challenges Preview
        st.markdown("""
        <div class="content-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;">
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                    🎯 Active Challenges
                </h3>
                <span style="font-size: 0.8rem; color: #10B981; font-weight: 600;">In Progress</span>
            </div>
        """, unsafe_allow_html=True)

        active_chals = [c for c in challenges if c.get("status") == "active"]
        if active_chals:
            for ch in active_chals[:2]:
                cur = ch.get("current_value", 0.0)
                tgt = ch.get("target_value", 1.0)
                pct = min(100, int((cur / tgt) * 100)) if tgt > 0 else 0
                st.markdown(f"""
                <div style="padding: 10px; background: #F8FAFC; border-radius: 10px; margin-bottom: 8px; border: 1px solid #E2E8F0;">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 0.88rem; color: #0F172A;">
                        <span>{ch['title']}</span>
                        <span style="color: #10B981;">{pct}%</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 6px;">
                        Progress: {cur:.1f} / {tgt:.1f} {ch['target_unit']}
                    </div>
                    <div style="background: #E2E8F0; border-radius: 4px; height: 6px; overflow: hidden;">
                        <div style="background: #10B981; width: {pct}%; height: 100%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active challenges. Head over to the Eco Challenges page to join one!")

        st.markdown("</div>", unsafe_allow_html=True)

        # Smart Recommendations Card
        recs = get_personalized_recommendations(stats, df)
        if recs:
            st.markdown("""
            <div class="content-card">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;">
                    <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">
                        💡 Smart Recommendations
                    </h3>
                    <span style="font-size: 0.78rem; color: #059669; font-weight: 600;">Personalized</span>
                </div>
            """, unsafe_allow_html=True)
            for r in recs:
                st.markdown(f"""
                <div style="display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid #F1F5F9;">
                    <span style="font-size: 1.3rem;">{r['icon']}</span>
                    <div>
                        <div style="font-weight: 700; font-size: 0.85rem; color: #0F172A;">{r['title']}</div>
                        <div style="font-size: 0.78rem; color: #64748B;">{r['action']}</div>
                        <div style="font-size: 0.72rem; color: #10B981; font-weight: 600; margin-top: 2px;">Potential: {r['potential']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 5. Community Benchmark Leaderboard
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="content-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                    🌐 EcoCampus Community Benchmark
                </h3>
                <span style="font-size: 0.82rem; color: #64748B;">
                    Simulated peer community for friendly motivation & performance comparison
                </span>
            </div>
            <span class="stat-badge badge-green">Simulated Demo Peer Group</span>
        </div>
    """, unsafe_allow_html=True)

    # Build leaderboard data combining user and demo peers
    user_entry = {
        "name": "You (Eco Warrior)",
        "avatar": "🌟",
        "score": stats["eco_score"],
        "activities": stats["total_activities"],
        "co2_avoided": stats["total_co2_kg"],
        "streak": stats["current_streak"],
        "badge": stats["eco_tier"],
        "is_user": True
    }
    all_members = [user_entry] + [{**p, "is_user": False} for p in DEMO_PEERS]
    all_members = sorted(all_members, key=lambda x: x["score"], reverse=True)

    leaderboard_html = '<div style="display: grid; gap: 8px;">'
    for rank, member in enumerate(all_members, 1):
        bg = "#ECFDF5" if member.get("is_user") else "#FFFFFF"
        border = "2px solid #10B981" if member.get("is_user") else "1px solid #E2E8F0"
        rank_badge = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
        
        leaderboard_html += f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: {bg}; border: {border}; border-radius: 12px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-weight: 800; font-size: 1.1rem; width: 30px; text-align: center;">{rank_badge}</span>
                <span style="font-size: 1.3rem;">{member['avatar']}</span>
                <div>
                    <span style="font-weight: 700; font-size: 0.92rem; color: #0F172A;">{member['name']}</span>
                    {' <span style="background: #10B981; color: #fff; font-size: 0.65rem; padding: 2px 6px; border-radius: 8px; font-weight: 700;">YOU</span>' if member.get('is_user') else ''}
                    <div style="font-size: 0.75rem; color: #64748B;">{member['activities']} activities • {member['streak']} day streak</div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.1rem; font-weight: 800; color: #065F46;">{member['score']} <span style="font-size: 0.75rem; font-weight: 600; color: #64748B;">EcoScore</span></div>
                <div style="font-size: 0.75rem; color: #10B981; font-weight: 600;">{member['co2_avoided']} kg CO2</div>
            </div>
        </div>
        """
    leaderboard_html += "</div>"
    st.markdown(leaderboard_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
