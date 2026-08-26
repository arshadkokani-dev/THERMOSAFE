import streamlit as st

from services.weather import get_location_weather
from core.thermal import assess_thermal_risk
from ui.dashboard import show_dashboard
from forecast.predictor import build_forecast_report
from ui.forecast_view import show_forecast


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="THERMOSAFE",
    page_icon="🌡️",
    layout="wide",
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("THERMOSAFE")
st.sidebar.caption(
    "Human Thermal Risk Intelligence"
)

location = st.sidebar.text_input(
    "Monitoring location",
    value="Pune",
)

analyze = st.sidebar.button(
    "Analyze Conditions"
)


# --------------------------------------------------
# GET WEATHER DATA
# --------------------------------------------------

if analyze or "weather" not in st.session_state:

    try:
        with st.spinner(
            "Fetching environmental conditions..."
        ):
            st.session_state.weather = (
                get_location_weather(location)
            )

    except Exception as error:

        st.error(
            f"Unable to retrieve weather data: {error}"
        )

        st.stop()


weather = st.session_state.weather


# --------------------------------------------------
# CURRENT CONDITIONS
# --------------------------------------------------

temperature = weather["temperature"]
humidity = weather["humidity"]
wind_speed = weather["wind"]

location_name = weather["location"]


# --------------------------------------------------
# THERMAL RISK ENGINE
# --------------------------------------------------

thermal = assess_thermal_risk(
    temperature_c=temperature,
    humidity=humidity,
    wind_speed=wind_speed,
)


# --------------------------------------------------
# DATA FOR DASHBOARD
# --------------------------------------------------

dashboard_data = {
    "location": location_name,

    "temperature": temperature,

    "humidity": humidity,

    "heat_index": thermal["heat_index"],

    "wind_speed": wind_speed,

    "risk_score": thermal["risk_score"],

    "risk_level": thermal["risk_level"],

    "risk_message": thermal["warning"],
}


# --------------------------------------------------
# RENDER DASHBOARD
# --------------------------------------------------

show_dashboard(dashboard_data)

forecast_report = build_forecast_report(
    current_temperature=dashboard_data["temperature"],
    current_humidity=dashboard_data["humidity"],
    current_wind=dashboard_data["wind_speed"],
    days=5,
)

show_forecast(forecast_report)