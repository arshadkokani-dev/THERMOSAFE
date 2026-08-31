import streamlit as st
import pandas as pd


def show_risk_map(risk_locations):

    st.markdown(
        '<div class="section-title">🗺️ THERMOSAFE Risk Map</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Compare thermal risk across monitored locations."
    )

    if not risk_locations:
        st.info("No location risk data available.")
        return

    df = pd.DataFrame(risk_locations)

    # -----------------------------
    # MAP
    # -----------------------------

    st.map(
        df,
        latitude="latitude",
        longitude="longitude",
        zoom=4,
    )

    # -----------------------------
    # LOCATION RISK OVERVIEW
    # -----------------------------

    st.subheader("Location Risk Overview")

    display_df = df[
        [
            "location",
            "temperature",
            "humidity",
            "risk_score",
            "risk_level",
        ]
    ].copy()

    display_df.columns = [
        "Location",
        "Temperature (°C)",
        "Humidity (%)",
        "Risk Score",
        "Risk Level",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )