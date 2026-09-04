from services.llm import generate_thermal_advice


def generate_ai_advice(
    temperature,
    humidity,
    wind,
    heat_index,
    risk_score,
    risk_level,
    population,
):
    """
    Generate the THERMOSAFE AI assessment.

    Environmental calculations come from the thermal engine.
    Groq interprets those verified results and generates the
    human-readable advisory.
    """

    factors = []

    if temperature >= 35:
        factors.append(
            f"high temperature ({temperature:.1f}°C)"
        )
    elif temperature >= 30:
        factors.append(
            f"elevated temperature ({temperature:.1f}°C)"
        )

    if humidity >= 70:
        factors.append(
            f"high humidity ({humidity:.0f}%)"
        )
    elif humidity >= 60:
        factors.append(
            f"elevated humidity ({humidity:.0f}%)"
        )

    if wind <= 5:
        factors.append(
            f"limited wind cooling ({wind:.1f} km/h)"
        )

    if heat_index > temperature + 2:
        factors.append(
            f"elevated apparent heat ({heat_index:.1f}°C)"
        )

    if factors:
        explanation = (
            "The main environmental contributors are "
            + ", ".join(factors)
            + "."
        )
    else:
        explanation = (
            "Current environmental conditions are not "
            "showing major thermal stress factors."
        )

    try:
        advice = generate_thermal_advice(
            temperature=temperature,
            humidity=humidity,
            wind=wind,
            heat_index=heat_index,
            risk_score=risk_score,
            risk_level=risk_level,
            population=population,
        )

    except Exception:
        advice = (
            "AI advisory is temporarily unavailable. "
            "The displayed thermal risk assessment is still "
            "based on the THERMOSAFE environmental risk engine."
        )

    return {
        "situation": (
            f"{risk_level.title()} thermal conditions "
            f"detected for {population.lower()}."
        ),
        "explanation": explanation,
        "advice": advice,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }