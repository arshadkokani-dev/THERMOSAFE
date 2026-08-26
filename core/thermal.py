"""
THERMOSAFE
Thermal Risk Intelligence Engine

This module converts environmental conditions into a
human-readable heat-risk assessment.

Inputs:
    - Temperature
    - Relative humidity
    - Wind speed
    - Optional precipitation

Outputs:
    - Heat index
    - Apparent temperature
    - Risk score
    - Risk level
    - Health interpretation
    - Recommended actions
    - Warning message

No Streamlit/UI code belongs in this file.
"""

from __future__ import annotations

from typing import Any


# ============================================================
# RISK LEVELS
# ============================================================

RISK_LEVELS = {
    "LOW": {
        "score": 0,
        "label": "Low Risk",
        "description": (
            "Heat conditions are currently within a generally "
            "comfortable range for most people."
        ),
    },
    "MODERATE": {
        "score": 1,
        "label": "Moderate Risk",
        "description": (
            "Heat stress may affect vulnerable people and "
            "people exposed to outdoor activity for long periods."
        ),
    },
    "HIGH": {
        "score": 2,
        "label": "High Risk",
        "description": (
            "Heat exposure may cause significant heat stress. "
            "Outdoor activity should be reduced during peak heat."
        ),
    },
    "EXTREME": {
        "score": 3,
        "label": "Extreme Risk",
        "description": (
            "Dangerous heat conditions are present. "
            "Immediate protective measures are recommended."
        ),
    },
}


# ============================================================
# VALIDATION
# ============================================================

def _validate_inputs(
    temperature: float,
    humidity: float,
    wind_speed: float = 0.0,
) -> None:
    """
    Validate environmental inputs.
    """

    if not isinstance(temperature, (int, float)):
        raise TypeError("Temperature must be numeric.")

    if not isinstance(humidity, (int, float)):
        raise TypeError("Humidity must be numeric.")

    if not isinstance(wind_speed, (int, float)):
        raise TypeError("Wind speed must be numeric.")

    if not -50 <= temperature <= 70:
        raise ValueError(
            "Temperature must be between -50°C and 70°C."
        )

    if not 0 <= humidity <= 100:
        raise ValueError(
            "Humidity must be between 0% and 100%."
        )

    if wind_speed < 0:
        raise ValueError(
            "Wind speed cannot be negative."
        )


# ============================================================
# HEAT INDEX
# ============================================================

def calculate_heat_index(
    temperature_c: float,
    humidity: float,
) -> float:
    """
    Calculate approximate heat index.

    The calculation uses the commonly used Rothfusz
    regression when conditions are appropriate.

    Returns:
        Heat index in °C.
    """

    _validate_inputs(
        temperature_c,
        humidity,
    )

    # Convert Celsius → Fahrenheit
    temperature_f = (
        temperature_c * 9 / 5
    ) + 32

    # For relatively mild conditions, heat index is
    # approximately the actual temperature.
    if temperature_f < 80:
        return round(temperature_c, 1)

    # Rothfusz regression
    t = temperature_f
    r = humidity

    heat_index_f = (
        -42.379
        + 2.04901523 * t
        + 10.14333127 * r
        - 0.22475541 * t * r
        - 0.00683783 * t * t
        - 0.05481717 * r * r
        + 0.00122874 * t * t * r
        + 0.00085282 * t * r * r
        - 0.00000199 * t * t * r * r
    )

    # Convert Fahrenheit → Celsius
    heat_index_c = (
        (heat_index_f - 32) * 5 / 9
    )

    return round(heat_index_c, 1)


# ============================================================
# APPARENT TEMPERATURE
# ============================================================

