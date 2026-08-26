"""
THERMOSAFE
Human Vulnerability Risk Engine

Adjusts the environmental thermal-risk score
for different population profiles.
"""

from __future__ import annotations

from typing import Any


# ============================================================
# VULNERABILITY PROFILES
# ============================================================

POPULATION_PROFILES = {
    "General Adult": {
        "multiplier": 1.00,
        "reason": "Baseline risk for a healthy adult.",
    },

    "Outdoor Worker": {
        "multiplier": 1.25,
        "reason": "Prolonged outdoor exposure can increase thermal stress.",
    },

    "Elderly": {
        "multiplier": 1.30,
        "reason": "Older adults can be more vulnerable to heat stress.",
    },

    "Child": {
        "multiplier": 1.20,
        "reason": "Children can be more sensitive to thermal conditions.",
    },

    "Athlete": {
        "multiplier": 1.15,
        "reason": "Physical exertion can increase heat generation and dehydration risk.",
    },
}


# ============================================================
# SINGLE PROFILE ASSESSMENT
# ============================================================

def assess_population_risk(
    base_risk_score: float,
    profile: str,
) -> dict[str, Any]:

    if profile not in POPULATION_PROFILES:
        raise ValueError(
            f"Unknown population profile: {profile}"
        )

    profile_data = POPULATION_PROFILES[profile]

    adjusted_score = round(
        base_risk_score * profile_data["multiplier"]
    )

    adjusted_score = min(
        100,
        adjusted_score,
    )

    if adjusted_score >= 75:
        risk_level = "EXTREME"

    elif adjusted_score >= 50:
        risk_level = "HIGH"

    elif adjusted_score >= 25:
        risk_level = "MODERATE"

    else:
        risk_level = "LOW"

    return {
        "profile": profile,
        "base_score": base_risk_score,
        "adjusted_score": adjusted_score,
        "risk_level": risk_level,
        "reason": profile_data["reason"],
    }


# ============================================================
# ALL POPULATION PROFILES
# ============================================================

def assess_all_populations(
    base_risk_score: float,
) -> list[dict[str, Any]]:

    return [
        assess_population_risk(
            base_risk_score,
            profile,
        )
        for profile in POPULATION_PROFILES
    ]