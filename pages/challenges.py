"""
EcoTrack - Eco Challenges Page
Browse challenge templates, join structured sustainability sprints,
log milestone progress, and earn achievement points.
"""

import streamlit as st
from datetime import date, datetime
from config import CHALLENGE_TEMPLATES
import database

def render_challenges_page(challenges, stats):
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            🎯 Eco Challenges & Sprints
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Commit to structured sustainability goals, track milestones, and earn points to boost your EcoScore.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_active, tab_catalog, tab_history = st.tabs(["🚀 Active Challenges", "🌟 Browse & Join Challenges", "🏁 Completed Sprints"])

    # -------------------------------------------------------------
    # TAB 1: ACTIVE CHALLENGES
    # -------------------------------------------------------------
    with tab_active:
        active_chals = [c for c in challenges if c.get("status") == "active"]

        if active_chals:
            for ch in active_chals:
                cid = ch["id"]
                cur = float(ch.get("current_value", 0.0))
                tgt = float(ch.get("target_value", 1.0))
                pct = min(100, int((cur / tgt) * 100)) if tgt > 0 else 0
                days_left = (datetime.strptime(ch["end_date"], "%Y-%m-%d").date() - date.today()).days
                status_color = "#10B981" if days_left >= 0 else "#EF4444"
                time_label = f"{days_left} days left" if days_left >= 0 else "Sprint overdue"

                st.markdown(f"""
                <div class="challenge-item">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #059669; letter-spacing: 0.05em;">
                                {ch['category']} • {ch['points']} Points
                            </span>
                            <h3 style="margin: 0.2rem 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                                {ch['title']}
                            </h3>
                            <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
                                Started: {ch['start_date']} • Ends: {ch['end_date']} (<span style="color: {status_color}; font-weight: 600;">{time_label}</span>)
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.6rem; font-weight: 800; color: #065F46;">{pct}%</div>
                            <div style="font-size: 0.75rem; color: #64748B;">{cur:.1f} / {tgt:.1f} {ch['target_unit']}</div>
                        </div>
                    </div>

                    <div style="margin: 12px 0 16px 0; background: #E2E8F0; border-radius: 6px; height: 8px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #10B981 0%, #059669 100%); width: {pct}%; height: 100%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Milestone progress logging form for this challenge
                with st.expander(f"📝 Log Milestone Progress for: {ch['title']}", expanded=False):
                    m_col1, m_col2, m_col3 = st.columns([1.5, 2, 1.2])
                    with m_col1:
                        m_inc = st.number_input(f"Add Progress ({ch['target_unit']})", min_value=0.1, max_value=100.0, value=1.0, step=0.5, key=f"prog_{cid}")
                    with m_col2:
                        m_note = st.text_input("Milestone Note", placeholder="e.g. Cycled 5 km to work", key=f"note_{cid}")
                    with m_col3:
                        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                        if st.button("Save Progress", key=f"btn_prog_{cid}", use_container_width=True):
                            completed = database.update_challenge_progress(cid, m_inc, m_note)
                            if completed:
                                st.balloons()
                                st.success(f"🎉 Congratulations! You have successfully completed '{ch['title']}'! +{ch['points']} points earned!")
                            else:
                                st.toast(f"✅ Added {m_inc} {ch['target_unit']} to '{ch['title']}'!", icon="📈")
                            st.rerun()

                st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

        else:
            st.info("You currently have no active challenges. Browse the catalog tab below to join your next sustainability sprint!")

    # -------------------------------------------------------------
    # TAB 2: BROWSE & JOIN CHALLENGES
    # -------------------------------------------------------------
    with tab_catalog:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #065F46;">
                Sustainability Challenge Catalog
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                Pick an initiative that matches your lifestyle goals. Click 'Join Challenge' to start tracking your sprint!
            </p>
        """, unsafe_allow_html=True)

        active_templates = {c.get("template_id") for c in challenges if c.get("status") == "active"}

        for t in CHALLENGE_TEMPLATES:
            is_active = t["id"] in active_templates
            diff_color = "#10B981" if t["difficulty"] == "Easy" else ("#F59E0B" if t["difficulty"] == "Medium" else "#EF4444")

            c_box1, c_box2 = st.columns([4, 1.2])
            with c_box1:
                st.markdown(f"""
                <div style="display: flex; gap: 14px; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #F1F5F9;">
                    <div style="font-size: 2.2rem; background: #F0FDF4; width: 55px; height: 55px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                        {t['icon']}
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">{t['title']}</span>
                            <span style="font-size: 0.72rem; padding: 2px 7px; border-radius: 8px; font-weight: 700; color: {diff_color}; background: #F8FAFC; border: 1px solid #E2E8F0;">
                                {t['difficulty']}
                            </span>
                            <span style="font-size: 0.72rem; padding: 2px 7px; border-radius: 8px; font-weight: 700; color: #059669; background: #D1FAE5;">
                                +{t['points']} pts
                            </span>
                        </div>
                        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748B;">
                            {t['description']}
                        </p>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #0F172A; font-weight: 600;">
                            Target: {t['target_value']} {t['target_unit']} in {t['duration_days']} days
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c_box2:
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
                if is_active:
                    st.button("Active Sprint", key=f"active_{t['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("🚀 Join Challenge", key=f"join_{t['id']}", use_container_width=True):
                        database.join_challenge(t["id"])
                        st.toast(f"🌱 You joined '{t['title']}'! Good luck!", icon="🎯")
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: COMPLETED SPRINTS
    # -------------------------------------------------------------
    with tab_history:
        completed_chals = [c for c in challenges if c.get("status") == "completed"]

        if completed_chals:
            st.markdown("""
            <div class="content-card">
                <h3 style="margin-top: 0; font-size: 1.2rem; font-weight: 700; color: #065F46;">
                    🏆 Your Challenge Hall of Fame
                </h3>
            """, unsafe_allow_html=True)

            for ch in completed_chals:
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8rem;">🏅</span>
                        <div>
                            <div style="font-weight: 700; font-size: 1rem; color: #064E3B;">{ch['title']}</div>
                            <div style="font-size: 0.78rem; color: #059669;">
                                Completed: {ch.get('completed_date', 'Recently')} • Achieved {ch['current_value']:.1f} / {ch['target_value']:.1f} {ch['target_unit']}
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: #10B981; color: #FFFFFF; font-size: 0.8rem; font-weight: 700; padding: 4px 10px; border-radius: 12px;">
                            +{ch['points']} Points
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No completed challenges yet. Work towards completing an active challenge to unlock points!")
