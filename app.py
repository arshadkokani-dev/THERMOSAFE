import streamlit as st

st.set_page_config(
    page_title="THERMOSAFE",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 THERMOSAFE")
st.subheader("AI-Powered Heatwave Early Warning & Human Thermal Risk Intelligence")

st.write(
    "Detect heat danger, assess human thermal risk, "
    "and recommend action before heat becomes a crisis."
)

st.success("THERMOSAFE system initialized successfully.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Temperature", "-- °C")

with col2:
    st.metric("Humidity", "-- %")

with col3:
    st.metric("Risk Level", "Loading...")