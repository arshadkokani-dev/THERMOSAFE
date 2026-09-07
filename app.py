import streamlit as st

from services.weather import get_location_weather
from core.thermal import assess_thermal_risk
from ui.dashboard import show_dashboard
from core.risk import assess_all_populations
from forecast.predictor import build_forecast_report
from ui.theme import apply_theme


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="THERMOSAFE",
    page_icon="🌡️",
    layout="wide",
)


# =========================================================
# THEME
# =========================================================

st.html(apply_theme())


# =========================================================
# SIDEBAR BRAND
# =========================================================

st.sidebar.html(
    """
    <div class="thermosafe-sidebar-brand">

        <div class="thermosafe-sidebar-logo">
            THERMOSAFE
        </div>

        <div class="thermosafe-sidebar-tagline">
            Human Thermal Risk Intelligence
        </div>

    </div>
    """
)

# =========================================================
# PAGE DEFINITIONS
# =========================================================

def command_center_page():
    show_dashboard(dashboard_data)


command_center = st.Page(
    command_center_page,
    title="Command Center",
    icon=":material/home:",
    default=True,
)

forecast_page = st.Page(
    "pages/2_Forecast_Analytics.py",
    title="Forecast Analytics",
    icon=":material/analytics:",
)

risk_map_page = st.Page(
    "pages/3_Thermal_Risk_Map.py",
    title="Thermal Risk Map",
    icon=":material/map:",
)

simulation_page = st.Page(
    "pages/4_Simulation_Lab.py",
    title="Simulation Lab",
    icon=":material/science:",
)

risk_intelligence_page = st.Page(
    "pages/5_Risk_Intelligence.py",
    title="Risk Intelligence",
    icon=":material/psychology:",
)


# =========================================================
# NAVIGATION
# =========================================================

pg = st.navigation(
    [
        command_center,
        forecast_page,
        risk_map_page,
        simulation_page,
        risk_intelligence_page,
    ],
    position="hidden",
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.html(
    """
    <div class="sidebar-section-label">
        Navigation
    </div>
    """
)


st.sidebar.page_link(
    command_center,
    label="Command Center",
    icon=":material/home:",
)

st.sidebar.page_link(
    forecast_page,
    label="Forecast Analytics",
    icon=":material/analytics:",
)

st.sidebar.page_link(
    risk_map_page,
    label="Thermal Risk Map",
    icon=":material/map:",
)

st.sidebar.page_link(
    simulation_page,
    label="Simulation Lab",
    icon=":material/science:",
)

st.sidebar.page_link(
    risk_intelligence_page,
    label="Risk Intelligence",
    icon=":material/psychology:",
)


# =========================================================
# ENVIRONMENT
# =========================================================

st.sidebar.html(
    """
    <div class="sidebar-section-label thermosafe-environment-label">
        Environment
    </div>
    """
)


location = st.sidebar.text_input(
    "Monitoring location",
    value="Pune",
    label_visibility="collapsed",
)


analyze = st.sidebar.button(
    "Analyze Conditions",
    type="primary",
    use_container_width=True,
)


# =========================================================
# GET WEATHER DATA
# =========================================================

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


# =========================================================
# CURRENT CONDITIONS
# =========================================================

temperature = weather["temperature"]
humidity = weather["humidity"]
wind_speed = weather["wind"]

location_name = weather["location"]


# =========================================================
# THERMAL RISK ENGINE
# =========================================================

thermal = assess_thermal_risk(
    temperature_c=temperature,
    humidity=humidity,
    wind_speed=wind_speed,
)


st.session_state["risk_score"] = (
    thermal["risk_score"]
)

st.session_state["risk_level"] = (
    thermal["risk_level"]
)


# =========================================================
# DASHBOARD DATA
# =========================================================

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


# =========================================================
# POPULATION RISK ANALYSIS
# =========================================================

population_risks = assess_all_populations(
    dashboard_data["risk_score"]
)

dashboard_data["population_risks"] = (
    population_risks
)


# =========================================================
# SAVE SHARED DATA
# =========================================================

st.session_state["dashboard_data"] = (
    dashboard_data
)


# =========================================================
# FORECAST REPORT
# =========================================================

forecast_report = build_forecast_report(
    current_temperature=dashboard_data["temperature"],
    current_humidity=dashboard_data["humidity"],
    current_wind=dashboard_data["wind_speed"],
    days=5,
)

st.session_state["forecast_report"] = (
    forecast_report
)


# =========================================================
# SIDEBAR FOOTER
# =========================================================

st.sidebar.html(
    """
    <div class="thermosafe-sidebar-footer">

        <div class="thermosafe-footer-line"></div>

        <div class="thermosafe-footer-title">
            Building a Cooler, Safer Tomorrow
        </div>

        <div class="thermosafe-footer-author">
            By <strong>Arshad Kokani</strong>
        </div>

    </div>
    """
)


# =========================================================
# RUN SELECTED PAGE
# =========================================================

pg.run()