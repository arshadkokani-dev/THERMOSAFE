import streamlit as st

from core.thermal import assess_thermal_risk
from core.risk import assess_population_risk


def show_simulator(base_data):

    # =====================================================
    # BASELINE
    # =====================================================

    location = base_data.get(
        "location",
        "Current Location",
    )

    baseline_temperature = float(
        base_data["temperature"]
    )

    baseline_humidity = float(
        base_data["humidity"]
    )

    baseline_wind = float(
        base_data["wind_speed"]
    )


    # =====================================================
    # LOCATION BADGE
    # =====================================================

    st.html(
        f"""
        <div class="location-badge">

            <span>{location}</span>

            <span>•</span>

            <span>BASELINE CONDITIONS</span>

        </div>
        """
    )


    # =====================================================
    # BASELINE CONDITIONS
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Baseline Conditions
        </div>

        <div class="analytics-section-subtitle">
            Current environmental conditions used as the
            starting point for the simulation.
        </div>
        """
    )


    baseline = [
        (
            "TEMPERATURE",
            f"{baseline_temperature:.1f} °C",
        ),
        (
            "HUMIDITY",
            f"{baseline_humidity:.0f}%",
        ),
        (
            "WIND SPEED",
            f"{baseline_wind:.1f} km/h",
        ),
    ]


    baseline_cols = st.columns(3)


    for col, (label, value) in zip(
        baseline_cols,
        baseline,
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
    # SCENARIO CONDITIONS
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            What-If Scenario
        </div>

        <div class="analytics-section-subtitle">
            Change environmental conditions and evaluate
            the resulting human thermal risk.
        </div>
        """
    )


    col1, col2 = st.columns(2)


    with col1:

        temperature = st.slider(
            "Temperature (°C)",
            min_value=15.0,
            max_value=50.0,
            value=baseline_temperature,
            step=0.5,
        )


    with col2:

        humidity = st.slider(
            "Humidity (%)",
            min_value=10,
            max_value=100,
            value=int(
                round(
                    baseline_humidity
                )
            ),
            step=1,
        )


    col3, col4 = st.columns(2)


    with col3:

        wind_speed = st.slider(
            "Wind Speed (km/h)",
            min_value=0.0,
            max_value=30.0,
            value=baseline_wind,
            step=0.5,
        )


    with col4:

        population = st.number_input(
            "Affected Population",
            min_value=0,
            max_value=1_000_000,
            value=10_000,
            step=1_000,
        )


    # =====================================================
    # POPULATION PROFILE
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Population Profile
        </div>

        <div class="analytics-section-subtitle">
            Select the population group being assessed.
        </div>
        """
    )


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


    # =====================================================
    # SCENARIO DELTA
    # =====================================================

    temperature_delta = (
        temperature
        - baseline_temperature
    )

    humidity_delta = (
        humidity
        - baseline_humidity
    )

    wind_delta = (
        wind_speed
        - baseline_wind
    )


    st.html(
        f"""
        <div class="simulation-delta">

            <div>
                <span class="simulation-delta-label">
                    Temperature
                </span>

                <strong>
                    {temperature_delta:+.1f} °C
                </strong>
            </div>

            <div>
                <span class="simulation-delta-label">
                    Humidity
                </span>

                <strong>
                    {humidity_delta:+.0f}%
                </strong>
            </div>

            <div>
                <span class="simulation-delta-label">
                    Wind
                </span>

                <strong>
                    {wind_delta:+.1f} km/h
                </strong>
            </div>

        </div>
        """
    )


    # =====================================================
    # RUN SIMULATION
    # =====================================================

    st.write("")

    analyze_scenario = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
    )


    if not analyze_scenario:
        return


    # =====================================================
    # THERMAL RISK
    # =====================================================

    thermal_result = assess_thermal_risk(
        temperature_c=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
    )


    # =====================================================
    # POPULATION RISK
    # =====================================================

    population_result = assess_population_risk(
        base_risk_score=thermal_result[
            "risk_score"
        ],
        profile=profile,
    )


    simulated_score = float(
        population_result[
            "adjusted_score"
        ]
    )

    simulated_level = str(
        population_result[
            "risk_level"
        ]
    ).upper()


    # =====================================================
    # BASELINE RISK
    # =====================================================

    baseline_thermal = assess_thermal_risk(
        temperature_c=baseline_temperature,
        humidity=baseline_humidity,
        wind_speed=baseline_wind,
    )


    baseline_population = assess_population_risk(
        base_risk_score=baseline_thermal[
            "risk_score"
        ],
        profile=profile,
    )


    baseline_score = float(
        baseline_population[
            "adjusted_score"
        ]
    )


    risk_change = (
        simulated_score
        - baseline_score
    )


    # =====================================================
    # RESULT
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Simulation Result
        </div>

        <div class="analytics-section-subtitle">
            Projected thermal risk under the selected scenario.
        </div>
        """
    )


    result_col1, result_col2, result_col3 = st.columns(3)


    with result_col1:

        st.html(
            f"""
            <div class="simulation-result-card">

                <div class="analytics-label">
                    SIMULATED RISK
                </div>

                <div class="simulation-score">
                    {simulated_score:.0f}
                    <span>/100</span>
                </div>

            </div>
            """
        )


    with result_col2:

        change_arrow = (
            "↑"
            if risk_change > 0
            else "↓"
            if risk_change < 0
            else "→"
        )

        st.html(
            f"""
            <div class="simulation-result-card">

                <div class="analytics-label">
                    RISK CHANGE
                </div>

                <div class="simulation-score">
                    {change_arrow}
                    {abs(risk_change):.0f}
                    <span>points</span>
                </div>

            </div>
            """
        )


    with result_col3:

        st.html(
            f"""
            <div class="simulation-result-card">

                <div class="analytics-label">
                    RISK LEVEL
                </div>

                <div class="simulation-level">
                    {simulated_level}
                </div>

            </div>
            """
        )


    # =====================================================
    # BEFORE / AFTER
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Baseline vs Scenario
        </div>
        """
    )


    comparison_col1, comparison_col2 = (
        st.columns(2)
    )


    with comparison_col1:

        st.html(
            f"""
            <div class="simulation-comparison-card">

                <div class="analytics-label">
                    BASELINE
                </div>

                <div class="simulation-comparison-score">
                    {baseline_score:.0f}/100
                </div>

                <div class="simulation-comparison-level">
                    {str(
                        baseline_population["risk_level"]
                    ).upper()}
                </div>

            </div>
            """
        )


    with comparison_col2:

        st.html(
            f"""
            <div class="simulation-comparison-card">

                <div class="analytics-label">
                    SIMULATED
                </div>

                <div class="simulation-comparison-score">
                    {simulated_score:.0f}/100
                </div>

                <div class="simulation-comparison-level">
                    {simulated_level}
                </div>

            </div>
            """
        )


    # =====================================================
    # IMPACT INTERPRETATION
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Impact Analysis
        </div>

        <div class="analytics-section-subtitle">
            Interpretation of the simulated conditions.
        </div>
        """
    )


    if risk_change >= 15:

        insight_class = "critical"

        insight_label = (
            "SIGNIFICANT RISK INCREASE"
        )

        insight_title = (
            "Thermal stress rises substantially"
        )

        insight_text = (
            f"The simulated conditions increase "
            f"human thermal risk by "
            f"{risk_change:.0f} points. "
            f"Under this scenario, "
            f"{profile.lower()} populations "
            f"should receive increased protection."
        )


    elif risk_change >= 5:

        insight_class = "danger"

        insight_label = (
            "RISK INCREASE"
        )

        insight_title = (
            "Thermal conditions become more demanding"
        )

        insight_text = (
            f"The simulated scenario increases "
            f"thermal risk by "
            f"{risk_change:.0f} points. "
            f"Additional hydration and cooling "
            f"measures may become necessary."
        )


    elif risk_change <= -5:

        insight_class = "safe"

        insight_label = (
            "RISK REDUCTION"
        )

        insight_title = (
            "Thermal conditions improve"
        )

        insight_text = (
            f"The simulated scenario reduces "
            f"thermal risk by "
            f"{abs(risk_change):.0f} points. "
            f"These conditions are comparatively "
            f"less thermally stressful."
        )


    else:

        insight_class = "warning"

        insight_label = (
            "LIMITED CHANGE"
        )

        insight_title = (
            "Thermal risk remains relatively stable"
        )

        insight_text = (
            "The selected environmental changes "
            "do not substantially alter the "
            "overall thermal-risk state."
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


    # =====================================================
    # POPULATION IMPACT
    # =====================================================

    st.html(
        f"""
        <div class="analytics-section">
            Population Impact
        </div>

        <div class="analytics-section-subtitle">
            Scenario assessment for approximately
            {population:,.0f} affected people.
        </div>
        """
    )


    st.html(
        f"""
        <div class="simulation-population-card">

            <div class="simulation-population-number">
                {population:,.0f}
            </div>

            <div class="simulation-population-label">
                PEOPLE IN SIMULATED EXPOSURE
            </div>

            <div class="simulation-population-text">
                Assessment profile:
                <strong>{profile}</strong>
            </div>

            <div class="simulation-population-text">
                Current simulated risk:
                <strong>
                    {simulated_score:.0f}/100
                    {simulated_level}
                </strong>
            </div>

        </div>
        """
    )


    # =====================================================
    # RECOMMENDATION
    # =====================================================

    if simulated_level == "LOW":

        recommendation = (
            "Normal activity can generally continue. "
            "Maintain routine hydration and monitor "
            "environmental conditions."
        )

    elif simulated_level == "MODERATE":

        recommendation = (
            "Increase hydration and schedule regular "
            "cooling breaks, especially during prolonged "
            "outdoor exposure."
        )

    elif simulated_level == "HIGH":

        recommendation = (
            "Reduce prolonged outdoor exposure, "
            "increase cooling breaks, and prioritize "
            "protection for vulnerable populations."
        )

    else:

        recommendation = (
            "Avoid prolonged outdoor exposure. "
            "Activate cooling measures and prioritize "
            "immediate protection of vulnerable populations."
        )


    st.html(
        f"""
        <div class="analytics-insight warning">

            <div class="analytics-insight-label">
                SIMULATED RESPONSE
            </div>

            <div class="analytics-insight-title">
                Recommended Action
            </div>

            <div class="analytics-insight-text">
                {recommendation}
            </div>

        </div>
        """
    )


    # =====================================================
    # ENGINE NOTE
    # =====================================================

    st.caption(
        "THERMOSAFE simulation uses the same thermal-risk "
        "and population-risk engines as the live monitoring system."
    )