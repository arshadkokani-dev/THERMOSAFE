import streamlit as st

from core.thermal import assess_thermal_risk
from core.risk import assess_population_risk


def show_simulator(base_data):

    st.markdown(
        "## Thermal Risk Simulator"
    )

    st.caption(
        "Explore how changing environmental conditions "
        "can affect human thermal risk."
    )

    st.divider()

    # --------------------------------------------------
    # SCENARIO INPUTS
    # --------------------------------------------------

    st.subheader("Scenario Conditions")

    col1, col2, col3 = st.columns(3)

    with col1:
        temperature = st.slider(
            "Temperature (°C)",
            min_value=15.0,
            max_value=50.0,
            value=float(base_data["temperature"]),
            step=0.5,
        )

    with col2:
        humidity = st.slider(
            "Humidity (%)",
            min_value=10,
            max_value=100,
            value=int(base_data["humidity"]),
            step=1,
        )

    with col3:
        wind_speed = st.slider(
            "Wind Speed (km/h)",
            min_value=0.0,
            max_value=30.0,
            value=float(base_data["wind_speed"]),
            step=0.5,
        )

    st.subheader("Population Profile")

    profile = st.selectbox(
        "Who are we assessing?",
        [
            "General Adult",
            "Outdoor Worker",
            "Elderly",
            "Child",
            "Athlete",
        ],
    )

    st.divider()

    # --------------------------------------------------
    # ANALYZE SCENARIO
    # --------------------------------------------------

    analyze_scenario = st.button(
        "Analyze Scenario",
        type="primary",
    )

    if analyze_scenario:

        thermal_result = assess_thermal_risk(
            temperature_c=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
        )

        population_result = assess_population_risk(
            base_risk_score=thermal_result["risk_score"],
            profile=profile,
        )

        st.subheader("Scenario Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Thermal Stress",
                f'{thermal_result["risk_score"]}/100',
            )

        with result_col2:
            st.metric(
                "Human Risk",
                f'{population_result["adjusted_score"]}/100',
            )

        with result_col3:
            st.metric(
                "Risk Level",
                population_result["risk_level"],
            )

        st.divider()

        st.subheader(
            f"Assessment for {profile}"
        )

        st.write(
            population_result["reason"]
        )

        risk_level = population_result["risk_level"]

        if risk_level == "LOW":

            st.success(
                "LOW RISK — Current scenario indicates "
                "limited thermal stress."
            )

            st.write(
                "Recommended: Maintain normal hydration "
                "and continue monitoring conditions."
            )

        elif risk_level == "MODERATE":

            st.warning(
                "MODERATE RISK — Thermal stress may "
                "increase with prolonged exposure."
            )

            st.write(
                "Recommended: Increase hydration, "
                "take regular cooling breaks, and "
                "avoid unnecessary prolonged exposure."
            )

        elif risk_level == "HIGH":

            st.error(
                "HIGH RISK — Significant thermal stress "
                "may occur under these conditions."
            )

            st.write(
                "Recommended: Reduce prolonged outdoor "
                "exposure, increase cooling breaks, "
                "and prioritize vulnerable individuals."
            )

        else:

            st.error(
                "EXTREME RISK — Severe thermal stress "
                "conditions detected."
            )

            st.write(
                "Recommended: Avoid prolonged outdoor "
                "exposure, activate cooling measures, "
                "and prioritize immediate protection "
                "of vulnerable populations."
            )

        st.divider()

        st.caption(
            "THERMOSAFE scenario analysis uses the same "
            "thermal-risk engine as the live monitoring system."
        )