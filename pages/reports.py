"""
EcoTrack - Reports & Analytics Page
Comprehensive interactive Plotly analytics suite, period trends,
category breakdowns, and exportable data digests.
"""

import streamlit as st
import pandas as pd
from datetime import date
from config import CATEGORIES
from components.charts import (
    create_category_donut,
    create_daily_activity_trend,
    create_cumulative_impact_chart,
    create_weekly_impact_breakdown,
    create_score_radar
)
from calculations import calculate_period_comparisons
import database

def render_reports_page(df, stats):
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            📊 Analytics, Trends & Environmental Reports
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Deep-dive visualizations of your long-term environmental performance, category balances, and exportable data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("No activity data available to generate reports. Log activities to view analytics.")
        return

    # 1. Filter Bar
    st.markdown("""
    <div class="content-card">
        <h4 style="margin: 0 0 0.8rem 0; font-size: 1.05rem; font-weight: 700; color: #0F172A;">
            Select Reporting Window
        </h4>
    """, unsafe_allow_html=True)

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        date_selection = st.selectbox(
            "Timeframe",
            ["All Time History", "Last 30 Days", "Last 14 Days", "Last 7 Days"]
        )
    with r_col2:
        cat_filter = st.selectbox("Category Filter", ["All Categories"] + CATEGORIES)

    st.markdown("</div>", unsafe_allow_html=True)

    # Filter DataFrame accordingly
    df_filtered = df.copy()
    today = date.today()

    if date_selection == "Last 7 Days":
        cutoff = (today - pd.Timedelta(days=7)).isoformat()
        df_filtered = df_filtered[df_filtered["date"] >= cutoff]
    elif date_selection == "Last 14 Days":
        cutoff = (today - pd.Timedelta(days=14)).isoformat()
        df_filtered = df_filtered[df_filtered["date"] >= cutoff]
    elif date_selection == "Last 30 Days":
        cutoff = (today - pd.Timedelta(days=30)).isoformat()
        df_filtered = df_filtered[df_filtered["date"] >= cutoff]

    if cat_filter != "All Categories":
        df_filtered = df_filtered[df_filtered["category"] == cat_filter]

    # Period Comparison Box
    comp = calculate_period_comparisons(df)
    if comp:
        curr = comp["current"]
        prev = comp["previous"]
        del_dict = comp["deltas"]

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 14px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span style="font-weight: 800; font-size: 1.1rem; color: #0F172A;">
                    📈 14-Day Performance Velocity (Current vs Prior Period)
                </span>
                <span class="stat-badge badge-green">Trend Velocity</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; text-align: center;">
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px;">
                    <div style="font-size: 0.75rem; color: #64748B;">Actions Completed</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #0F172A;">{curr['activities']}</div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: {'#10B981' if del_dict['activities_pct'] >= 0 else '#EF4444'};">
                        {'+' if del_dict['activities_pct'] > 0 else ''}{del_dict['activities_pct']}% vs prior
                    </div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px;">
                    <div style="font-size: 0.75rem; color: #64748B;">CO2 Avoided</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #065F46;">{curr['co2_kg']} kg</div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: {'#10B981' if del_dict['co2_pct'] >= 0 else '#EF4444'};">
                        {'+' if del_dict['co2_pct'] > 0 else ''}{del_dict['co2_pct']}% vs prior
                    </div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px;">
                    <div style="font-size: 0.75rem; color: #64748B;">Water Conserved</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #0284C7;">{curr['water_l']:,.0f} L</div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: {'#10B981' if del_dict['water_pct'] >= 0 else '#EF4444'};">
                        {'+' if del_dict['water_pct'] > 0 else ''}{del_dict['water_pct']}% vs prior
                    </div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px;">
                    <div style="font-size: 0.75rem; color: #64748B;">Power Conserved</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #F59E0B;">{curr['energy_kwh']} kWh</div>
                    <div style="font-size: 0.75rem; font-weight: 700; color: {'#10B981' if del_dict['energy_pct'] >= 0 else '#EF4444'};">
                        {'+' if del_dict['energy_pct'] > 0 else ''}{del_dict['energy_pct']}% vs prior
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Charts Section
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(create_cumulative_impact_chart(df_filtered), use_container_width=True)
    with c2:
        st.plotly_chart(create_weekly_impact_breakdown(df_filtered), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(create_category_donut(df_filtered, metric="co2_kg"), use_container_width=True)
    with c4:
        st.plotly_chart(create_daily_activity_trend(df_filtered, days=21), use_container_width=True)

    # 3. Radar Balance & Export Section
    st.markdown("---")
    rad_col, exp_col = st.columns([1, 1])

    with rad_col:
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 700; color: #0F172A;'>Habit Balance Radar</h4>", unsafe_allow_html=True)
        st.plotly_chart(create_score_radar(stats.get("eco_breakdown", {})), use_container_width=True)

    with exp_col:
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 700; color: #0F172A;'>Data Export & Reports</h4>", unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size: 0.88rem; color: #64748B;">
            Download your raw verified environmental activity ledger for offline portfolio review, academic presentation, or carbon audit verification.
        </p>
        """, unsafe_allow_html=True)

        csv_str = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Activity Report (CSV)",
            data=csv_str,
            file_name=f"ecotrack_report_{today.isoformat()}.csv",
            mime="text/csv",
            use_container_width=True
        )

        json_str = df_filtered.to_json(orient="records", indent=2).encode('utf-8')
        st.download_button(
            label="💾 Download Raw Data (JSON)",
            data=json_str,
            file_name=f"ecotrack_report_{today.isoformat()}.json",
            mime="application/json",
            use_container_width=True
        )
