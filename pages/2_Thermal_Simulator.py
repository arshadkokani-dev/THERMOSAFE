import streamlit as st

from ui.simulator import show_simulator


st.set_page_config(
    page_title="THERMOSAFE Simulator",
    page_icon="🧪",
    layout="wide",
)

st.title("Thermal Risk Simulator")

st.caption(
    "Simulate changing environmental conditions "
    "and evaluate human thermal risk."
)

st.divider()


# --------------------------------------------------
# CURRENT CONDITIONS
# --------------------------------------------------

current_data = {
    "temperature": st.session_state.get(
        "temperature",
        30.0,
    ),

    "humidity": st.session_state.get(
        "humidity",
        60.0,
    ),

    "wind_speed": st.session_state.get(
        "wind_speed",
        5.0,
    ),
}


show_simulator(current_data)