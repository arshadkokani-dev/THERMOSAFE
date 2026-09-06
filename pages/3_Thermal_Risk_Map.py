import streamlit as st
import pandas as pd

from services.weather import get_location_weather
from core.thermal import assess_thermal_risk
from ui.risk_map import show_risk_map
from ui.theme import apply_theme


# =========================================================
# THERMOSAFE — THERMAL RISK MAP
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
                Thermal Risk Map
            </div>

            <div class="analytics-section-subtitle">
                Spatial thermal-risk intelligence across monitored locations.
            </div>

        </div>
    </div>
    """
)


# =========================================================
# LOAD LOCATIONS
# =========================================================

try:

    locations_df = pd.read_csv(
        "data/locations.csv"
    )

except Exception as error:

    st.error(
        f"Unable to load monitored locations: {error}"
    )

    st.stop()


# =========================================================
# COLLECT RISK DATA
# =========================================================

risk_locations = []
failed_locations = []


for _, row in locations_df.iterrows():

    city = str(row["location"]).strip()

    try:

        location_weather = get_location_weather(city)

        location_thermal = assess_thermal_risk(
            temperature_c=location_weather["temperature"],
            humidity=location_weather["humidity"],
            wind_speed=location_weather["wind"],
        )

        risk_locations.append(
            {
                "location": city,

                "latitude": float(
                    row["latitude"]
                ),

                "longitude": float(
                    row["longitude"]
                ),

                "temperature": float(
                    location_weather["temperature"]
                ),

                "humidity": float(
                    location_weather["humidity"]
                ),

                "wind": float(
                    location_weather["wind"]
                ),

                "risk_score": float(
                    location_thermal["risk_score"]
                ),

                "risk_level": location_thermal[
                    "risk_level"
                ],
            }
        )

    except Exception:
        failed_locations.append(city)

# =========================================================
# AVAILABILITY STATUS
# =========================================================

if failed_locations:

    st.warning(
        f"{len(failed_locations)} monitored location(s) "
        "could not be updated right now: "
        + ", ".join(failed_locations)
    )

# =========================================================
# RENDER MAP
# =========================================================

if risk_locations:

    show_risk_map(
        risk_locations
    )

else:

    st.warning(
        "No location risk data is currently available."
    )