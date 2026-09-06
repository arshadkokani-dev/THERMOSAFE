import streamlit as st

from ui.simulator import show_simulator
from ui.theme import apply_theme


# =========================================================
# THERMOSAFE — SIMULATION LAB
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
                Simulation Lab
            </div>

            <div class="analytics-section-subtitle">
                Explore how changing environmental conditions
                could affect human thermal risk.
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


if dashboard_data:

    current_data = {
        "temperature": float(
            dashboard_data.get(
                "temperature",
                30.0,
            )
        ),

        "humidity": float(
            dashboard_data.get(
                "humidity",
                60.0,
            )
        ),

        "wind_speed": float(
            dashboard_data.get(
                "wind_speed",
                5.0,
            )
        ),

        "location": dashboard_data.get(
            "location",
            "Current Location",
        ),
    }

else:

    current_data = {
        "temperature": float(
            st.session_state.get(
                "temperature",
                30.0,
            )
        ),

        "humidity": float(
            st.session_state.get(
                "humidity",
                60.0,
            )
        ),

        "wind_speed": float(
            st.session_state.get(
                "wind_speed",
                5.0,
            )
        ),

        "location": "Default Scenario",
    }


# =========================================================
# SIMULATOR
# =========================================================

show_simulator(
    current_data
)