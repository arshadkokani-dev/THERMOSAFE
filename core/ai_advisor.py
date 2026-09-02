def generate_ai_advice(
    temperature,
    humidity,
    wind,
    heat_index,
    risk_score,
    risk_level,
    population
):

    if risk_level == "EXTREME":

        situation = (
            f"Extreme thermal stress is currently detected for "
            f"{population.lower()}."
        )

        advice = (
            "Avoid prolonged heat exposure immediately. "
            "Move to a cool or shaded environment, maintain hydration, "
            "and prioritize protection of vulnerable individuals."
        )

    elif risk_level == "HIGH":

        situation = (
            f"High thermal stress is currently detected for "
            f"{population.lower()}."
        )

        advice = (
            "Reduce prolonged outdoor exposure, take frequent cooling "
            "breaks, and maintain regular hydration."
        )

    elif risk_level == "MODERATE":

        situation = (
            f"Moderate thermal stress is currently detected for "
            f"{population.lower()}."
        )

        advice = (
            "Maintain hydration, take cooling breaks during prolonged "
            "outdoor activity, and continue monitoring conditions."
        )

    else:

        situation = (
            f"Current thermal conditions are relatively safe for "
            f"{population.lower()}."
        )

        advice = (
            "Normal activity can continue while maintaining normal "
            "hydration and monitoring changing conditions."
        )

    # Explain the environmental drivers

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
            f"limited cooling from wind ({wind:.1f} km/h)"
        )

    if factors:

        explanation = (
            "The main environmental contributors are "
            + ", ".join(factors)
            + "."
        )

    else:

        explanation = (
            "Current temperature, humidity, and wind conditions "
            "are not showing major environmental stress factors."
        )

    return {
        "situation": situation,
        "explanation": explanation,
        "advice": advice,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }