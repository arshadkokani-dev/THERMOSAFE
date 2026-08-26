"""
THERMOSAFE
Heat Forecast & Risk Prediction Engine

This module converts current/forecast weather conditions into
a multi-day thermal-risk outlook.

The MVP uses a lightweight deterministic forecasting approach.
It does NOT require training a large ML model.

Later, this module can be replaced or enhanced with a trained
forecasting model without changing the dashboard architecture.
"""

from __future__ import annotations

from typing import Any

from core.thermal import assess_thermal_risk


# ============================================================
# FORECAST CONFIGURATION
# ============================================================

DEFAULT_FORECAST_DAYS = 5


# ============================================================
# DEMO WEATHER FORECAST
# ============================================================

def generate_demo_weather(
    current_temperature: float = 38.0,
    current_humidity: float = 60.0,
    current_wind: float = 8.0,
    days: int = DEFAULT_FORECAST_DAYS,
) -> list[dict[str, Any]]:
    """
    Generate realistic demo weather conditions for the MVP.

    This allows THERMOSAFE to demonstrate its forecasting
    workflow even when a live weather API is unavailable.

    The values are intentionally kept close to the current
    conditions rather than making unrealistic predictions.
    """

    if days < 1:
        raise ValueError(
            "Forecast must contain at least one day."
        )

    # Small deterministic changes make the demo look like
    # an actual multi-day forecast without random behaviour.
    temperature_changes = [
        0.0,
        1.2,
        2.0,
        -0.8,
        -1.5,
        0.5,
        1.0,
    ]

    humidity_changes = [
        0.0,
        3.0,
        5.0,
        -2.0,
        -4.0,
        2.0,
        1.0,
    ]

    wind_changes = [
        0.0,
        -1.0,
        -2.0,
        2.0,
        3.0,
        1.0,
        -1.0,
    ]

    forecast = []

    for index in range(days):

        temp_change = temperature_changes[
            index % len(temperature_changes)
        ]

        humidity_change = humidity_changes[
            index % len(humidity_changes)
        ]

        wind_change = wind_changes[
            index % len(wind_changes)
        ]

        temperature = max(
            15.0,
            current_temperature + temp_change,
        )

        humidity = max(
            10.0,
            min(
                100.0,
                current_humidity + humidity_change,
            ),
        )

        wind = max(
            0.0,
            current_wind + wind_change,
        )

        forecast.append(
            {
                "day": index + 1,
                "temperature_c": round(
                    temperature,
                    1,
                ),
                "humidity": round(
                    humidity,
                    1,
                ),
                "wind_speed": round(
                    wind,
                    1,
                ),
            }
        )

    return forecast


# ============================================================
# SINGLE DAY FORECAST ASSESSMENT
# ============================================================

