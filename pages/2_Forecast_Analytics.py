import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from forecast.predictor import build_forecast_report
from ui.theme import apply_theme


# =========================================================
# THERMOSAFE — FORECAST & ANALYTICS
# =========================================================

st.html(apply_theme())


# =========================================================
# PAGE HEADER
# =========================================================

st.html(
    """
    <div class="thermosafe-header">
        <div>
            <div class="section-title">
                Forecast &amp; Analytics
            </div>

            <div class="analytics-section-subtitle">
                Thermal-risk trends, forecast intelligence, and early-warning analysis.
            </div>
        </div>
    </div>
    """
)


# =========================================================
# SHARED DATA
# =========================================================

dashboard_data = st.session_state.get(
    "dashboard_data",
    None
)


# =========================================================
# SAFETY CHECK
# =========================================================

if dashboard_data is None:
    st.warning(
        "No environmental data available yet. "
        "Return to the Command Center and click "
        "'Analyze Conditions' first."
    )
    st.stop()


# =========================================================
# CURRENT CONDITIONS
# =========================================================

current_risk = float(
    dashboard_data.get("risk_score", 0)
)

current_level = dashboard_data.get(
    "risk_level",
    "UNKNOWN"
)

temperature = float(
    dashboard_data.get("temperature", 0)
)

humidity = float(
    dashboard_data.get("humidity", 0)
)

wind_speed = float(
    dashboard_data.get("wind_speed", 0)
)

heat_index = float(
    dashboard_data.get("heat_index", temperature)
)

location = dashboard_data.get(
    "location",
    "Unknown location"
)


# =========================================================
# LOCATION CONTEXT
# =========================================================

st.html(
    f"""
    <div class="location-badge">
        <span>{location}</span>
        <span>•</span>
        <span>LIVE ENVIRONMENT</span>
    </div>
    """
)


