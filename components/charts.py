"""
EcoTrack - Interactive Plotly Visualization Components
Generates responsive, publication-ready Plotly charts styled to match
the Forest Green & Emerald SaaS theme.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta

# Modern Palette
CHART_COLORS = [
    "#10B981", # Emerald
    "#059669", # Forest Green
    "#0284C7", # Ocean Blue
    "#F59E0B", # Amber
    "#8B5CF6", # Violet
    "#14B8A6", # Teal
    "#EC4899"  # Pink
]

LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#1E293B"),
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_family="Plus Jakarta Sans")
)

def create_category_donut(df, metric="activities"):
    """
    Renders a sleek Plotly donut chart showing category distribution.
    metric can be 'activities' (counts) or 'co2_kg' (impact sum).
    """
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No activity data logged yet", showarrow=False, font=dict(size=14, color="#94A3B8"))
        fig.update_layout(**LAYOUT_DEFAULTS, height=280)
        return fig

    if metric == "activities":
        cat_data = df["category"].value_counts().reset_index()
        cat_data.columns = ["Category", "Count"]
        values_col = "Count"
        title = "Activity Distribution by Category"
    else:
        cat_data = df.groupby("category")["co2_kg"].sum().reset_index()
        cat_data.columns = ["Category", "CO2_kg"]
        values_col = "CO2_kg"
        title = "CO2 Avoided by Category (kg)"

    fig = px.pie(
        cat_data,
        names="Category",
        values=values_col,
        hole=0.62,
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Value: %{value}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=11)),
        height=320,
        title=dict(text=title, font=dict(size=14, color="#0F172A", weight=700))
    )
    return fig

def create_daily_activity_trend(df, days=14):
    """
    Renders a bar chart of daily activity counts over the last N days.
    """
    today = date.today()
    all_dates = [today - timedelta(days=i) for i in range(days - 1, -1, -1)]
    date_strs = [d.isoformat() for d in all_dates]
    counts_map = {d: 0 for d in date_strs}

    if df is not None and not df.empty and "date" in df.columns:
        for d, count in df["date"].value_counts().items():
            if str(d) in counts_map:
                counts_map[str(d)] = count

    trend_df = pd.DataFrame({
        "Date": [d[5:] for d in date_strs], # MM-DD
        "FullDate": date_strs,
        "Activities": [counts_map[d] for d in date_strs]
    })

    fig = px.bar(
        trend_df,
        x="Date",
        y="Activities",
        text="Activities",
        color_discrete_sequence=["#10B981"]
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=11,
        marker_line_color="#059669",
        marker_line_width=1,
        marker=dict(cornerradius=6)
    )
    fig.update_layout(
        **LAYOUT_DEFAULTS,
        xaxis=dict(showgrid=False, linecolor="#CBD5E1", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=11), title="Activities Completed"),
        height=300,
        title=dict(text=f"Daily Activity Cadence (Last {days} Days)", font=dict(size=14, color="#0F172A", weight=700))
    )
    return fig

def create_cumulative_impact_chart(df):
    """
    Renders a dual-axis area/line chart showing cumulative CO2 avoided and Water saved over time.
    """
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No impact data recorded yet", showarrow=False, font=dict(size=14, color="#94A3B8"))
        fig.update_layout(**LAYOUT_DEFAULTS, height=320)
        return fig

    # Aggregate by date ascending
    daily_sums = df.groupby("date").agg({
        "co2_kg": "sum",
        "water_l": "sum",
        "waste_kg": "sum",
        "energy_kwh": "sum"
    }).reset_index().sort_values("date")

    daily_sums["cum_co2"] = daily_sums["co2_kg"].cumsum()
    daily_sums["cum_water"] = daily_sums["water_l"].cumsum()

    fig = go.Figure()

    # Cumulative CO2 Area
    fig.add_trace(go.Scatter(
        x=daily_sums["date"],
        y=daily_sums["cum_co2"],
        name="Cumulative CO2 Avoided (kg)",
        mode="lines+markers",
        line=dict(color="#10B981", width=3),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.12)",
        hovertemplate="<b>%{x}</b><br>Cumulative CO2: %{y:.1f} kg<extra></extra>"
    ))

    # Water Line (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=daily_sums["date"],
        y=daily_sums["cum_water"],
        name="Cumulative Water Saved (L)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#0284C7", width=2.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Cumulative Water: %{y:.0f} L<extra></extra>"
    ))

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        xaxis=dict(showgrid=False, linecolor="#CBD5E1", tickfont=dict(size=11)),
        yaxis=dict(
            title=dict(text="CO2 Avoided (kg)", font=dict(color="#10B981")),
            tickfont=dict(color="#10B981"),
            showgrid=True,
            gridcolor="#F1F5F9"
        ),
        yaxis2=dict(
            title=dict(text="Water Conserved (L)", font=dict(color="#0284C7")),
            tickfont=dict(color="#0284C7"),
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=340,
        title=dict(text="Cumulative Environmental Impact Growth", font=dict(size=14, color="#0F172A", weight=700))
    )
    return fig

def create_weekly_impact_breakdown(df):
    """
    Renders grouped weekly impact metrics for comparative review.
    """
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Log activities to view weekly breakdown", showarrow=False, font=dict(size=14, color="#94A3B8"))
        fig.update_layout(**LAYOUT_DEFAULTS, height=280)
        return fig

    df_copy = df.copy()
    df_copy["week"] = pd.to_datetime(df_copy["date"]).dt.to_period("W").astype(str)
    weekly = df_copy.groupby("week").agg({
        "co2_kg": "sum",
        "energy_kwh": "sum",
        "id": "count"
    }).reset_index().rename(columns={"id": "activities"})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=weekly["week"],
        y=weekly["co2_kg"],
        name="CO2 Avoided (kg)",
        marker_color="#10B981"
    ))
    fig.add_trace(go.Bar(
        x=weekly["week"],
        y=weekly["energy_kwh"],
        name="Energy Saved (kWh)",
        marker_color="#F59E0B"
    ))

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        barmode="group",
        xaxis=dict(showgrid=False, title="Week Period"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        height=320,
        title=dict(text="Weekly Carbon & Energy Conservation Trends", font=dict(size=14, color="#0F172A", weight=700))
    )
    return fig

def create_score_radar(breakdown):
    """
    Renders a clean polar radar chart illustrating user's balance across EcoScore dimensions.
    """
    categories = ["Consistency", "Impact", "Diversity", "Challenges"]
    max_values = [30.0, 35.0, 20.0, 15.0]

    # Normalized to 100% for balanced radar presentation
    scores = [
        (breakdown.get("consistency", 0) / 30.0) * 100,
        (breakdown.get("impact", 0) / 35.0) * 100,
        (breakdown.get("diversity", 0) / 20.0) * 100,
        (breakdown.get("challenges", 0) / 15.0) * 100,
    ]
    # Close the radar loop
    categories_closed = categories + [categories[0]]
    scores_closed = scores + [scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(16, 185, 129, 0.25)",
        line=dict(color="#10B981", width=2.5),
        name="User Mastery %"
    ))

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%", linecolor="#CBD5E1"),
            angularaxis=dict(linecolor="#CBD5E1")
        ),
        showlegend=False,
        height=280,
        margin=dict(l=30, r=30, t=30, b=30)
    )
    return fig
