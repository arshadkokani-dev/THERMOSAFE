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
    # POPULATION SELECTION
    # ============================================================

    selected_profile = "General Adult"

    if population_risks:

        selected_profile = st.selectbox(
            "Select population profile",
            [
                item["profile"]
                for item in population_risks
            ],
            key="population_profile"
        )

    # ============================================================
    # EXPLAINABLE RISK INTELLIGENCE
    # ============================================================

    st.markdown(
        '<div class="section-title">🔎 Why This Risk?</div>',
        unsafe_allow_html=True
    )

    factors = []

    if temperature >= 35:
        factors.append(
            "🌡️ High temperature is increasing thermal stress."
        )

    elif temperature >= 30:
        factors.append(
            "🌡️ Elevated temperature is contributing to thermal stress."
        )

    else:
        factors.append(
            "🌡️ Temperature is currently within a relatively moderate range."
        )


    if humidity >= 80:
        factors.append(
            f"💧 Very high humidity ({humidity:.0f}%) is reducing "
            "the body's ability to cool through sweating."
        )

    elif humidity >= 60:
        factors.append(
            f"💧 Elevated humidity ({humidity:.0f}%) may reduce "
            "cooling efficiency."
        )

    else:
        factors.append(
            f"💧 Humidity ({humidity:.0f}%) is providing "
            "relatively better cooling conditions."
        )


    if wind <= 2:
        factors.append(
            f"💨 Very low wind ({wind:.1f} km/h) provides "
            "limited air movement for cooling."
        )

    elif wind <= 8:
        factors.append(
            f"💨 Moderate air movement ({wind:.1f} km/h) "
            "provides some cooling."
        )

    else:
        factors.append(
            f"💨 Stronger wind ({wind:.1f} km/h) improves "
            "evaporative cooling."
        )


    for factor in factors:
        st.write(factor)


    if risk_score >= 75:

        st.error(
            "Overall interpretation: Severe thermal conditions "
            "require immediate protective action."
        )

    elif risk_score >= 50:

        st.warning(
            "Overall interpretation: Elevated thermal stress "
            "requires increased hydration and cooling breaks."
        )

    elif risk_score >= 30:

        st.warning(
            "Overall interpretation: Thermal stress is increasing. "
            "Continue monitoring conditions carefully."
        )

    else:

        st.success(
            "Overall interpretation: Current environmental conditions "
            "present relatively low thermal stress."
        )


    # ============================================================
    # PERSONALIZED SAFETY ACTION PLAN
    # ============================================================

    st.markdown(
        '<div class="section-title">🛡️ Personalized Safety Action Plan</div>',
        unsafe_allow_html=True
    )

    safety_plan = generate_safety_plan(
        risk_score=risk_score,
        risk_level=risk_level,
        population=selected_profile
    )

    for action in safety_plan:

        priority = action["priority"]

        if priority == "CRITICAL":

            st.error(
                f'🚨 {action["title"]} — {action["message"]}'
            )

        elif priority == "HIGH":

            st.warning(
                f'⚠️ {action["title"]} — {action["message"]}'
            )

        elif priority == "MODERATE":

            st.info(
                f'🟡 {action["title"]} — {action["message"]}'
            )

        else:

            st.success(
                f'🟢 {action["title"]} — {action["message"]}'
            )

    # ============================================================
    # AI RISK ADVISOR
    # ============================================================

    st.markdown(
        '<div class="section-title">🤖 THERMOSAFE AI Risk Advisor</div>',
        unsafe_allow_html=True
    )

    ai_result = generate_ai_advice(
        temperature=temperature,
        humidity=humidity,
        wind=wind,
        heat_index=heat_index,
        risk_score=risk_score,
        risk_level=risk_level,
        population=selected_profile
    )

    st.info(
        f'**Current Assessment:** {ai_result["situation"]}'
    )

    st.write(
        f'🔎 **Why:** {ai_result["explanation"]}'
    )

    st.success(
        f'💡 **AI Recommendation:** {ai_result["advice"]}'
    )


    # ============================================================
    # VULNERABLE POPULATION RISK
    # ============================================================

    st.markdown(
        '<div class="section-title">Vulnerable Population Risk</div>',
        unsafe_allow_html=True
    )

    if population_risks:

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