def calculate_apparent_temperature(
    temperature_c: float,
    humidity: float,
    wind_speed: float = 0.0,
) -> float:
    """
    Estimate apparent temperature.

    This provides a practical "feels like" value for
    the THERMOSAFE dashboard.

    Returns:
        Apparent temperature in °C.
    """

    _validate_inputs(
        temperature_c,
        humidity,
        wind_speed,
    )

    # Humidity contribution
    humidity_effect = (
        0.05 * (humidity - 40)
    )

    # Wind provides some cooling.
    # We intentionally keep the effect conservative.
    wind_effect = min(
        wind_speed * 0.08,
        3.0,
    )

    apparent = (
        temperature_c
        + humidity_effect
        - wind_effect
    )

    return round(apparent, 1)


# ============================================================
# THERMAL STRESS SCORE
# ============================================================

def calculate_risk_score(
    temperature_c: float,
    humidity: float,
    wind_speed: float = 0.0,
) -> int:
    """
    Convert environmental conditions into a
    THERMOSAFE risk score from 0–100.

    The score is NOT a medical diagnosis.

    It is an environmental risk indicator designed
    for the prototype.
    """

    _validate_inputs(
        temperature_c,
        humidity,
        wind_speed,
    )

    heat_index = calculate_heat_index(
        temperature_c,
        humidity,
    )

    apparent_temperature = calculate_apparent_temperature(
        temperature_c,
        humidity,
        wind_speed,
    )

    # Start with actual temperature contribution.
    score = 0.0

    # --------------------------------------------------------
    # Temperature contribution
    # --------------------------------------------------------

    if temperature_c < 30:
        score += 10

    elif temperature_c < 35:
        score += 25

    elif temperature_c < 40:
        score += 45

    elif temperature_c < 45:
        score += 65

    else:
        score += 80

    # --------------------------------------------------------
    # Humidity contribution
    # --------------------------------------------------------

    if humidity < 40:
        score += 0

    elif humidity < 60:
        score += 5

    elif humidity < 75:
        score += 10

    elif humidity < 85:
        score += 15

    else:
        score += 20

    # --------------------------------------------------------
    # Heat index contribution
    # --------------------------------------------------------

    if heat_index >= 32:
        score += 5

    if heat_index >= 38:
        score += 8

    if heat_index >= 41:
        score += 10

    # --------------------------------------------------------
    # Apparent temperature contribution
    # --------------------------------------------------------

    if apparent_temperature >= 35:
        score += 5

    if apparent_temperature >= 40:
        score += 8

    if apparent_temperature >= 45:
        score += 10

    # --------------------------------------------------------
    # Wind cooling adjustment
    # --------------------------------------------------------

    if wind_speed >= 20:
        score -= 5

    elif wind_speed >= 10:
        score -= 2

    score = max(
        0,
        min(
            int(round(score)),
            100,
        ),
    )

    return score


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(
    score: int,
) -> str:
    """
    Convert a 0–100 risk score into a THERMOSAFE
    risk category.
    """

    if score < 25:
        return "LOW"

    if score < 50:
        return "MODERATE"

    if score < 75:
        return "HIGH"

    return "EXTREME"


# ============================================================
# RISK DESCRIPTION
# ============================================================

def get_risk_description(
    risk_level: str,
) -> str:
    """
    Return the explanation associated with a risk level.
    """

    risk_level = risk_level.upper()

    if risk_level not in RISK_LEVELS:
        raise ValueError(
            f"Unknown risk level: {risk_level}"
        )

    return RISK_LEVELS[risk_level]["description"]


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

def get_recommendations(
    risk_level: str,
) -> list[str]:
    """
    Return practical protective actions based on
    environmental risk.
    """

    risk_level = risk_level.upper()

    recommendations = {
        "LOW": [
            "Stay hydrated throughout the day.",
            "Normal outdoor activity is generally reasonable.",
            "Take breaks if exposed to prolonged heat.",
        ],

        "MODERATE": [
            "Increase water intake.",
            "Avoid prolonged exposure during peak afternoon heat.",
            "Take regular cooling breaks.",
            "Monitor children, older adults and vulnerable people.",
        ],

        "HIGH": [
            "Reduce strenuous outdoor activity.",
            "Avoid unnecessary exposure during peak heat.",
            "Drink water regularly and use cooling measures.",
            "Check on elderly people, children and outdoor workers.",
            "Seek a cooler indoor environment when possible.",
        ],

        "EXTREME": [
            "Avoid unnecessary outdoor exposure.",
            "Move to a cool or air-conditioned environment.",
            "Increase hydration and use active cooling.",
            "Do not perform strenuous activity in direct heat.",
            "Check on vulnerable people and outdoor workers.",
            "Seek medical help if serious heat-illness symptoms occur.",
        ],
    }

    return recommendations.get(
        risk_level,
        recommendations["LOW"],
    )


