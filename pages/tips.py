"""
EcoTrack - Daily Eco Tips & Practical Recycling Guide Page
Dynamic rotating daily tips, category filters, and an interactive,
practical recycling decision engine.
"""

import streamlit as st
from datetime import date
from config import DAILY_TIPS, RECYCLING_GUIDE
from components.cards import render_tip_card

def render_tips_page():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            💡 Daily Eco Tips & Recycling Guide
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Evidence-backed micro-tips and a practical, zero-confusion recycling decision manual.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_daily, tab_recycling, tab_all = st.tabs(["🌟 Today's Featured Tip", "♻️ Practical Recycling Directory", "📚 Tip Library"])

    # -------------------------------------------------------------
    # TAB 1: TODAY'S FEATURED TIP
    # -------------------------------------------------------------
    with tab_daily:
        # Compute deterministic daily tip based on day of year
        day_of_year = date.today().timetuple().tm_yday
        featured_tip = DAILY_TIPS[day_of_year % len(DAILY_TIPS)]

        st.markdown("""
        <div class="content-card">
            <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #059669; letter-spacing: 0.05em;">
                Daily Rotating Sustainability Insight
            </span>
            <h3 style="margin: 0.2rem 0 1rem 0; font-size: 1.35rem; font-weight: 800; color: #0F172A;">
                Tip of the Day: {date.today().strftime('%A, %B %d')}
            </h3>
        """.format(date=date), unsafe_allow_html=True)

        render_tip_card(featured_tip)

        st.markdown("""
        <div style="background: #F8FAFC; border-radius: 12px; padding: 14px; margin-top: 1rem; border: 1px solid #E2E8F0;">
            <div style="font-weight: 700; font-size: 0.9rem; color: #0F172A; margin-bottom: 4px;">
                💡 Why Small Habits Compound:
            </div>
            <p style="font-size: 0.85rem; color: #64748B; margin: 0; line-height: 1.5;">
                Behavioral sustainability research shows that anchoring one micro-habit (like turning off the faucet while brushing or keeping a reusable tote by the door) creates a psychological 'spillover effect', leading individuals to adopt 3 to 5 additional pro-environmental behaviors within 60 days.
            </p>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: PRACTICAL RECYCLING DIRECTORY
    # -------------------------------------------------------------
    with tab_recycling:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #065F46;">
                🔍 Can I Recycle This? Searchable Directory
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                Eliminate 'wishcycling' (placing non-recyclables in the blue bin hoping they get recycled). Look up items instantly.
            </p>
        """, unsafe_allow_html=True)

        search_item = st.text_input("Search Item (e.g. pizza, bottle, styrofoam, battery, coffee cup)", placeholder="Type to filter...")

        matched_items = [
            item for item in RECYCLING_GUIDE
            if search_item.lower() in item["item"].lower()
            or search_item.lower() in item["rules"].lower()
            or search_item.lower() in item["preparation"].lower()
        ]

        if matched_items:
            for item in matched_items:
                badge_bg = "#D1FAE5" if item["badge_color"] == "green" else ("#FEF3C7" if item["badge_color"] == "amber" else "#FEE2E2")
                badge_txt = "#065F46" if item["badge_color"] == "green" else ("#92400E" if item["badge_color"] == "amber" else "#991B1B")

                st.markdown(f"""
                <div style="border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px; background: #FFFFFF;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <h4 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: #0F172A;">{item['item']}</h4>
                        <span style="background: {badge_bg}; color: {badge_txt}; font-size: 0.78rem; font-weight: 700; padding: 3px 9px; border-radius: 10px;">
                            {item['recyclable']}
                        </span>
                    </div>
                    <div style="font-size: 0.85rem; color: #334155; margin-bottom: 6px;">
                        <b>Preparation:</b> {item['preparation']}
                    </div>
                    <div style="font-size: 0.82rem; color: #64748B; margin-bottom: 6px;">
                        <b>Sorting Rule:</b> {item['rules']}
                    </div>
                    <div style="font-size: 0.82rem; color: #059669; font-weight: 600;">
                        🌱 <b>Greener Alternative:</b> {item['green_alternative']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"No specific entry found for '{search_item}'. When in doubt, avoid placing non-rigid plastics or food-soiled paper into curbside bins as contamination spoils the whole batch.")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: COMPLETE TIP LIBRARY
    # -------------------------------------------------------------
    with tab_all:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                Browse All Tips by Category
            </h3>
        """, unsafe_allow_html=True)

        cat_choice = st.selectbox("Filter Category", ["All Categories"] + list({t["category"] for t in DAILY_TIPS}))

        filtered_tips = DAILY_TIPS if cat_choice == "All Categories" else [t for t in DAILY_TIPS if t["category"] == cat_choice]

        t_col1, t_col2 = st.columns(2)
        for i, tip in enumerate(filtered_tips):
            col = t_col1 if i % 2 == 0 else t_col2
            with col:
                render_tip_card(tip)

        st.markdown("</div>", unsafe_allow_html=True)
