import streamlit as st

from core.risk import assess_all_populations
from core.ai_advisor import generate_ai_advice


st.title("Risk Intelligence")

st.caption(
    "Human vulnerability analysis and thermal-risk interpretation."
)


# --------------------------------------------------
# CURRENT THERMAL RISK
# --------------------------------------------------

risk_score = st.session_state.get(
    "risk_score",
    0
)

risk_level = st.session_state.get(
    "risk_level",
    "UNKNOWN"
)


st.subheader("Current Thermal Risk")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Environmental Risk",
        f"{risk_score}/100"
    )

with col2:
    st.metric(
        "Current Risk Level",
        risk_level
    )


# --------------------------------------------------
# POPULATION ANALYSIS
# --------------------------------------------------

st.subheader("Population Vulnerability")

population_risks = assess_all_populations(
    risk_score
)

selected_profile = st.selectbox(
    "Select population profile",
    [
        item["profile"]
        for item in population_risks
    ]
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

analyze_population = st.button(
    "Analyze Population Risk",
    type="primary"
)


if analyze_population:

    selected = next(
        item
        for item in population_risks
        if item["profile"] == selected_profile
    )

    st.divider()

    st.subheader(
        f"Analysis: {selected_profile}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Base Risk",
            f'{selected["base_score"]}/100'
        )

    with col2:
        st.metric(
            "Human Risk",
            f'{selected["adjusted_score"]}/100'
        )

    with col3:
        st.metric(
            "Risk Level",
            selected["risk_level"]
        )

    st.info(
        f'Why this population is affected: '
        f'{selected["reason"]}'
    )


    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("Safety Recommendations")

    population_risk_level = selected["risk_level"]

    if population_risk_level == "LOW":

        st.success(
            "Maintain normal hydration and continue "
            "monitoring environmental conditions."
        )

    elif population_risk_level == "MODERATE":

        st.warning(
            "Increase hydration, take regular cooling "
            "breaks, and avoid unnecessary prolonged "
            "heat exposure."
        )

    elif population_risk_level == "HIGH":

        st.error(
            "Reduce prolonged outdoor exposure and "
            "prioritize cooling, hydration, and protection "
            "of vulnerable individuals."
        )

    else:

        st.error(
            "Severe thermal stress conditions detected. "
            "Avoid prolonged exposure and activate "
            "immediate cooling and protection measures."
        )

        # --------------------------------------------------
    # AI RISK ADVISOR
    # --------------------------------------------------

    st.subheader("THERMOSAFE AI Risk Advisor")

    temperature = st.session_state.get(
        "dashboard_data",
        {}
    ).get("temperature", 0)

    humidity = st.session_state.get(
        "dashboard_data",
        {}
    ).get("humidity", 0)

    wind = st.session_state.get(
        "dashboard_data",
        {}
    ).get("wind_speed", 0)

    heat_index = st.session_state.get(
        "dashboard_data",
        {}
    ).get("heat_index", temperature)

    ai_result = generate_ai_advice(
        temperature=temperature,
        humidity=humidity,
        wind=wind,
        heat_index=heat_index,
        risk_score=selected["adjusted_score"],
        risk_level=selected["risk_level"],
        population=selected_profile,
    )

    st.info(
        ai_result["advice"]
    )

else:

    st.info(
        "Select a population profile and click "
        "'Analyze Population Risk' to generate "
        "a vulnerability assessment."
    )

    