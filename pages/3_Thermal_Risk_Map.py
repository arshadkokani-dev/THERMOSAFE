import streamlit as st
import pandas as pd

from services.weather import get_location_weather
from core.thermal import assess_thermal_risk
from ui.risk_map import show_risk_map


st.title("Thermal Risk Map")

st.caption(
    "Spatial thermal-risk intelligence across monitored locations."
)


st.subheader("Regional Risk Overview")


try:
    locations_df = pd.read_csv(
        "data/locations.csv"
    )

    risk_locations = []

    for _, row in locations_df.iterrows():

        try:
            city = row["location"]

            location_weather = get_location_weather(
                city
            )

            location_thermal = assess_thermal_risk(
                temperature_c=location_weather["temperature"],
                humidity=location_weather["humidity"],
                wind_speed=location_weather["wind"],
            )

            risk_locations.append(
                {
                    "location": city,
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "temperature": location_weather["temperature"],
                    "humidity": location_weather["humidity"],
                    "risk_score": location_thermal["risk_score"],
                    "risk_level": location_thermal["risk_level"],
                }
            )

        except Exception:
            continue

    if risk_locations:
        show_risk_map(risk_locations)

    else:
        st.warning(
            "No location risk data is currently available."
        )

except Exception as error:

    st.error(
        f"Unable to load risk map data: {error}"
    )