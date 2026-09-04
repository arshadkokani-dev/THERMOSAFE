import streamlit as st
import pandas as pd

from forecast.predictor import build_forecast_report


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("Risk Analytics")

st.caption(
    "Thermal-risk trends, forecast intelligence, and early-warning analysis."
)


# --------------------------------------------------
# GET SHARED DATA
# --------------------------------------------------

dashboard_data = st.session_state.get(
    "dashboard_data",
    None
)



# --------------------------------------------------
# SAFETY CHECK
# --------------------------------------------------

if dashboard_data is None:

    st.warning(
        "No environmental data available yet. "
        "Return to the Command Center and click "
        "'Analyze Conditions' first."
    )

    st.stop()


# --------------------------------------------------
# CURRENT DATA
# --------------------------------------------------

current_risk = dashboard_data.get(
    "risk_score",
    0
)

current_level = dashboard_data.get(
    "risk_level",
    "UNKNOWN"
)

temperature = dashboard_data.get(
    "temperature",
    0
)

humidity = dashboard_data.get(
    "humidity",
    0
)

wind_speed = dashboard_data.get(
    "wind_speed",
    0
)

heat_index = dashboard_data.get(
    "heat_index",
    temperature
)

forecast_report = build_forecast_report(
    current_temperature=temperature,
    current_humidity=humidity,
    current_wind=wind_speed,
    days=5,
)

st.session_state["forecast_report"] = forecast_report


# --------------------------------------------------
# CURRENT RISK OVERVIEW
# --------------------------------------------------

st.subheader("Current Risk Overview")

cols = st.columns(4)

cols[0].metric(
    "CURRENT RISK",
    f"{current_risk}/100"
)

cols[1].metric(
    "RISK LEVEL",
    current_level
)

cols[2].metric(
    "TEMPERATURE",
    f"{temperature:.1f} °C"
)

cols[3].metric(
    "HUMIDITY",
    f"{humidity:.0f}%"
)


# --------------------------------------------------
# 5-DAY FORECAST ANALYSIS
# --------------------------------------------------

st.subheader("5-Day Risk Outlook")


if forecast_report:

    # Try to get forecast list
    forecast_data = forecast_report.get(
        "forecast",
        forecast_report
    )

    if isinstance(forecast_data, list):

        risks = []
        temperatures = []

        for day in forecast_data:

            day_temperature = day.get(
                "temperature",
                temperature
            )

            day_risk = day.get(
                "risk_score",
                current_risk
            )

            temperatures.append(
                day_temperature
            )

            risks.append(
                day_risk
            )

        if risks:

            average_risk = sum(risks) / len(risks)
            peak_risk = max(risks)

            high_days = sum(
                1 for risk in risks
                if risk >= 50
            )

            forecast_cols = st.columns(4)

            forecast_cols[0].metric(
                "5-DAY AVERAGE",
                f"{average_risk:.1f}/100"
            )

            forecast_cols[1].metric(
                "PEAK RISK",
                f"{peak_risk}/100"
            )

            forecast_cols[2].metric(
                "HIGH / EXTREME DAYS",
                high_days
            )

            forecast_cols[3].metric(
                "HEATWAVE",
                "YES" if high_days >= 2 else "NO"
            )

            # ------------------------------------------
            # RISK TREND
            # ------------------------------------------

            st.subheader("📈 Thermal Risk Trend")

            chart_data = pd.DataFrame(
                {
                    "Day": [
                        f"Day {i + 1}"
                        for i in range(len(risks))
                    ],
                    "Risk": risks,
                }
            )

            st.line_chart(
                chart_data.set_index("Day")
            )

            # ------------------------------------------
            # FORECAST TABLE
            # ------------------------------------------

            st.subheader(
                "Daily Thermal Risk Forecast"
            )

            for index, day in enumerate(
                forecast_data
            ):

                day_temperature = day.get(
                    "temperature",
                    temperature
                )

                day_risk = day.get(
                    "risk_score",
                    current_risk
                )

                day_level = day.get(
                    "risk_level",
                    "UNKNOWN"
                )

                col1, col2, col3 = st.columns(3)

                col1.write(
                    f"**Day {index + 1}**"
                )

                col2.write(
                    f"{day_temperature:.1f} °C"
                )

                col3.write(
                    f"{day_risk}/100 — {day_level}"
                )

        else:

            st.info(
                "Forecast data is available but contains no risk values."
            )

    else:

        st.info(
            "Forecast format could not be analyzed yet."
        )

else:

    st.info(
        "Forecast data is not available yet. "
        "Run an environmental analysis first."
    )


# --------------------------------------------------
# EARLY WARNING
# --------------------------------------------------

st.subheader("🔥 Heatwave Intelligence")


if current_risk >= 75:

    st.error(
        "EXTREME RISK: Immediate heat-protection "
        "measures are recommended."
    )

elif current_risk >= 50:

    st.warning(
        "HIGH RISK: Increased thermal stress detected. "
        "Limit prolonged exposure and increase cooling."
    )

elif current_risk >= 30:

    st.warning(
        "MODERATE RISK: Thermal stress is increasing. "
        "Continue hydration and monitor conditions."
    )

else:

    st.success(
        "LOW RISK: Current conditions indicate "
        "relatively low thermal stress."
    )


# --------------------------------------------------
# RECOMMENDED RESPONSE
# --------------------------------------------------

st.subheader("🛡️ Recommended Response")


if current_risk >= 75:

    st.error(
        "Avoid prolonged outdoor exposure. "
        "Prioritize cooling, hydration, and protection "
        "of vulnerable populations."
    )

elif current_risk >= 50:

    st.warning(
        "Increase hydration, take regular cooling breaks, "
        "and reduce unnecessary outdoor exposure."
    )

elif current_risk >= 30:

    st.info(
        "Stay hydrated, monitor thermal conditions, "
        "and take cooling breaks when needed."
    )

else:

    st.success(
        "Current conditions are relatively safe. "
        "Continue normal hydration and monitoring."
    )