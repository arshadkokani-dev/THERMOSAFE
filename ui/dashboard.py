import streamlit as st


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

    if risk_score >= 75:

        st.error(
            "EXTREME HEAT ALERT: Severe thermal stress detected. "
            "Avoid prolonged outdoor exposure and activate immediate "
            "cooling and hydration measures."
        )

    elif risk_score >= 50:

        st.warning(
            "HIGH HEAT ALERT: Elevated thermal stress detected. "
            "Increase hydration, take frequent cooling breaks, "
            "and limit prolonged heat exposure."
        )

    elif risk_score >= 30:

        st.warning(
            "MODERATE HEAT ALERT: Thermal stress is increasing. "
            "Stay hydrated and monitor conditions, especially for "
            "vulnerable individuals."
        )

    else:

        st.success(
            "LOW HEAT RISK: Current conditions are within a relatively "
            "safe range. Continue normal hydration and monitoring."
        )

    # ============================================================
    # VULNERABLE POPULATION RISK
    # ============================================================

    st.markdown(
        '<div class="section-title">Vulnerable Population Risk</div>',
        unsafe_allow_html=True
    )

    if population_risks:

        selected_profile = st.selectbox(
            "Select a population profile",
            [
                item["profile"]
                for item in population_risks
            ]
        )

        selected_risk = next(
            item
            for item in population_risks
            if item["profile"] == selected_profile
        )

        profile_cols = st.columns(3)

        profile_cols[0].metric(
            "BASE ENVIRONMENTAL RISK",
            f'{selected_risk["base_score"]}/100'
        )

        profile_cols[1].metric(
            "HUMAN RISK",
            f'{selected_risk["adjusted_score"]}/100'
        )

        profile_cols[2].metric(
            "RISK LEVEL",
            selected_risk["risk_level"]
        )

        st.info(
            f'Why this profile? {selected_risk["reason"]}'
        )