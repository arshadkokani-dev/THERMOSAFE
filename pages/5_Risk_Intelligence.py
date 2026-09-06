import streamlit as st

from core.risk import assess_all_populations
from core.ai_advisor import generate_ai_advice
from core.recommendations import generate_safety_plan
from ui.theme import apply_theme


# =========================================================
# THERMOSAFE — RISK INTELLIGENCE
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
                Risk Intelligence
            </div>

            <div class="analytics-section-subtitle">
                Human vulnerability analysis, adaptive safety
                recommendations, and AI-powered risk interpretation.
            </div>

        </div>

    </div>
    """
)


# =========================================================
# CURRENT CONDITIONS
# =========================================================

dashboard_data = st.session_state.get(
    "dashboard_data",
    None,
)


if dashboard_data is None:

    st.warning(
        "No environmental analysis is available yet. "
        "Return to the Command Center and click "
        "'Analyze Conditions' first."
    )

    st.stop()


risk_score = float(
    dashboard_data.get(
        "risk_score",
        0,
    )
)

risk_level = str(
    dashboard_data.get(
        "risk_level",
        "UNKNOWN",
    )
).upper()

temperature = float(
    dashboard_data.get(
        "temperature",
        0,
    )
)

humidity = float(
    dashboard_data.get(
        "humidity",
        0,
    )
)

wind = float(
    dashboard_data.get(
        "wind_speed",
        0,
    )
)

heat_index = float(
    dashboard_data.get(
        "heat_index",
        temperature,
    )
)

location = dashboard_data.get(
    "location",
    "Current Location",
)


# =========================================================
# LOCATION
# =========================================================

st.html(
    f"""
    <div class="location-badge">

        <span>{location}</span>

        <span>•</span>

        <span>LIVE RISK INTELLIGENCE</span>

    </div>
    """
)


# =========================================================
# CURRENT THERMAL RISK
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Current Thermal Risk
    </div>

    <div class="analytics-section-subtitle">
        Environmental conditions currently driving human thermal risk.
    </div>
    """
)


risk_overview = [
    (
        "ENVIRONMENTAL RISK",
        f"{risk_score:.0f}/100",
    ),
    (
        "RISK LEVEL",
        risk_level,
    ),
    (
        "HEAT INDEX",
        f"{heat_index:.1f} °C",
    ),
    (
        "TEMPERATURE",
        f"{temperature:.1f} °C",
    ),
]


risk_cols = st.columns(4)


for col, (label, value) in zip(
    risk_cols,
    risk_overview,
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


# =========================================================
# POPULATION VULNERABILITY
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Population Vulnerability
    </div>

    <div class="analytics-section-subtitle">
        Compare how different population groups may respond
        to the current thermal conditions.
    </div>
    """
)


population_risks = assess_all_populations(
    risk_score
)


# ---------------------------------------------------------
# POPULATION SNAPSHOT
# ---------------------------------------------------------

population_cols = st.columns(
    len(population_risks)
)


for col, item in zip(
    population_cols,
    population_risks,
):

    with col:

        profile = item["profile"]
        adjusted_score = float(
            item["adjusted_score"]
        )
        level = str(
            item["risk_level"]
        ).upper()

        st.html(
            f"""
            <div class="risk-population-card">

                <div class="analytics-label">
                    {profile.upper()}
                </div>

                <div class="risk-population-score">
                    {adjusted_score:.0f}
                    <span>/100</span>
                </div>

                <div class="risk-population-level">
                    {level}
                </div>

            </div>
            """
        )


# =========================================================
# SELECT PROFILE
# =========================================================

selected_profile = st.selectbox(
    "Select population profile",
    [
        item["profile"]
        for item in population_risks
    ],
)


selected = next(
    item
    for item in population_risks
    if item["profile"] == selected_profile
)


# =========================================================
# SELECTED POPULATION ANALYSIS
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Vulnerability Assessment
    </div>

    <div class="analytics-section-subtitle">
        Detailed thermal-risk assessment for the selected population.
    </div>
    """
)


assessment_col1, assessment_col2, assessment_col3 = (
    st.columns(3)
)


with assessment_col1:

    st.html(
        f"""
        <div class="analytics-metric">

            <div class="analytics-label">
                BASE RISK
            </div>

            <div class="analytics-value">
                {float(selected["base_score"]):.0f}/100
            </div>

        </div>
        """
    )


with assessment_col2:

    st.html(
        f"""
        <div class="analytics-metric">

            <div class="analytics-label">
                HUMAN RISK
            </div>

            <div class="analytics-value">
                {float(selected["adjusted_score"]):.0f}/100
            </div>

        </div>
        """
    )


with assessment_col3:

    st.html(
        f"""
        <div class="analytics-metric">

            <div class="analytics-label">
                RISK LEVEL
            </div>

            <div class="analytics-value">
                {str(selected["risk_level"]).upper()}
            </div>

        </div>
        """
    )


# =========================================================
# WHY THIS POPULATION IS AFFECTED
# =========================================================

st.html(
    f"""
    <div class="analytics-insight warning">

        <div class="analytics-insight-label">
            VULNERABILITY INTERPRETATION
        </div>

        <div class="analytics-insight-title">
            Why {selected_profile} may be affected
        </div>

        <div class="analytics-insight-text">
            {selected["reason"]}
        </div>

    </div>
    """
)


# =========================================================
# SAFETY RECOMMENDATIONS
# =========================================================

st.html(
    """
    <div class="analytics-section">
        Adaptive Safety Recommendations
    </div>

    <div class="analytics-section-subtitle">
        Recommended protective actions based on risk severity
        and population vulnerability.
    </div>
    """
)


safety_plan = generate_safety_plan(
    risk_score=float(
        selected["adjusted_score"]
    ),
    risk_level=selected["risk_level"],
    population=selected_profile,
)


for action in safety_plan:

    priority = str(
        action.get(
            "priority",
            "MODERATE",
        )
    ).upper()

    if priority == "CRITICAL":
        priority_class = "critical"

    elif priority == "HIGH":
        priority_class = "danger"

    elif priority == "MODERATE":
        priority_class = "warning"

    else:
        priority_class = "safe"


    st.html(
        f"""
        <div class="
            risk-action-card
            {priority_class}
        ">

            <div class="risk-action-priority">
                {priority}
            </div>

            <div class="risk-action-title">
                {action["title"]}
            </div>

            <div class="risk-action-message">
                {action["message"]}
            </div>

        </div>
        """
    )


# =========================================================
# AI RISK ADVISOR
# =========================================================

st.html(
    """
    <div class="analytics-section">
        THERMOSAFE AI Risk Advisor
    </div>

    <div class="analytics-section-subtitle">
        AI-generated interpretation of the current environmental
        and population-specific risk.
    </div>
    """
)


ai_result = generate_ai_advice(
    temperature=temperature,
    humidity=humidity,
    wind=wind,
    heat_index=heat_index,
    risk_score=float(
        selected["adjusted_score"]
    ),
    risk_level=selected["risk_level"],
    population=selected_profile,
)


st.html(
    f"""
    <div class="risk-ai-card">

        <div class="risk-ai-label">
            AI RISK INTERPRETATION
        </div>

        <div class="risk-ai-text">
            {ai_result["advice"]}
        </div>

    </div>
    """
)


# =========================================================
# ENGINE NOTE
# =========================================================

st.caption(
    "THERMOSAFE Risk Intelligence combines the environmental "
    "thermal-risk engine, population vulnerability assessment, "
    "adaptive safety planning, and AI interpretation."
)