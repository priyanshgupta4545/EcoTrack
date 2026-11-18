"""
EcoTrack - Reusable UI Card Components
Produces polished, modern HTML/CSS cards for KPIs, EcoScore, badges, and tips.
"""

import streamlit as st

def render_kpi_card(title, value, unit, icon, icon_bg="#D1FAE5", subtext="", delta=None, delta_positive=True):
    """
    Renders an attractive SaaS KPI statistic card with icon and delta indicator.
    """
    delta_html = ""
    if delta is not None:
        delta_color = "#10B981" if delta_positive else "#EF4444"
        arrow = "↑" if delta_positive else "↓"
        sign = "+" if delta > 0 else ""
        delta_html = f'<span style="color: {delta_color}; font-weight: 700; font-size: 0.8rem; margin-left: 6px;">{arrow} {sign}{delta}%</span>'

    card_html = f"""
    <div class="stat-card">
        <div class="stat-header">
            <span class="stat-title">{title}</span>
            <div class="stat-icon" style="background-color: {icon_bg};">
                {icon}
            </div>
        </div>
        <div class="stat-value">
            {value} <span style="font-size: 0.95rem; font-weight: 600; color: #64748B;">{unit}</span>
        </div>
        <div class="stat-subtext">
            <span>{subtext}</span>
            {delta_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_ecoscore_card(score_dict):
    """
    Renders the feature showcase card for the user's multi-factor EcoScore.
    """
    score = score_dict.get("score", 0)
    tier = score_dict.get("tier", "Eco Scout 🌱")
    tier_desc = score_dict.get("next_tier_desc", "")
    breakdown = score_dict.get("breakdown", {})

    b_cons = breakdown.get("consistency", 0)
    b_imp = breakdown.get("impact", 0)
    b_div = breakdown.get("diversity", 0)
    b_chal = breakdown.get("challenges", 0)

    html = f"""
    <div class="ecoscore-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #A7F3D0;">
                    Overall Sustainability Index
                </span>
                <h3 style="margin: 0.2rem 0; font-size: 1.6rem; color: #FFFFFF; font-weight: 800;">
                    {tier}
                </h3>
                <p style="margin: 0; color: #D1FAE5; font-size: 0.85rem;">
                    {tier_desc}
                </p>
            </div>
            <div style="text-align: right;">
                <div class="ecoscore-number">{score}</div>
                <div style="font-size: 0.8rem; color: #A7F3D0; font-weight: 600;">out of 100</div>
            </div>
        </div>

        <div style="margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.15);">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
                <div style="background: rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 10px;">
                    <div style="font-size: 0.75rem; color: #A7F3D0;">Consistency</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{b_cons}/30</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 10px;">
                    <div style="font-size: 0.75rem; color: #A7F3D0;">Impact</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{b_imp}/35</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 10px;">
                    <div style="font-size: 0.75rem; color: #A7F3D0;">Diversity</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{b_div}/20</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 10px;">
                    <div style="font-size: 0.75rem; color: #A7F3D0;">Challenges</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">{b_chal}/15</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_badge_card(badge_dict, is_unlocked=False, unlocked_at=None, current_val=0):
    """
    Renders an individual achievement badge card (locked vs unlocked state).
    """
    card_class = "badge-card unlocked" if is_unlocked else "badge-card locked"
    status_text = f"✨ Unlocked on {unlocked_at[:10]}" if is_unlocked else f"🔒 Goal: {badge_dict['requirement_label']}"
    tier_color = "#F59E0B" if badge_dict["tier"] == "Gold" else ("#10B981" if badge_dict["tier"] == "Platinum" else "#64748B")

    progress_html = ""
    if not is_unlocked:
        pct = min(100.0, (current_val / float(badge_dict["threshold"])) * 100.0) if badge_dict["threshold"] > 0 else 0.0
        progress_html = f"""
        <div style="margin-top: 10px; background-color: #E2E8F0; border-radius: 6px; height: 6px; overflow: hidden;">
            <div style="background-color: #10B981; width: {pct}%; height: 100%;"></div>
        </div>
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 4px; text-align: right;">{int(pct)}% complete</div>
        """

    html = f"""
    <div class="{card_class}">
        <div class="badge-card-icon">{badge_dict['icon']}</div>
        <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: {tier_color}; letter-spacing: 0.05em;">
            {badge_dict['tier']} Badge
        </div>
        <h4 style="margin: 0.3rem 0; font-size: 1.05rem; font-weight: 700; color: #0F172A;">{badge_dict['name']}</h4>
        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 0.6rem; min-height: 2.4rem;">
            {badge_dict['description']}
        </p>
        <div style="font-size: 0.75rem; font-weight: 600; color: {'#065F46' if is_unlocked else '#94A3B8'};">
            {status_text}
        </div>
        {progress_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_tip_card(tip_dict):
    """
    Renders an eye-catching daily tip or insight box.
    """
    html = f"""
    <div class="tip-box">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.4rem;">
            <span style="font-size: 1.4rem;">{tip_dict.get('icon', '💡')}</span>
            <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #065F46; letter-spacing: 0.05em;">
                {tip_dict.get('category', 'Eco Tip')}
            </span>
        </div>
        <h4 style="margin: 0 0 0.4rem 0; font-size: 1.15rem; color: #064E3B; font-weight: 700;">
            {tip_dict.get('title', 'Actionable Sustainability Tip')}
        </h4>
        <p style="margin: 0 0 0.6rem 0; font-size: 0.92rem; color: #1E293B; line-height: 1.5;">
            {tip_dict.get('tip', '')}
        </p>
        <div style="font-size: 0.82rem; font-weight: 600; color: #059669; display: flex; align-items: center; gap: 4px;">
            <span>👉 <b>Action Step:</b></span> {tip_dict.get('action', '')}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
