import streamlit as st

from core.recommendations import generate_safety_plan
from core.ai_advisor import generate_ai_advice


def show_dashboard(data, population_risks=None):

    # ============================================================
    # STYLING
    # ============================================================

    st.markdown(
        """
        <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .subtitle {
            color: #8b95a7;
            font-size: 16px;
            margin-bottom: 28px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # TITLE
    # ============================================================

    st.markdown(
        '<div class="main-title">THERMOSAFE Command Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Real-time environmental monitoring and human thermal risk intelligence.'
        '</div>',
        unsafe_allow_html=True
    )

    # ============================================================
    # CURRENT ENVIRONMENT
    # ============================================================

    st.markdown(
        '<div class="section-title">Current Environment</div>',
        unsafe_allow_html=True
    )

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    heat_index = data.get("heat_index", temperature)
    wind = data.get("wind", data.get("wind_speed", 0))

    cols = st.columns(4)

    cols[0].metric(
        "TEMPERATURE",
        f"{temperature:.1f} °C"
    )

    cols[1].metric(
        "HUMIDITY",
        f"{humidity:.0f} %"
    )

    cols[2].metric(
        "HEAT INDEX",
        f"{heat_index:.1f} °C"
    )

    cols[3].metric(
        "WIND",
        f"{wind:.1f} km/h"
    )

    # ============================================================
    # HUMAN THERMAL RISK
    # ============================================================

    st.markdown(
        '<div class="section-title">Human Thermal Risk</div>',
        unsafe_allow_html=True
    )

    risk_score = data.get("risk_score", 0)
    risk_level = data.get("risk_level", "ANALYZING")

    risk_cols = st.columns(2)

    risk_cols[0].metric(
        "THERMAL STRESS SCORE",
        f"{risk_score}/100"
    )

    risk_cols[1].metric(
        "RISK LEVEL",
        risk_level
    )

    # ============================================================
    # LIVE THERMAL RISK LEVEL
    # ============================================================

    st.markdown(
        '<div class="section-title">🔥 Live Thermal Risk Level</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "CURRENT THERMAL RISK",
        f"{risk_score}/100"
    )

    if risk_level == "EXTREME":
        st.error("🔴 EXTREME — Immediate protective action recommended.")

    elif risk_level == "HIGH":
        st.warning("🟠 HIGH — Reduce heat exposure and increase cooling breaks.")

    elif risk_level == "MODERATE":
        st.warning("🟡 MODERATE — Stay hydrated and continue monitoring conditions.")

    else:
        st.success("🟢 LOW — Current thermal conditions are relatively safe.")

    st.progress(
        min(max(risk_score / 100, 0.0), 1.0),
        text=f"Thermal Risk Level — {risk_score}/100"
    )

    st.info(
        "THERMOSAFE has analyzed the current environmental conditions."
    )

    # ============================================================
    # SMART HEAT ALERT
    # ============================================================

    st.markdown(
        '<div class="section-title">🚨 Smart Heat Alert</div>',
        unsafe_allow_html=True
    )

    if risk_level == "EXTREME":
        st.error(
            "EXTREME HEAT ALERT: Severe thermal stress detected. "
            "Avoid prolonged outdoor exposure and activate immediate "
            "cooling and hydration measures."
        )

    elif risk_level == "HIGH":
        st.warning(
            "HIGH HEAT ALERT: Elevated thermal stress detected. "
            "Increase hydration and take frequent cooling breaks."
        )

    elif risk_level == "MODERATE":
        st.warning(
            "MODERATE HEAT ALERT: Thermal stress is increasing. "
            "Stay hydrated and monitor conditions carefully."
        )

    else:
        st.success(
            "LOW HEAT RISK: Current conditions are within a relatively "
            "safe range. Continue normal hydration and monitoring."
        )

    # ============================================================
    # 5-DAY THERMAL OUTLOOK
    # ============================================================

    st.markdown(
        '<div class="section-title">5-Day Thermal Outlook</div>',
        unsafe_allow_html=True
    )

    forecast_report = st.session_state.get(
        "forecast_report",
        None
    )

    if forecast_report:

        forecast_data = forecast_report.get(
            "forecast",
            forecast_report
        )

        if isinstance(forecast_data, list) and forecast_data:

            forecast_cols = st.columns(
                min(len(forecast_data), 5)
            )

            for index, day in enumerate(
                forecast_data[:5]
            ):

                day_temperature = day.get(
                    "temperature",
                    temperature
                )

                day_risk = day.get(
                    "risk_score",
                    risk_score
                )

                day_level = day.get(
                    "risk_level",
                    "UNKNOWN"
                )

                with forecast_cols[index]:

                    st.metric(
                        f"DAY {index + 1}",
                        f"{day_temperature:.1f} °C"
                    )

                    st.caption(
                        f"Risk {day_risk}/100"
                    )

                    st.write(
                        day_level
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

    # ============================================================
    # AI RISK ADVISOR
    # ============================================================

    st.markdown(
        '<div class="section-title">THERMOSAFE AI Risk Advisor</div>',
        unsafe_allow_html=True
    )

    ai_result = generate_ai_advice(
        temperature=temperature,
        humidity=humidity,
        wind=wind,
        heat_index=heat_index,
        risk_score=risk_score,
        risk_level=risk_level,
        population="General Adult"
    )

    st.info(
        ai_result["advice"]
    )