# =========================================================
# CURRENT RISK OVERVIEW
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Current Risk Overview
    </div>

    <div class="analytics-section-subtitle">
        Live environmental conditions feeding the thermal-risk engine.
    </div>
    """
)

overview = [
    ("CURRENT RISK", f"{current_risk:.0f}/100"),
    ("RISK LEVEL", current_level),
    ("TEMPERATURE", f"{temperature:.1f} °C"),
    ("HUMIDITY", f"{humidity:.0f}%"),
]

cols = st.columns(4)

for col, (label, value) in zip(cols, overview):
    with col:
        st.html(
            f"""
            <div class="analytics-metric">
                <div class="analytics-label">
                    {label}
                </div>

                <div class="analytics-value">
                    {value}
                </div>
            </div>
            """
        )


# =========================================================
# BUILD 5-DAY FORECAST
# =========================================================

forecast_report = build_forecast_report(
    current_temperature=temperature,
    current_humidity=humidity,
    current_wind=wind_speed,
    days=5,
)

st.session_state["forecast_report"] = forecast_report


# =========================================================
# EXTRACT FORECAST DATA
# =========================================================

forecast_data = []

if forecast_report:

    possible_forecast = forecast_report.get(
        "forecast",
        forecast_report
    )

    if isinstance(possible_forecast, list):
        forecast_data = possible_forecast[:5]


# =========================================================
# 5-DAY FORECAST INTELLIGENCE
# =========================================================

st.html(
    """
    <div class="analytics-section">
        5-Day Forecast Intelligence
    </div>

    <div class="analytics-section-subtitle">
        Projected thermal conditions and early-warning indicators.
    </div>
    """
)


if forecast_data:

    risks = []
    temperatures = []

    for day in forecast_data:

        day_temperature = float(
            day.get(
                "temperature",
                temperature
            )
        )

        day_risk = float(
            day.get(
                "risk_score",
                current_risk
            )
        )

        temperatures.append(day_temperature)
        risks.append(day_risk)


    # -----------------------------------------------------
    # FORECAST SUMMARY
    # -----------------------------------------------------

    average_risk = (
        sum(risks) / len(risks)
        if risks
        else current_risk
    )

    peak_risk = (
        max(risks)
        if risks
        else current_risk
    )

    high_days = sum(
        1
        for risk in risks
        if risk >= 50
    )

    extreme_days = sum(
        1
        for risk in risks
        if risk >= 75
    )

    heatwave_detected = (
        high_days >= 2
        or extreme_days >= 1
    )


    summary = [
        (
            "5-DAY AVERAGE",
            f"{average_risk:.1f}/100"
        ),
        (
            "PEAK RISK",
            f"{peak_risk:.0f}/100"
        ),
        (
            "HIGH / EXTREME DAYS",
            str(high_days)
        ),
        (
            "HEATWAVE",
            "DETECTED"
            if heatwave_detected
            else "NOT DETECTED"
        ),
    ]

    summary_cols = st.columns(4)

    for col, (label, value) in zip(
        summary_cols,
        summary
    ):
        with col:
            st.html(
                f"""
                <div class="analytics-metric">
                    <div class="analytics-label">
                        {label}
                    </div>

                    <div class="analytics-value">
                        {value}
                    </div>
                </div>
                """
            )


    # =====================================================
    # THERMAL RISK TREND
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Thermal Risk Trend
        </div>

        <div class="analytics-section-subtitle">
            Five-day projection of human thermal stress.
        </div>
        """
    )

    risk_chart = pd.DataFrame(
        {
            "Day": [
                f"Day {index + 1}"
                for index in range(len(risks))
            ],
            "Risk": risks,
        }
    )


    fig_risk = go.Figure()

    fig_risk.add_trace(
        go.Scatter(
            x=risk_chart["Day"],
            y=risk_chart["Risk"],
            mode="lines+markers",
            line=dict(
                color="#38bdf8",
                width=3
            ),
            marker=dict(
                color="#38bdf8",
                size=7
            ),
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Risk Score: %{y:.0f}/100"
                "<extra></extra>"
            ),
        )
    )

    fig_risk.update_layout(
        height=350,
        margin=dict(
            l=50,
            r=20,
            t=20,
            b=35,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#cbd5e1",
            family="Inter, sans-serif"
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            tickfont=dict(
                color="#94a3b8",
                size=11
            ),
        ),
        yaxis=dict(
            title="Risk Score",
            range=[0, 100],
            gridcolor="rgba(148,163,184,0.12)",
            zeroline=False,
            tickfont=dict(
                color="#94a3b8",
                size=11
            ),
            title_font=dict(
                color="#94a3b8",
                size=11
            ),
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            bordercolor="#38bdf8",
            font=dict(
                color="#f8fafc"
            )
        ),
        showlegend=False,
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


    # =====================================================
    # TEMPERATURE TREND
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Temperature Trend
        </div>

        <div class="analytics-section-subtitle">
            Forecast temperature trajectory across the analysis window.
        </div>
        """
    )

    temperature_chart = pd.DataFrame(
        {
            "Day": [
                f"Day {index + 1}"
                for index in range(len(temperatures))
            ],
            "Temperature": temperatures,
        }
    )


    fig_temperature = go.Figure()

    fig_temperature.add_trace(
        go.Scatter(
            x=temperature_chart["Day"],
            y=temperature_chart["Temperature"],
            mode="lines+markers",
            line=dict(
                color="#60a5fa",
                width=3
            ),
            marker=dict(
                color="#60a5fa",
                size=7
            ),
            hovertemplate=(
                "<b>%{x}</b>"
                "<br>Temperature: %{y:.1f} °C"
                "<extra></extra>"
            ),
        )
    )

    # Give the chart a little breathing room
    # so a flat forecast line remains readable.
    min_temperature = min(temperatures)
    max_temperature = max(temperatures)

    if min_temperature == max_temperature:
        temperature_padding = 2
    else:
        temperature_padding = max(
            1,
            (max_temperature - min_temperature) * 0.25
        )

    fig_temperature.update_layout(
        height=330,
        margin=dict(
            l=55,
            r=20,
            t=20,
            b=35,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#cbd5e1",
            family="Inter, sans-serif"
        ),
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            tickfont=dict(
                color="#94a3b8",
                size=11
            ),
        ),
        yaxis=dict(
            title="Temperature (°C)",
            range=[
                min_temperature - temperature_padding,
                max_temperature + temperature_padding
            ],
            gridcolor="rgba(148,163,184,0.12)",
            zeroline=False,
            tickfont=dict(
                color="#94a3b8",
                size=11
            ),
            title_font=dict(
                color="#94a3b8",
                size=11
            ),
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            bordercolor="#60a5fa",
            font=dict(
                color="#f8fafc"
            )
        ),
        showlegend=False,
    )

    st.plotly_chart(
        fig_temperature,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


    # =====================================================
    # 5-DAY THERMAL OUTLOOK
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            5-Day Thermal Outlook
        </div>

        <div class="analytics-section-subtitle">
            Day-by-day thermal risk projection.
        </div>
        """
    )


    forecast_cols = st.columns(
        len(forecast_data)
    )


    for index, (col, day) in enumerate(
        zip(
            forecast_cols,
            forecast_data
        )
    ):

        day_temperature = float(
            day.get(
                "temperature",
                temperature
            )
        )

        day_risk = float(
            day.get(
                "risk_score",
                current_risk
            )
        )

        day_level = day.get(
            "risk_level",
            "UNKNOWN"
        )


        level_key = str(
            day_level
        ).strip().lower()


        if level_key == "low":
            level_class = "analytics-low"
            fill_color = "#4ade80"

        elif level_key == "moderate":
            level_class = "analytics-moderate"
            fill_color = "#facc15"

        elif level_key == "high":
            level_class = "analytics-high"
            fill_color = "#fb923c"

        else:
            level_class = "analytics-extreme"
            fill_color = "#f87171"


        risk_width = max(
            3,
            min(
                100,
                day_risk
            )
        )


        with col:
            st.html(
                f"""
                <div class="analytics-forecast-card">

                    <div class="analytics-day">
                        DAY {index + 1}
                    </div>

                    <div class="analytics-temp">
                        {day_temperature:.1f} °C
                    </div>

                    <div class="analytics-risk">
                        Thermal risk {day_risk:.0f}/100
                    </div>

                    <div class="analytics-risk-bar">
                        <div
                            class="analytics-risk-fill"
                            style="
                                width: {risk_width}%;
                                background: {fill_color};
                            "
                        ></div>
                    </div>

                    <div class="
                        analytics-risk-level
                        {level_class}
                    ">
                        {str(day_level).upper()}
                    </div>

                </div>
                """
            )


else:

    st.info(
        "Forecast data is currently unavailable. "
        "Run an environmental analysis from the Command Center."
    )


# =========================================================
# HEATWAVE INTELLIGENCE
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Heatwave Intelligence
    </div>

    <div class="analytics-section-subtitle">
        Early-warning interpretation of the forecast.
    </div>
    """
)


if forecast_data:

    if extreme_days >= 1:

        insight_class = "critical"
        insight_label = "CRITICAL WARNING"
        insight_title = "Extreme thermal stress detected"
        insight_text = (
            "The forecast contains an extreme-risk period. "
            "Prolonged outdoor exposure should be minimized, "
            "with priority given to cooling, hydration, and "
            "protection of vulnerable populations."
        )

    elif high_days >= 2:

        insight_class = "danger"
        insight_label = "EARLY WARNING"
        insight_title = "Sustained thermal stress expected"
        insight_text = (
            "Multiple forecast days reach elevated thermal-risk "
            "levels. Plan cooling breaks, maintain hydration, "
            "and reduce unnecessary prolonged heat exposure."
        )

    elif peak_risk >= 30:

        insight_class = "warning"
        insight_label = "WATCH"
        insight_title = "Thermal conditions may become elevated"
        insight_text = (
            "The forecast shows periods of increasing thermal "
            "stress. Conditions remain manageable, but prolonged "
            "exposure may become more demanding."
        )

    else:

        insight_class = "safe"
        insight_label = "EARLY WARNING"
        insight_title = "No significant thermal escalation"
        insight_text = (
            "The forecast does not indicate significant "
            "thermal-risk escalation over the next five days. "
            "Normal activity and hydration can generally continue."
        )


    st.html(
        f"""
        <div class="
            analytics-insight
            {insight_class}
        ">

            <div class="analytics-insight-label">
                {insight_label}
            </div>

            <div class="analytics-insight-title">
                {insight_title}
            </div>

            <div class="analytics-insight-text">
                {insight_text}
            </div>

        </div>
        """
    )


# =========================================================
# RECOMMENDED RESPONSE
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Recommended Response
    </div>

    <div class="analytics-section-subtitle">
        Response guidance based on the current thermal-risk state.
    </div>
    """
)


if current_risk >= 75:

    response_class = "critical"
    response_label = "CURRENT RESPONSE"
    response_title = "Immediate heat protection required"
    response_text = (
        "Avoid prolonged outdoor exposure. Prioritize cooling, "
        "hydration, and protection of vulnerable populations."
    )

elif current_risk >= 50:

    response_class = "danger"
    response_label = "CURRENT RESPONSE"
    response_title = "Reduce prolonged heat exposure"
    response_text = (
        "Increase hydration, take regular cooling breaks, "
        "and reduce unnecessary outdoor exposure."
    )

elif current_risk >= 30:

    response_class = "warning"
    response_label = "CURRENT RESPONSE"
    response_title = "Monitor rising thermal stress"
    response_text = (
        "Stay hydrated, monitor thermal conditions, "
        "and take cooling breaks when needed."
    )

else:

    response_class = "safe"
    response_label = "CURRENT RESPONSE"
    response_title = "Conditions are relatively safe"
    response_text = (
        "Current conditions support normal activity. "
        "Continue normal hydration and routine monitoring."
    )


st.html(
    f"""
    <div class="
        analytics-insight
        {response_class}
    ">

        <div class="analytics-insight-label">
            {response_label}
        </div>

        <div class="analytics-insight-title">
            {response_title}
        </div>

        <div class="analytics-insight-text">
            {response_text}
        </div>

    </div>
    """
)