"""
EcoTrack - Environmental Impact Calculator & Methodology
Interactive what-if lifestyle simulator, tangible equivalencies,
and transparent scientific assumptions.
"""

import streamlit as st
from calculations import simulate_lifestyle_shift, calculate_equivalencies
from config import METHODOLOGY_NOTES

def render_impact_page(stats):
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            🧮 Environmental Impact Calculator
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Simulate the compounded environmental benefits of small lifestyle shifts and explore the scientific assumptions behind EcoTrack.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_sim, tab_eq, tab_method = st.tabs(["🔮 Lifestyle Shift Simulator", "🌳 Human-Scale Equivalencies", "📚 Scientific Methodology"])

    # -------------------------------------------------------------
    # TAB 1: WHAT-IF SIMULATOR
    # -------------------------------------------------------------
    with tab_sim:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #065F46;">
                What-If Lifestyle Simulator
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                Adjust the habit sliders below to model how daily micro-habits compound into massive resource savings over a year.
            </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            s_km = st.slider("🚲 Green Commute (Walk/Cycle vs Car)", min_value=0, max_value=100, value=15, step=5, help="Kilometers per week")
            s_shower = st.slider("🚿 Shower Shortening", min_value=0, max_value=15, value=4, step=1, help="Minutes saved per day")
            s_meatless = st.slider("🥗 Plant-Forward Meals", min_value=0, max_value=21, value=4, step=1, help="Meatless meals per week")
        with col2:
            s_bottles = st.slider("🍶 Single-Use Bottles Avoided", min_value=0, max_value=30, value=7, step=1, help="Refills per week")
            s_led = st.slider("💡 Lights / Electronics Powered Down", min_value=0, max_value=12, value=4, step=1, help="Hours saved per day")

        sim_results = simulate_lifestyle_shift(s_km, s_shower, s_meatless, s_bottles, s_led)
        w = sim_results["weekly"]
        a = sim_results["annual"]
        eq = a["equivalents"]

        st.markdown("---")

        # Annual Impact Showcase
        st.markdown("<h4 style='font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-bottom: 0.8rem;'>Projected Annual Environmental Savings</h4>", unsafe_allow_html=True)

        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        with res_col1:
            st.metric("Annual CO2 Avoided", f"{a['co2_kg']:,.1f} kg", f"{w['co2_kg']} kg / week")
        with res_col2:
            st.metric("Annual Water Saved", f"{a['water_l']:,.0f} L", f"{w['water_l']:,.0f} L / week")
        with res_col3:
            st.metric("Annual Waste Diverted", f"{a['waste_kg']:,.1f} kg", f"{w['waste_kg']} kg / week")
        with res_col4:
            st.metric("Annual Energy Saved", f"{a['energy_kwh']:,.1f} kWh", f"{w['energy_kwh']} kWh / week")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Tangible Visual Equivalents
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065F46 0%, #059669 100%); border-radius: 16px; padding: 1.4rem; color: #FFFFFF;">
            <h4 style="margin: 0 0 1rem 0; font-size: 1.15rem; color: #FFFFFF; font-weight: 700;">
                🌍 What this means in the real world:
            </h4>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; text-align: center;">
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px;">
                    <div style="font-size: 1.8rem;">🌲</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #34D399;">{eq['trees_annual']}</div>
                    <div style="font-size: 0.75rem; color: #D1FAE5;">Urban tree carbon absorption years</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px;">
                    <div style="font-size: 1.8rem;">🚗</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #34D399;">{eq['car_km']:,.0f} km</div>
                    <div style="font-size: 0.75rem; color: #D1FAE5;">Gasoline car driving emissions erased</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px;">
                    <div style="font-size: 1.8rem;">🛁</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #38BDF8;">{eq['bathtubs']:,.0f}</div>
                    <div style="font-size: 0.75rem; color: #E0F2FE;">Full bathtubs of clean drinking water</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px;">
                    <div style="font-size: 1.8rem;">⚡</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #FCD34D;">{eq['phone_charges']:,.0f}</div>
                    <div style="font-size: 0.75rem; color: #FEF3C7;">Smartphone battery recharges</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: PERSONAL TANGIBLE EQUIVALENTS
    # -------------------------------------------------------------
    with tab_eq:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                Your Personal Actual Impact Equivalencies
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                Based on your actual logged activities on EcoTrack so far:
            </p>
        """, unsafe_allow_html=True)

        actual_eq = calculate_equivalencies(
            stats["total_co2_kg"],
            stats["total_water_l"],
            stats["total_waste_kg"],
            stats["total_energy_kwh"]
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 14px; padding: 18px; text-align: center;">
                <div style="font-size: 2.2rem;">🌳</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #065F46;">{actual_eq['trees_annual']} Trees</div>
                <div style="font-size: 0.85rem; color: #059669; font-weight: 600; margin-top: 4px;">Carbon Absorption Equivalent</div>
                <p style="font-size: 0.78rem; color: #64748B; margin-top: 8px;">
                    Equivalent to the annual carbon sequestered by {actual_eq['trees_annual']} mature urban trees grown for one full year.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 14px; padding: 18px; text-align: center;">
                <div style="font-size: 2.2rem;">🚗</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #0369A1;">{actual_eq['car_km']} km</div>
                <div style="font-size: 0.85rem; color: #0284C7; font-weight: 600; margin-top: 4px;">Car Driving Eliminated</div>
                <p style="font-size: 0.78rem; color: #64748B; margin-top: 8px;">
                    Equivalent to avoiding emissions from driving an average petrol car for {actual_eq['car_km']} kilometers.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div style="background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 14px; padding: 18px; text-align: center;">
                <div style="font-size: 2.2rem;">📱</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #B45309;">{actual_eq['phone_charges']} Charges</div>
                <div style="font-size: 0.85rem; color: #D97706; font-weight: 600; margin-top: 4px;">Smartphones Powered</div>
                <p style="font-size: 0.78rem; color: #64748B; margin-top: 8px;">
                    Conserved enough electricity to fully charge an average smartphone battery {actual_eq['phone_charges']} times.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: SCIENTIFIC METHODOLOGY
    # -------------------------------------------------------------
    with tab_method:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.25rem; font-weight: 700; color: #0F172A;">
                Methodology & Transparent Assumptions
            </h3>
            <p style="color: #64748B; font-size: 0.88rem;">
                EcoTrack adheres to open, transparent emission factors calibrated from recognized environmental agencies.
            </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        > ℹ️ **Notice & Scientific Framing:**<br>
        > {METHODOLOGY_NOTES['disclaimer']}
        """, unsafe_allow_html=True)

        st.markdown("""
        | Environmental Dimension | Calibration Factor | Primary Reference Source | Rationale & Methodology |
        | :--- | :--- | :--- | :--- |
        | **Transportation** | **0.170 kg CO2e / km** | US EPA GHG Equivalencies & UK DEFRA | Represents the average tailpipe and upstream fuel combustion emissions of a typical passenger sedan (petrol). Walking or cycling cancels this emission completely. |
        | **Mass Transit Shift** | **0.100 kg CO2e / km** | Federal Transit Administration (FTA) | Average bus/metro occupancy creates ~0.07 kg CO2/km vs 0.17 kg for single passenger car, yielding a net avoidance of 0.10 kg/km. |
        | **Water Conservation** | **9.0 Liters / min** | US EPA WaterSense Standards | Standard low-to-medium flow showerhead delivers 9 Liters of potable water per minute. Cutting a shower from 10 min to 5 min saves 45 Liters. |
        | **Water Heating Energy** | **0.003 kg CO2e / L** | Lawrence Berkeley National Laboratory | Pumping, treating, and heating residential potable water requires ~0.008 kWh electrical or thermal equivalent per Liter. |
        | **Grid Electricity** | **0.400 kg CO2e / kWh** | US EPA eGRID Subregion Averages & IEA | Represents average combined marginal grid emission factor across mixed fossil and renewable regional grids. |
        | **Plastic Packaging** | **1.400 - 1.500 kg CO2e / kg** | EPA Waste Reduction Model (WARM) | Life-cycle savings from crude oil extraction, polymerization, blow-molding, and landfill diversion of PET and HDPE. |
        | **Plant-Forward Diet** | **1.800 kg CO2e / meal** | Poore & Nemecek (Science 2018), Our World in Data | Replacing 100g of ruminant meat (beef/lamb) with plant legumes avoids ruminant enteric methane, feed transport, and land-use change. |
        | **Food Waste Diversion** | **0.500 kg CO2e / kg** | Project Drawdown - Food Waste | Prevents anaerobic decomposition in compacted municipal landfills which converts organics into potent methane (CH4, GWP 28x). |
        | **Tree Carbon Sink** | **21.77 kg CO2 / year** | US EPA GHG Equivalencies Calculator | Carbon sequestered annually by one tree seedling planted and grown for 10 years in an urban or temperate setting. |
        """)

        st.markdown("</div>", unsafe_allow_html=True)