# ============================================================
# WARNING MESSAGE
# ============================================================

def get_warning_message(
    risk_level: str,
) -> str:
    """
    Generate the main warning displayed by the UI.
    """

    messages = {
        "LOW": (
            "Current conditions indicate a relatively "
            "low thermal risk."
        ),

        "MODERATE": (
            "Moderate thermal stress detected. "
            "Vulnerable groups should take precautions."
        ),

        "HIGH": (
            "High thermal stress detected. "
            "Reduce outdoor exposure and increase cooling measures."
        ),

        "EXTREME": (
            "EXTREME HEAT RISK detected. "
            "Immediate protective action is recommended."
        ),
    }

    return messages.get(
        risk_level,
        messages["LOW"],
    )


# ============================================================
# COMPLETE THERMAL ASSESSMENT
# ============================================================

def assess_thermal_risk(
    temperature_c: float,
    humidity: float,
    wind_speed: float = 0.0,
    precipitation: float = 0.0,
) -> dict[str, Any]:
    """
    Main THERMOSAFE thermal intelligence function.

    This is the function the dashboard, forecast,
    simulator and alert system will eventually use.

    Returns a complete structured assessment.
    """

    _validate_inputs(
        temperature_c,
        humidity,
        wind_speed,
    )

    heat_index = calculate_heat_index(
        temperature_c,
        humidity,
    )

    apparent_temperature = calculate_apparent_temperature(
        temperature_c,
        humidity,
        wind_speed,
    )

    risk_score = calculate_risk_score(
        temperature_c,
        humidity,
        wind_speed,
    )

    risk_level = get_risk_level(
        risk_score
    )

    return {
        "temperature_c": round(
            temperature_c,
            1,
        ),

        "humidity": round(
            humidity,
            1,
        ),

        "wind_speed": round(
            wind_speed,
            1,
        ),

        "precipitation": round(
            precipitation,
            1,
        ),

        "heat_index": heat_index,

        "apparent_temperature": (
            apparent_temperature
        ),

        "risk_score": risk_score,

        "risk_level": risk_level,

        "risk_label": RISK_LEVELS[
            risk_level
        ]["label"],

        "description": get_risk_description(
            risk_level
        ),

        "warning": get_warning_message(
            risk_level
        ),

        "recommendations": get_recommendations(
            risk_level
        ),
    }


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    print("THERMOSAFE Thermal Engine Test")
    print("=" * 45)

    # Test scenario representing a hot,
    # humid Indian summer afternoon.
    result = assess_thermal_risk(
        temperature_c=39.0,
        humidity=68.0,
        wind_speed=8.0,
    )

    print(
        f"Temperature: "
        f"{result['temperature_c']} °C"
    )

    print(
        f"Humidity: "
        f"{result['humidity']} %"
    )

    print(
        f"Wind: "
        f"{result['wind_speed']} km/h"
    )

    print(
        f"Heat Index: "
        f"{result['heat_index']} °C"
    )

    print(
        f"Feels Like: "
        f"{result['apparent_temperature']} °C"
    )

    print(
        f"Risk Score: "
        f"{result['risk_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{result['risk_label']}"
    )

    print()
    print(
        f"Warning: "
        f"{result['warning']}"
    )

    print()
    print("Recommendations:")

    for recommendation in result["recommendations"]:
        print(
            f"  - {recommendation}"
        )

    print()
    print("Thermal engine test PASSED.")