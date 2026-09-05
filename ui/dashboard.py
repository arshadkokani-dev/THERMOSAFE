import html
from textwrap import dedent

import streamlit as st

from core.ai_advisor import generate_ai_advice
from ui.theme import get_svg_icon, apply_theme


def show_dashboard(data, population_risks=None):
    """
    Render the THERMOSAFE Command Center.

    The dashboard displays:
    - Current location
    - Current environmental conditions
    - Human thermal risk
    - Risk explanation
    - 5-day thermal outlook
    - Groq-powered AI risk advisory
    """

    # ------------------------------------------------------------
    # THEME
    # ------------------------------------------------------------

    st.html(apply_theme())

    # ------------------------------------------------------------
    # DATA
    # ------------------------------------------------------------

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    heat_index = data.get("heat_index", temperature)

    wind = data.get(
        "wind",
        data.get("wind_speed", 0),
    )

    risk_score = data.get("risk_score", 0)
    risk_level = data.get("risk_level", "UNKNOWN")

    location = html.escape(
        str(data.get("location", "Unknown location"))
    )

    # ------------------------------------------------------------
    # RISK CONFIGURATION
    # ------------------------------------------------------------

    risk_config = {
        "LOW": {
            "color": "#4ade80",
            "class": "risk-low",
            "description": (
                "Current environmental conditions indicate "
                "relatively low thermal stress."
            ),
        },
        "MODERATE": {
            "color": "#facc15",
            "class": "risk-moderate",
            "description": (
                "Thermal stress is beginning to increase, "
                "but conditions remain manageable."
            ),
        },
        "HIGH": {
            "color": "#fb923c",
            "class": "risk-high",
            "description": (
                "Elevated thermal stress is present. "
                "Reducing prolonged heat exposure is recommended."
            ),
        },
        "EXTREME": {
            "color": "#f87171",
            "class": "risk-extreme",
            "description": (
                "Severe thermal stress is present. "
                "Immediate protective measures are recommended."
            ),
        },
    }

    config = risk_config.get(
        risk_level,
        {
            "color": "#94a3b8",
            "class": "risk-low",
            "description": (
                "Thermal conditions are being assessed."
            ),
        },
    )

    risk_color = config["color"]
    risk_class = config["class"]
    risk_description = config["description"]

    # ------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------

    location_icon = get_svg_icon("location")

    st.html(
        dedent(
            f"""
            <div class="thermosafe-header">

                <div>
                    <div class="thermosafe-brand">
                        THERMOSAFE
                    </div>

                    <div class="thermosafe-subtitle">
                        Human Thermal Risk Intelligence
                    </div>
                </div>

                <div class="location-badge">
                    {location_icon}
                    <span>{location}</span>
                </div>

            </div>
            """
        ),
        
    )

    # ------------------------------------------------------------
    # THERMAL RISK HERO
    # ------------------------------------------------------------

    st.html(
        dedent(
            f"""
            <div class="risk-hero">

                <div class="risk-hero-content">

                    <div>

                        <div class="eyebrow">
                            HUMAN THERMAL RISK
                        </div>

                        <div class="risk-number">
                            <span class="risk-score">
                                {risk_score}
                            </span>

                            <span class="risk-denominator">
                                /100
                            </span>
                        </div>

                        <div class="risk-description">
                            {risk_description}
                        </div>

                    </div>

                    <div class="risk-status-block">

                        <div class="eyebrow">
                            CURRENT STATUS
                        </div>

                        <div
                            class="risk-status"
                            style="color:{risk_color};"
                        >
                            {risk_level}
                        </div>

                        <div class="risk-pill {risk_class}">
                            LIVE ASSESSMENT
                        </div>

                    </div>

                </div>

                <div class="risk-progress-track">
                    <div
                        class="risk-progress-fill"
                        style="
                            width:{min(max(risk_score, 0), 100)}%;
                            background:{risk_color};
                        "
                    ></div>
                </div>

            </div>
            """
        ),
        
    )

    # ------------------------------------------------------------
    # CURRENT ENVIRONMENT
    # ------------------------------------------------------------

    environment_icon = get_svg_icon("temperature")

    st.html(
        dedent(
            f"""
            <div class="section-title">
                {environment_icon}
                <span>Current Environment</span>
            </div>
            """
        ),
        
    )

    environment = [
        (
            "temperature",
            "Temperature",
            f"{temperature:.1f} °C",
        ),
        (
            "humidity",
            "Humidity",
            f"{humidity:.0f} %",
        ),
        (
            "heat-index",
            "Heat Index",
            f"{heat_index:.1f} °C",
        ),
        (
            "wind",
            "Wind",
            f"{wind:.1f} km/h",
        ),
    ]

    columns = st.columns(4)

    for column, (icon_name, label, value) in zip(
        columns,
        environment,
    ):
        icon = get_svg_icon(icon_name)

        with column:
            st.html(
                dedent(
                    f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-label">
                            {label}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                    """
                ),
                
            )

    # ------------------------------------------------------------
    # LIVE THERMAL RISK
    # ------------------------------------------------------------

    risk_icon = get_svg_icon("risk")

    st.html(
        dedent(
            f"""
            <div class="section-title">
                {risk_icon}
                <span>Live Thermal Risk</span>
            </div>
            """
        ),
        
    )

    if risk_level == "EXTREME":
        live_message = (
            "Severe thermal stress is present. "
            "Immediate protective action is recommended."
        )
    elif risk_level == "HIGH":
        live_message = (
            "Elevated thermal stress is present. "
            "Reduce prolonged heat exposure."
        )
    elif risk_level == "MODERATE":
        live_message = (
            "Thermal stress is emerging, but current "
            "conditions remain manageable."
        )
    else:
        live_message = (
            "Current thermal conditions are relatively "
            "comfortable for normal activity."
        )

    st.html(
        dedent(
            f"""
            <div class="intelligence-card">

                <div class="live-risk-layout">

                    <div>
                        <div class="card-label">
                            CURRENT THERMAL RISK
                        </div>

                        <div
                            class="live-risk-score"
                            style="color:{risk_color};"
                        >
                            {risk_score}/100
                        </div>
                    </div>

                    <div class="live-risk-message">
                        {live_message}
                    </div>

                </div>

            </div>
            """
        ),
        
    )

    # ------------------------------------------------------------
    # SMART HEAT ALERT + WHY THIS RISK
    # ------------------------------------------------------------

    alert_icon = get_svg_icon("alert")

    if risk_level == "EXTREME":
        alert_title = "Extreme thermal stress detected"
        alert_message = (
            "Avoid prolonged outdoor exposure and prioritize "
            "immediate cooling and hydration."
        )

    elif risk_level == "HIGH":
        alert_title = "High thermal stress detected"
        alert_message = (
            "Reduce prolonged heat exposure and take regular "
            "cooling breaks."
        )

    elif risk_level == "MODERATE":
        alert_title = "Moderate thermal stress detected"
        alert_message = (
            "Conditions are becoming more stressful. "
            "Limit prolonged strenuous exposure."
        )

    else:
        alert_title = "Conditions currently stable"
        alert_message = (
            "Thermal conditions are relatively comfortable "
            "for normal activity."
        )

    # ------------------------------------------------------------
    # RISK FACTORS
    # ------------------------------------------------------------

    factors = []

    if temperature >= 35:
        factors.append(
            f"Temperature is high at {temperature:.1f}°C."
        )
    elif temperature >= 30:
        factors.append(
            f"Temperature is elevated at {temperature:.1f}°C."
        )
    else:
        factors.append(
            f"Temperature is relatively mild at {temperature:.1f}°C."
        )

    if humidity >= 80:
        factors.append(
            f"Humidity is very high at {humidity:.0f}%, "
            "which can reduce cooling efficiency."
        )
    elif humidity >= 60:
        factors.append(
            f"Humidity is elevated at {humidity:.0f}% "
            "and may reduce cooling efficiency."
        )
    else:
        factors.append(
            f"Humidity is relatively moderate at {humidity:.0f}%."
        )

    if wind <= 2:
        factors.append(
            f"Wind is very low at {wind:.1f} km/h."
        )
    elif wind <= 8:
        factors.append(
            f"Wind provides some cooling at {wind:.1f} km/h."
        )
    else:
        factors.append(
            f"Wind provides useful cooling at {wind:.1f} km/h."
        )

    risk_explanation = " ".join(factors)

    columns = st.columns(2)

    # ------------------------------------------------------------
    # SMART HEAT ALERT
    # ------------------------------------------------------------

    with columns[0]:

        st.html(
            dedent(
                f"""
                <div class="section-title">
                    {alert_icon}
                    <span>Smart Heat Alert</span>
                </div>

                <div class="intelligence-card">

                    <div class="card-label">
                        CURRENT STATUS
                    </div>

                    <div class="card-title">
                        {alert_title}
                    </div>

                    <div class="card-text">
                        {alert_message}
                    </div>

                </div>
                """
            ),
            
        )

    # ------------------------------------------------------------
    # WHY THIS RISK
    # ------------------------------------------------------------

    with columns[1]:

        st.html(
            dedent(
                f"""
                <div class="section-title">
                    {risk_icon}
                    <span>Why This Risk?</span>
                </div>

                <div class="intelligence-card">

                    <div class="card-text">
                        {risk_explanation}
                    </div>

                </div>
                """
            ),
            
        )

    # ------------------------------------------------------------
    # 5-DAY THERMAL OUTLOOK
    # ------------------------------------------------------------

    forecast_icon = get_svg_icon("forecast")

    st.html(
        dedent(
            f"""
            <div class="section-title">
                {forecast_icon}
                <span>5-Day Thermal Outlook</span>
            </div>
            """
        ),
        
    )

    forecast_report = st.session_state.get(
        "forecast_report",
        None,
    )

    if forecast_report:

        forecast_data = forecast_report.get(
            "forecast",
            forecast_report,
        )

        if (
            isinstance(forecast_data, list)
            and forecast_data
        ):

            forecast_columns = st.columns(
                min(len(forecast_data[:5]), 5)
            )

            for index, day in enumerate(
                forecast_data[:5]
            ):

                day_temperature = day.get(
                    "temperature",
                    temperature,
                )

                day_risk = day.get(
                    "risk_score",
                    risk_score,
                )

                day_level = day.get(
                    "risk_level",
                    "LOW",
                )

                day_config = risk_config.get(
                    day_level,
                    risk_config["LOW"],
                )

                with forecast_columns[index]:

                    st.html(
                        dedent(
                            f"""
                            <div class="forecast-card">

                                <div class="forecast-day">
                                    DAY {index + 1}
                                </div>

                                <div class="forecast-temperature">
                                    {day_temperature:.1f} °C
                                </div>

                                <div class="forecast-risk">
                                    Thermal risk: {day_risk}/100
                                </div>

                                <div class="risk-pill {day_config["class"]}">
                                    {day_level}
                                </div>

                            </div>
                            """
                        ),
                        
                    )

        else:

            st.info(
                "Forecast data is currently unavailable."
            )

    else:

        st.info(
            "Run an environmental analysis to view "
            "the 5-day thermal outlook."
        )

    # ------------------------------------------------------------
    # AI RISK ADVISOR
    # ------------------------------------------------------------

    ai_icon = get_svg_icon("ai")

    st.html(
        dedent(
            f"""
            <div class="section-title">
                {ai_icon}
                <span>THERMOSAFE AI Risk Advisor</span>
            </div>
            """
        ),
        
    )

    # This remains connected to the real Groq-powered
    # THERMOSAFE AI advisor through core.ai_advisor.

    ai_result = generate_ai_advice(
        temperature=temperature,
        humidity=humidity,
        wind=wind,
        heat_index=heat_index,
        risk_score=risk_score,
        risk_level=risk_level,
        population="General Adult",
    )

    ai_situation = html.escape(
        str(ai_result.get("situation", ""))
    )

    ai_advice = html.escape(
        str(ai_result.get("advice", ""))
    )

    st.html(
        dedent(
            f"""
            <div class="intelligence-card ai-card">

                <div class="ai-header">

                    <div class="card-label">
                        AI ENVIRONMENTAL ASSESSMENT
                    </div>

                    <div class="ai-status">
                        GROQ
                    </div>

                </div>

                <div class="card-title">
                    {ai_situation}
                </div>

                <div class="card-text ai-advice">
                    {ai_advice}
                </div>

            </div>
            """
        ),
        
    )