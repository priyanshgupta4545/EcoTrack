"""
EcoTrack - Activity Tracker Page
Complete CRUD management for user eco-friendly activities with category filtering,
keyword search, dynamic impact recalculation, and CSV download.
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
from config import CATEGORIES, CATEGORY_ICONS, ACTIVITY_PRESETS, ACTIVITY_MAP
from calculations import calculate_activity_impact
import database

def render_activities_page(df, stats):
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0;">
            📝 Eco Activity Tracker
        </h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-top: 0.2rem;">
            Log your daily eco actions, monitor personal records, and manage your environmental diary.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_log, tab_view, tab_manage = st.tabs(["➕ Log New Activity", "📋 Activity Ledger & Filter", "✏️ Edit / Delete Records"])

    # -------------------------------------------------------------
    # TAB 1: LOG NEW ACTIVITY
    # -------------------------------------------------------------
    with tab_log:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.2rem; font-weight: 700; color: #065F46;">
                Log a Green Habit
            </h3>
            <p style="color: #64748B; font-size: 0.85rem;">
                Select from our calibrated activity presets or create a custom entry. Impacts are computed automatically based on scientific lifecycle models.
            </p>
        """, unsafe_allow_html=True)

        mode = st.radio("Activity Type", ["Calibrated Preset", "Custom Activity"], horizontal=True)

        with st.form("add_activity_form", clear_on_submit=False):
            if mode == "Calibrated Preset":
                preset_labels = [f"{p['icon']} {p['name']} ({p['category']})" for p in ACTIVITY_PRESETS]
                selected_label = st.selectbox("Select Habit Preset", preset_labels)
                sel_idx = preset_labels.index(selected_label)
                preset = ACTIVITY_PRESETS[sel_idx]

                col1, col2, col3 = st.columns(3)
                with col1:
                    act_date = st.date_input("Date of Action", value=date.today())
                with col2:
                    qty = st.number_input(f"Quantity ({preset['unit']})", min_value=0.1, max_value=1000.0, value=float(preset["default_qty"]), step=0.5)
                with col3:
                    st.text_input("Unit", value=preset["unit"], disabled=True)

                notes = st.text_input("Personal Notes or Reflections (Optional)", placeholder="e.g. Cycled with Alex along the greenway")

                # Preview live calculated impacts
                preview_impacts = calculate_activity_impact(preset["id"], qty)
                st.markdown(f"""
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; padding: 12px; margin: 12px 0;">
                    <span style="font-weight: 700; color: #065F46; font-size: 0.85rem;">Estimated Impact Preview:</span>
                    <div style="display: flex; gap: 20px; margin-top: 6px; font-size: 0.85rem;">
                        <span style="color: #065F46;"><b>-{preview_impacts['co2_kg']} kg</b> CO2e</span>
                        <span style="color: #0284C7;"><b>{preview_impacts['water_l']} L</b> Water Saved</span>
                        <span style="color: #B45309;"><b>{preview_impacts['waste_kg']} kg</b> Waste Diverted</span>
                        <span style="color: #D97706;"><b>{preview_impacts['energy_kwh']} kWh</b> Power Saved</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                submitted = st.form_submit_button("🌱 Record Activity", use_container_width=True)
                if submitted:
                    database.add_activity(
                        act_date=act_date.isoformat(),
                        activity_id=preset["id"],
                        name=preset["name"],
                        category=preset["category"],
                        quantity=qty,
                        unit=preset["unit"],
                        co2_kg=preview_impacts["co2_kg"],
                        water_l=preview_impacts["water_l"],
                        waste_kg=preview_impacts["waste_kg"],
                        energy_kwh=preview_impacts["energy_kwh"],
                        notes=notes
                    )
                    database.sync_badges(stats)
                    st.success(f"Successfully logged '{preset['name']}'! Your environmental diary has been updated.")
                    st.rerun()

            else: # Custom Activity
                col1, col2 = st.columns(2)
                with col1:
                    custom_name = st.text_input("Activity Name", placeholder="e.g. Swapped halogen for OLED strip")
                    custom_cat = st.selectbox("Category", CATEGORIES)
                with col2:
                    act_date = st.date_input("Date", value=date.today(), key="custom_date")
                    custom_unit = st.text_input("Unit of Measure", placeholder="e.g. hours, items, km")

                col3, col4, col5, col6 = st.columns(4)
                with col3:
                    custom_qty = st.number_input("Quantity", min_value=0.1, value=1.0, step=0.5)
                with col4:
                    custom_co2 = st.number_input("CO2 Avoided (kg)", min_value=0.0, value=0.5, step=0.1)
                with col5:
                    custom_water = st.number_input("Water Conserved (L)", min_value=0.0, value=0.0, step=5.0)
                with col6:
                    custom_energy = st.number_input("Energy Saved (kWh)", min_value=0.0, value=0.2, step=0.1)

                custom_notes = st.text_input("Notes", placeholder="Details about this custom environmental step")
                submitted = st.form_submit_button("🌱 Save Custom Activity", use_container_width=True)

                if submitted:
                    if not custom_name.strip():
                        st.error("Please provide an activity name.")
                    else:
                        database.add_activity(
                            act_date=act_date.isoformat(),
                            activity_id="custom",
                            name=custom_name.strip(),
                            category=custom_cat,
                            quantity=custom_qty,
                            unit=custom_unit or "units",
                            co2_kg=custom_co2,
                            water_l=custom_water,
                            waste_kg=0.0,
                            energy_kwh=custom_energy,
                            notes=custom_notes
                        )
                        database.sync_badges(stats)
                        st.success(f"Custom activity '{custom_name}' recorded!")
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: ACTIVITY LEDGER & FILTER
    # -------------------------------------------------------------
    with tab_view:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.2rem; font-weight: 700; color: #0F172A;">
                Search & Filter Activity Records
            </h3>
        """, unsafe_allow_html=True)

        f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 2])
        with f_col1:
            cat_filter = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
        with f_col2:
            search_query = st.text_input("Search (keyword in name/notes)", placeholder="e.g. cycle, shower")
        with f_col3:
            d_range = st.date_input("Date Range", value=(date.today() - pd.Timedelta(days=30), date.today()))

        st.markdown("</div>", unsafe_allow_html=True)

        start_d = d_range[0].isoformat() if isinstance(d_range, tuple) and len(d_range) > 0 else None
        end_d = d_range[1].isoformat() if isinstance(d_range, tuple) and len(d_range) > 1 else None

        filtered_df = database.get_activities(
            start_date=start_d,
            end_date=end_d,
            category=cat_filter,
            search=search_query
        )

        if not filtered_df.empty:
            # Summary Metrics for filtered view
            f_acts = len(filtered_df)
            f_co2 = filtered_df["co2_kg"].sum()
            f_water = filtered_df["water_l"].sum()
            f_energy = filtered_df["energy_kwh"].sum()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Filtered Activities", f"{f_acts}")
            m2.metric("Filtered CO2 Avoided", f"{f_co2:.2f} kg")
            m3.metric("Filtered Water Saved", f"{f_water:,.0f} L")
            m4.metric("Filtered Power Saved", f"{f_energy:.2f} kWh")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Clean Display Table
            display_cols = ["id", "date", "name", "category", "quantity", "unit", "co2_kg", "water_l", "energy_kwh", "notes"]
            clean_df = filtered_df[display_cols].copy()
            clean_df.columns = ["ID", "Date", "Activity Name", "Category", "Qty", "Unit", "CO2 (kg)", "Water (L)", "Power (kWh)", "Notes"]

            st.dataframe(clean_df, use_container_width=True, hide_index=True)

            # Export Button
            csv_data = clean_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Ledger as CSV",
                data=csv_data,
                file_name=f"ecotrack_activities_{date.today().isoformat()}.csv",
                mime="text/csv",
                help="Download your filtered activity history for spreadsheet analysis"
            )
        else:
            st.info("No activities match your current search and filter criteria.")

    # -------------------------------------------------------------
    # TAB 3: EDIT / DELETE
    # -------------------------------------------------------------
    with tab_manage:
        st.markdown("""
        <div class="content-card">
            <h3 style="margin-top: 0; font-size: 1.2rem; font-weight: 700; color: #0F172A;">
                Edit or Remove an Existing Record
            </h3>
            <p style="color: #64748B; font-size: 0.85rem;">
                Select an activity ID to modify its values or delete the entry from your database.
            </p>
        """, unsafe_allow_html=True)

        if df is not None and not df.empty:
            activity_options = {f"#{r['id']} | {r['date']} - {r['name']} ({r['quantity']} {r['unit']})": r["id"] for _, r in df.iterrows()}
            chosen_label = st.selectbox("Select Activity to Manage", list(activity_options.keys()))
            target_id = activity_options[chosen_label]

            act_row = database.get_activity_by_id(target_id)
            if act_row:
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    e_date = st.date_input("Date", value=datetime.strptime(act_row["date"], "%Y-%m-%d").date(), key=f"e_date_{target_id}")
                    e_name = st.text_input("Name", value=act_row["name"], key=f"e_name_{target_id}")
                    e_cat = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(act_row["category"]) if act_row["category"] in CATEGORIES else 0, key=f"e_cat_{target_id}")
                with e_col2:
                    e_qty = st.number_input("Quantity", value=float(act_row["quantity"]), min_value=0.1, step=0.5, key=f"e_qty_{target_id}")
                    e_unit = st.text_input("Unit", value=act_row["unit"], key=f"e_unit_{target_id}")
                    e_notes = st.text_input("Notes", value=act_row["notes"], key=f"e_notes_{target_id}")

                e_sub1, e_sub2, e_sub3 = st.columns(3)
                with e_sub1:
                    e_co2 = st.number_input("CO2 (kg)", value=float(act_row["co2_kg"]), min_value=0.0, step=0.1, key=f"e_co2_{target_id}")
                with e_sub2:
                    e_water = st.number_input("Water (L)", value=float(act_row["water_l"]), min_value=0.0, step=1.0, key=f"e_water_{target_id}")
                with e_sub3:
                    e_energy = st.number_input("Power (kWh)", value=float(act_row["energy_kwh"]), min_value=0.0, step=0.1, key=f"e_energy_{target_id}")

                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button("💾 Update Activity", use_container_width=True, key=f"update_btn_{target_id}"):
                        database.update_activity(
                            pk_id=target_id,
                            act_date=e_date.isoformat(),
                            name=e_name,
                            category=e_cat,
                            quantity=e_qty,
                            unit=e_unit,
                            co2_kg=e_co2,
                            water_l=e_water,
                            waste_kg=act_row.get("waste_kg", 0.0),
                            energy_kwh=e_energy,
                            notes=e_notes
                        )
                        st.success(f"Activity #{target_id} updated successfully!")
                        st.rerun()

                with btn_col2:
                    if st.button("🗑️ Delete Activity", use_container_width=True, key=f"del_btn_{target_id}", type="secondary"):
                        database.delete_activity(target_id)
                        st.warning(f"Activity #{target_id} has been permanently deleted.")
                        st.rerun()

        else:
            st.info("No activities available to edit or delete.")

        st.markdown("</div>", unsafe_allow_html=True)