def assess_forecast_day(
    weather: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate thermal risk for one forecast day.
    """

    required_fields = [
        "temperature_c",
        "humidity",
        "wind_speed",
    ]

    for field in required_fields:

        if field not in weather:
            raise ValueError(
                f"Missing forecast field: {field}"
            )

    thermal_result = assess_thermal_risk(
        temperature_c=weather["temperature_c"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
    )

    return {
        **weather,
        **thermal_result,
    }


# ============================================================
# COMPLETE FORECAST
# ============================================================

def generate_risk_forecast(
    weather_forecast: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Convert a list of weather predictions into
    THERMOSAFE thermal-risk predictions.
    """

    if not weather_forecast:
        raise ValueError(
            "Weather forecast cannot be empty."
        )

    results = []

    for weather in weather_forecast:

        result = assess_forecast_day(
            weather
        )

        results.append(
            result
        )

    return results


# ============================================================
# FORECAST SUMMARY
# ============================================================

def summarize_forecast(
    forecast: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Produce a high-level summary of the forecast.

    Used later by the dashboard and alert system.
    """

    if not forecast:
        raise ValueError(
            "Forecast cannot be empty."
        )

    highest_risk_day = max(
        forecast,
        key=lambda item: item["risk_score"],
    )

    average_temperature = sum(
        item["temperature_c"]
        for item in forecast
    ) / len(forecast)

    average_risk = sum(
        item["risk_score"]
        for item in forecast
    ) / len(forecast)

    extreme_days = [
        item
        for item in forecast
        if item["risk_level"] == "EXTREME"
    ]

    high_or_extreme_days = [
        item
        for item in forecast
        if item["risk_level"] in [
            "HIGH",
            "EXTREME",
        ]
    ]

    return {
        "days": len(forecast),

        "average_temperature": round(
            average_temperature,
            1,
        ),

        "average_risk_score": round(
            average_risk,
            1,
        ),

        "highest_risk_day": highest_risk_day[
            "day"
        ],

        "highest_risk_score": highest_risk_day[
            "risk_score"
        ],

        "highest_risk_level": highest_risk_day[
            "risk_level"
        ],

        "extreme_days": len(
            extreme_days
        ),

        "high_or_extreme_days": len(
            high_or_extreme_days
        ),

        "alert_required": len(
            high_or_extreme_days
        ) > 0,
    }


# ============================================================
# HEATWAVE DETECTION
# ============================================================

def detect_heatwave(
    forecast: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Detect a potential heatwave pattern.

    This is a prototype rule-based detector.

    A heatwave warning is triggered when several forecast
    days show sustained high thermal risk.
    """

    if not forecast:
        return {
            "detected": False,
            "severity": "NONE",
            "message": "No forecast data available.",
        }

    high_risk_days = [
        item
        for item in forecast
        if item["risk_level"] in [
            "HIGH",
            "EXTREME",
        ]
    ]

    extreme_days = [
        item
        for item in forecast
        if item["risk_level"] == "EXTREME"
    ]

    # Three or more high/extreme-risk days indicate a
    # potential sustained heat event.
    if len(high_risk_days) >= 3:

        if len(extreme_days) >= 2:

            return {
                "detected": True,
                "severity": "EXTREME",
                "message": (
                    "Potential severe heatwave pattern "
                    "detected across the forecast period."
                ),
                "high_risk_days": len(
                    high_risk_days
                ),
                "extreme_days": len(
                    extreme_days
                ),
            }

        return {
            "detected": True,
            "severity": "HIGH",
            "message": (
                "Potential heatwave pattern detected. "
                "Multiple consecutive high-risk days "
                "are forecast."
            ),
            "high_risk_days": len(
                high_risk_days
            ),
            "extreme_days": len(
                extreme_days
            ),
        }

    return {
        "detected": False,
        "severity": "NONE",
        "message": (
            "No sustained heatwave pattern detected "
            "in the current forecast."
        ),
        "high_risk_days": len(
            high_risk_days
        ),
        "extreme_days": len(
            extreme_days
        ),
    }


# ============================================================
# COMPLETE FORECAST REPORT
# ============================================================

def build_forecast_report(
    current_temperature: float = 38.0,
    current_humidity: float = 60.0,
    current_wind: float = 8.0,
    days: int = DEFAULT_FORECAST_DAYS,
) -> dict[str, Any]:
    """
    Build the complete THERMOSAFE forecast report.

    This will eventually be called by the dashboard.
    """

    weather_forecast = generate_demo_weather(
        current_temperature=current_temperature,
        current_humidity=current_humidity,
        current_wind=current_wind,
        days=days,
    )

    risk_forecast = generate_risk_forecast(
        weather_forecast
    )

    summary = summarize_forecast(
        risk_forecast
    )

    heatwave = detect_heatwave(
        risk_forecast
    )

    return {
        "forecast": risk_forecast,
        "summary": summary,
        "heatwave": heatwave,
    }


# ============================================================
# DISPLAY HELPER
# ============================================================

def print_forecast_report(
    report: dict[str, Any],
) -> None:
    """
    Print a clean forecast report for terminal testing.
    """

    print()
    print("=" * 70)
    print("THERMOSAFE — HEAT RISK FORECAST")
    print("=" * 70)

    print()

    for item in report["forecast"]:

        print(
            f"Day {item['day']}: "
            f"{item['temperature_c']}°C | "
            f"{item['humidity']}% humidity | "
            f"Risk {item['risk_score']}/100 | "
            f"{item['risk_level']}"
        )

    print()
    print("-" * 70)

    summary = report["summary"]

    print(
        f"Average Temperature: "
        f"{summary['average_temperature']}°C"
    )

    print(
        f"Average Risk Score: "
        f"{summary['average_risk_score']}/100"
    )

    print(
        f"Highest Risk Day: "
        f"Day {summary['highest_risk_day']}"
    )

    print(
        f"Highest Risk: "
        f"{summary['highest_risk_level']}"
    )

    print(
        f"High/Extreme Risk Days: "
        f"{summary['high_or_extreme_days']}"
    )

    print()

    heatwave = report["heatwave"]

    if heatwave["detected"]:

        print(
            f"HEATWAVE ALERT: "
            f"{heatwave['severity']}"
        )

        print(
            heatwave["message"]
        )

    else:

        print(
            "Heatwave Status: "
            "No sustained heatwave detected."
        )

    print()
    print("=" * 70)


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    print(
        "THERMOSAFE Forecast Engine Test"
    )

    report = build_forecast_report(
        current_temperature=39.0,
        current_humidity=68.0,
        current_wind=8.0,
        days=5,
    )

    print_forecast_report(
        report
    )

    print()
    print(
        "Forecast engine test PASSED."
    )