import pandas as pd
import streamlit as st

from streamlit_folium import st_folium

from maps.heatmap import create_risk_map


def show_risk_map(risk_locations):

    if not risk_locations:
        st.info(
            "No location risk data available."
        )
        return

    df = pd.DataFrame(
        risk_locations
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    location_count = len(df)

    highest_risk_row = df.loc[
        df["risk_score"].idxmax()
    ]

    highest_location = (
        highest_risk_row["location"]
    )

    highest_score = float(
        highest_risk_row["risk_score"]
    )

    highest_level = str(
        highest_risk_row["risk_level"]
    ).upper()

    average_risk = float(
        df["risk_score"].mean()
    )

    if highest_score >= 75:
        status = "EXTREME"

    elif highest_score >= 50:
        status = "HIGH"

    elif highest_score >= 30:
        status = "MODERATE"

    else:
        status = "LOW"


    st.html(
        """
        <div class="analytics-section">
            Regional Risk Overview
        </div>

        <div class="analytics-section-subtitle">
            Live thermal-risk comparison across monitored locations.
        </div>
        """
    )


    summary = [
        (
            "LOCATIONS MONITORED",
            str(location_count)
        ),
        (
            "HIGHEST RISK",
            highest_location
        ),
        (
            "PEAK RISK",
            f"{highest_score:.0f}/100"
        ),
        (
            "REGIONAL STATUS",
            status
        ),
    ]


    summary_cols = st.columns(4)

    for col, (label, value) in zip(
        summary_cols,
        summary
    ):

        with col:

            st.html(
                f"""
                <div class="analytics-metric">

                    <div class="analytics-label">
                        {label}
                    </div>

                    <div class="analytics-value">
                        {value}
                    </div>

                </div>
                """
            )


    # =====================================================
    # MAP
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Spatial Thermal Risk
        </div>

        <div class="analytics-section-subtitle">
            Select a location to inspect its current thermal conditions.
        </div>
        """
    )


    thermal_map = create_risk_map(
        risk_locations
    )

    if thermal_map:

        st_folium(
            thermal_map,
            use_container_width=True,
            height=560,
            returned_objects=[],
        )


    # =====================================================
    # LOCATION RANKING
    # =====================================================

    st.html(
        """
        <div class="analytics-section">
            Location Risk Overview
        </div>

        <div class="analytics-section-subtitle">
            Locations ranked from highest to lowest thermal risk.
        </div>
        """
    )


    ranked_df = df.sort_values(
        by="risk_score",
        ascending=False,
    ).reset_index(
        drop=True
    )


    for index, row in ranked_df.iterrows():

        risk_score = float(
            row["risk_score"]
        )

        risk_level = str(
            row["risk_level"]
        ).strip().lower()


        if risk_level == "low":
            level_class = "analytics-low"
            fill_color = "#4ade80"

        elif risk_level == "moderate":
            level_class = "analytics-moderate"
            fill_color = "#facc15"

        elif risk_level == "high":
            level_class = "analytics-high"
            fill_color = "#fb923c"

        else:
            level_class = "analytics-extreme"
            fill_color = "#f87171"


        risk_width = max(
            3,
            min(
                100,
                risk_score
            )
        )


        st.html(
            f"""
            <div class="map-location-card">

                <div class="map-location-rank">
                    #{index + 1}
                </div>

                <div class="map-location-main">

                    <div class="map-location-name">
                        {row["location"]}
                    </div>

                    <div class="map-location-meta">
                        {float(row["temperature"]):.1f} °C
                        &nbsp; • &nbsp;
                        {float(row["humidity"]):.0f}% humidity
                    </div>

                </div>

                <div class="map-location-risk">

                    <div class="map-risk-score">
                        {risk_score:.0f}
                    </div>

                    <div class="
                        analytics-risk-level
                        {level_class}
                    ">
                        {str(row["risk_level"]).upper()}
                    </div>

                </div>

                <div class="map-risk-bar">

                    <div
                        class="map-risk-fill"
                        style="
                            width: {risk_width}%;
                            background: {fill_color};
                        "
                    ></div>

                </div>

            </div>
            """
        )