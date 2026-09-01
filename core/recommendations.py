def generate_safety_plan(
    risk_score,
    risk_level,
    population="General Adult"
):

    actions = []

    # -----------------------------
    # RISK-BASED ACTIONS
    # -----------------------------

    if risk_score >= 75:

        actions.append({
            "title": "Immediate Cooling",
            "message": "Move to a cool or shaded environment immediately.",
            "priority": "CRITICAL"
        })

        actions.append({
            "title": "Hydration",
            "message": "Increase fluid intake and avoid prolonged heat exposure.",
            "priority": "CRITICAL"
        })

        actions.append({
            "title": "Outdoor Exposure",
            "message": "Avoid prolonged outdoor activity until conditions improve.",
            "priority": "CRITICAL"
        })

    elif risk_score >= 50:

        actions.append({
            "title": "Cooling Breaks",
            "message": "Take frequent cooling breaks and avoid unnecessary heat exposure.",
            "priority": "HIGH"
        })

        actions.append({
            "title": "Hydration",
            "message": "Increase hydration and drink fluids regularly.",
            "priority": "HIGH"
        })

        actions.append({
            "title": "Outdoor Activity",
            "message": "Limit prolonged outdoor activity, especially during peak heat.",
            "priority": "HIGH"
        })

    elif risk_score >= 30:

        actions.append({
            "title": "Hydration",
            "message": "Maintain good hydration throughout the day.",
            "priority": "MODERATE"
        })

        actions.append({
            "title": "Monitor Conditions",
            "message": "Continue monitoring thermal conditions as risk may increase.",
            "priority": "MODERATE"
        })

        actions.append({
            "title": "Cooling",
            "message": "Take cooling breaks when spending extended time outdoors.",
            "priority": "MODERATE"
        })

    else:

        actions.append({
            "title": "Normal Activity",
            "message": "Current thermal conditions are relatively safe.",
            "priority": "LOW"
        })

        actions.append({
            "title": "Hydration",
            "message": "Continue normal hydration.",
            "priority": "LOW"
        })

    # -----------------------------
    # POPULATION-SPECIFIC ACTIONS
    # -----------------------------

    if population in [
        "Elderly",
        "Children",
        "Outdoor Workers"
    ]:

        actions.append({
            "title": "Vulnerable Population",
            "message": (
                f"Extra monitoring is recommended for {population.lower()} "
                "during elevated thermal risk."
            ),
            "priority": "HIGH"
        })

    return actions