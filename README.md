# EcoTrack – Smart Sustainability & Environmental Impact Tracker 🌱

[![Python](https://img.shields.io/badge/Python-3.10%2B-10B981?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-059669?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-0284C7?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Persistent_DB-7C3AED?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

> **EcoTrack** is a modern, full-stack sustainability web application designed to help individuals monitor their daily eco-friendly activities, quantify verified greenhouse gas (GHG) reductions and resource conservation, participate in community challenges, and develop lasting sustainable habits.

---

## 📖 Table of Contents
1. [Project Overview & Vision](#-project-overview--vision)
2. [Problem Statement](#-problem-statement)
3. [The EcoTrack Solution](#-the-ecotrack-solution)
4. [Key Features](#-key-features)
5. [Scientific Assumptions & Methodology](#-scientific-assumptions--methodology)
6. [Technology Stack](#-technology-stack)
7. [System Architecture](#-system-architecture)
8. [Installation & Setup](#-installation--setup)
9. [Running the Application](#-running-the-application)
10. [Application Walkthrough](#-application-walkthrough)
11. [Future Roadmap](#-future-roadmap)
12. [Contributing & License](#-contributing--license)

---

## 🌍 Project Overview & Vision

Environmental awareness is often hindered by **intangibility**: people turn off light switches, choose plant-based meals, or commute by bicycle without knowing whether their individual actions make a measurable difference.

**EcoTrack** closes this feedback loop by transforming daily micro-habits into clear, tangible environmental metrics:
- **Carbon Dioxide Equivalent ($CO_2e$) Avoided** (in kilograms)
- **Potable Water Conserved** (in Liters)
- **Landfill Waste Diverted** (in kilograms and single-use items)
- **Electrical Energy Saved** (in kilowatt-hours)
- **Equivalencies**: Urban tree-years of carbon absorption, automobile kilometers avoided, and bathtubs of water conserved.

Built with the polish of a venture-backed SaaS platform, EcoTrack combines real-time data persistence, interactive Plotly visualizations, behavioral gamification, and an evidence-backed recycling decision manual.

---

## ⚠️ Problem Statement

1. **The Intangibility Gap**: Individuals want to live more sustainably but lack feedback on the actual impact of choosing a train over a car, or cutting shower times in half.
2. **Wishcycling & Recycling Confusion**: Over 25% of municipal recycling is contaminated because consumers are unsure how to properly sort items like greasy pizza boxes, coffee cups, or plastic films.
3. **Lack of Habit Continuity**: Sustainability efforts often fade after a few days without milestone tracking, streaks, and gamified reinforcement.
4. **Data Opacity**: Many carbon calculators use black-box numbers without disclosing conversion factors or scientific limitations.

---

## 💡 The EcoTrack Solution

EcoTrack provides an end-to-end habit tracking and impact calculation platform:
- **1-Click Quick Logging**: Record daily actions in seconds with calibrated presets or custom entries.
- **Multi-Factor EcoScore (0–100)**: A holistic sustainability index evaluating habit consistency, total environmental impact, category diversity, and challenge completions.
- **Interactive Lifestyle Simulator**: What-if scenario modeler demonstrating how weekly micro-habits compound into annual tons of $CO_2$ avoided.
- **Interactive Recycling Decision Engine**: Searchable directory answering *"Can I recycle this?"* with preparation steps and green alternatives.
- **Simulated Community Benchmarks**: Friendly peer comparisons against demo cohorts for educational benchmarking.

---

## ✨ Key Features

### 1. 🏠 Interactive Command Center (Home Dashboard)
- **SaaS Metric Cards**: Displays total actions, $CO_2e$ avoided, water conserved, and waste diverted with period-over-period percentage velocity ($\Delta\%$).
- **Tangible Equivalencies**: Converts metric units into intuitive equivalents (tree-years of absorption, car kilometers cancelled, bathtubs of water, and phone recharges).
- **Embedded Quick-Logger**: Record actions with 1 click directly from the dashboard.
- **Cadence & Distribution Charts**: Real-time Plotly charts tracking 14-day activity streaks and category balances.
- **EcoCampus Benchmark**: Friendly peer ranking against clearly labeled simulated benchmark profiles.

### 2. 📝 Full-Featured Eco Activity Tracker
- **Pre-Calibrated Library**: Presets across Transportation, Energy, Water, Waste & Recycling, Sustainable Food, and Eco Lifestyle.
- **Custom Activity Creator**: Log unique community initiatives with user-defined emission factors.
- **Full CRUD Management**: View, filter by category or date range, search by keyword, edit past entries, or delete records.
- **CSV Data Export**: Instant download of your complete activity ledger.

### 3. 🧮 Environmental Impact Calculator & Simulator
- **Interactive Sliders**: Simulate weekly changes (e.g. $+20\text{ km}$ green transit, $4\text{ min}$ shorter showers, $4$ plant-based meals).
- **Dynamic Annual Projections**: Real-time mathematical compounding of annual resource savings.
- **Transparent Open Math**: Step-by-step formulas linking directly to official sources (EPA, DEFRA, IEA).

### 4. 🎯 Eco Challenges & Sprints
- **Structured Sprints**: Plastic-Free Week, H2O Conservation Sprint, Pedal & Stride Commuter, Power Down Protocol, and Zero Waste Warrior.
- **Milestone Progress Tracking**: Log increments toward sprint targets with dynamic progress bars.
- **Point Rewards**: Earn points upon completion that directly boost your EcoScore.

### 5. 🏆 Achievements & Badges System
- **Tiered Badge Showcase**: Bronze, Silver, Gold, and Platinum badges (Green Beginner, Plastic Warrior, Aqua Protector, Carbon Conscious, Habit Builder, and Eco Champion).
- **Dynamic Unlock Criteria**: Badges verify actual database statistics and unlock automatically.
- **Personal Monthly Goals**: Create and track customized monthly reduction targets.

### 6. 💡 Daily Tips & Practical Recycling Guide
- **Rotating Daily Insight**: Deterministic daily tip selected based on the day of the year.
- **"Can I Recycle This?" Search Engine**: Instant lookup for items like pizza boxes, soft plastic films, aluminum cans, styrofoam, and lithium batteries.
- **Preparation & Contamination Rules**: Clear instructions on rinsing, separating lids, and avoiding wishcycling.

### 7. 📊 Reports & Advanced Analytics
- **Cumulative Carbon Curve**: Visualizes cumulative greenhouse gas avoidance over time.
- **Weekly Energy Trends**: Grouped comparisons of electricity conserved vs carbon mitigated.
- **Balance Radar**: Multi-axis radar chart showing user strengths across Consistency, Impact, Diversity, and Challenges.
- **Dual Export**: Download data in clean CSV or structured JSON.

---

## 🔬 Scientific Assumptions & Methodology

All calculations in EcoTrack are calibrated against published empirical research and government lifecycle assessments:

| Category | Empirical Factor | Primary Scientific Reference |
| :--- | :--- | :--- |
| **Green Commute** | $0.170\text{ kg } CO_2e\text{ / km}$ | US EPA Greenhouse Gas Equivalencies & UK DEFRA (petrol passenger vehicle average) |
| **Public Transit Shift** | $0.100\text{ kg } CO_2e\text{ / km}$ | Federal Transit Administration (FTA) net modal shift factor |
| **Shower Water** | $9.0\text{ Liters / min}$ | US EPA WaterSense standard residential showerhead flow rates |
| **Water Heating Energy**| $0.003\text{ kg } CO_2e\text{ / L}$ | Lawrence Berkeley National Laboratory domestic water heating energy profile |
| **Grid Electricity** | $0.400\text{ kg } CO_2e\text{ / kWh}$ | US EPA eGRID subregion average & International Energy Agency (IEA) |
| **Plastic Diversion** | $1.400 - 1.500\text{ kg } CO_2e\text{ / kg}$ | US EPA Waste Reduction Model (WARM) life-cycle analysis |
| **Plant-Based Meal** | $1.800\text{ kg } CO_2e\text{ & } 1,200\text{ L water}$ | Poore & Nemecek (*Science*, 2018); Our World in Data |
| **Tree Absorption** | $21.77\text{ kg } CO_2\text{ / year}$ | US EPA estimate for one urban tree seedling grown for 10 years |

*Note: All values are calibrated estimates designed for personal habit coaching and educational awareness, not ISO 14064 certified corporate greenhouse gas inventories.*

---

## 🛠️ Technology Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core application logic, math, and database operations |
| **Framework** | Streamlit 1.35+ | Reactive, full-featured web UI framework |
| **Data Processing** | Pandas | Tabular data analysis, time-series aggregation, and filtering |
| **Visualizations** | Plotly Express & Graph Objects | Publication-grade interactive charts and radar diagrams |
| **Data Storage** | SQLite 3 | Relational database with persistent ACID storage |
| **Design / Styling** | Custom Modern CSS | Forest green and emerald palette, glassmorphism cards, responsive layouts |
| **Version Control** | Git & GitHub | Modular codebase, automated demo seeding, and documentation |

---

## 🏗️ System Architecture

```
EcoTrack/
├── app.py                  # Main Streamlit application entry point & router
├── requirements.txt        # Python package dependencies
├── config.py               # Constants, theme colors, presets, tips, and factors
├── database.py             # SQLite persistence layer (CRUD, badges, challenges, goals)
├── calculations.py         # Environmental impact engine, EcoScore, streaks & trends
├── assets/
│   └── style.css           # Modern SaaS stylesheet (emerald/forest theme, cards, typography)
├── components/
│   ├── __init__.py
│   ├── cards.py            # Reusable HTML KPI cards, badge cards, and tip boxes
│   ├── charts.py           # Reusable Plotly charts (donut, trend, area, radar)
│   ├── dashboard.py        # Home dashboard layout, quick logger, and community board
│   └── sidebar.py          # Branded sidebar, navigation radio, and demo reset controls
├── pages/
│   ├── __init__.py
│   ├── activities.py       # Activity Tracker: logging, ledger, search, edit, delete
│   ├── impact.py           # What-if lifestyle simulator & scientific methodology
│   ├── challenges.py       # Eco challenges catalogue, milestone tracker & sprints
│   ├── achievements.py     # Badges showcase & personal monthly goals
│   ├── tips.py             # Rotating daily tips & interactive recycling directory
│   └── reports.py          # Analytics dashboard, period comparisons, CSV/JSON export
├── data/
│   └── ecotrack.db         # Persistent SQLite database file (auto-generated)
└── screenshots/
    └── README.md           # Visual UI screenshots guide
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your system.
- Git installed.

### Step-by-Step Installation

1. **Clone or Download the Repository:**
   ```bash
   git clone https://github.com/your-username/EcoTrack.git
   cd EcoTrack
   ```

2. **Create and Activate a Virtual Environment:**
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows:**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Running the Application

Launch the Streamlit web application:

```bash
streamlit run app.py
```

Streamlit will start a local development server and automatically open the application in your default web browser at:
```
http://localhost:8501
```

*Note: On initial launch, EcoTrack automatically initializes the SQLite database and seeds 30 days of realistic demo records so that charts and analytics are immediately visible.*

---

## 🧭 Application Walkthrough

### 1. Resetting or Clearing Data
- In the left sidebar, click **"🔄 Reset Demo"** at any time to restore the curated 30-day sample history.
- Click **"🗑️ Clear All"** if you wish to start from a blank ledger.

### 2. Quick-Logging an Activity
- On the **Home Dashboard**, navigate to the **"⚡ Quick Log Eco Activity"** widget.
- Select an activity preset (e.g. *"Walked or Cycled instead of Driving"*), input the distance or quantity, and click **"Log Action"**.
- Your EcoScore, avoided $CO_2$, and streak counters will update immediately.

### 3. Joining a Challenge
- Navigate to **"🎯 Eco Challenges"** in the sidebar.
- Click the **"Browse & Join Challenges"** tab.
- Choose a sprint (e.g., *"H2O Conservation Sprint"*) and click **"Join Challenge"**.
- Log milestone increments in the **"Active Challenges"** tab as you complete daily actions.

### 4. Looking Up Recycling Rules
- Navigate to **"💡 Daily Tips & Recycling"**.
- Open the **"Practical Recycling Directory"** tab.
- Type any household packaging (e.g., *"pizza"*, *"styrofoam"*, or *"coffee cup"*) to view preparation instructions and contamination risks.

---

## 🗺️ Future Roadmap

- [ ] **Smart Receipt & Barcode Scanner**: Upload grocery receipts or scan barcodes to automatically categorize packaging materials.
- [ ] **IoT Smart Plug Integration**: Ingest real-time power readings from smart home meters (Shelly / Tuya).
- [ ] **Multi-User Community Hub**: Real-time peer leaderboards with secure federated authentication.
- [ ] **Offline PWA Support**: Progressive Web App packaging for native offline mobile experience.

---

## 🤝 Contributing & License

Contributions are welcome! If you have suggestions or improvements:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewEcoFeature`).
3. Commit your changes (`git commit -m 'Add new eco-friendly activity preset'`).
4. Push to the branch (`git push origin feature/NewEcoFeature`).
5. Open a Pull Request.

This project is licensed under the **MIT License**.
