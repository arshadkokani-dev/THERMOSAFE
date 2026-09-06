import folium


def create_risk_map(risk_locations):
    """
    Create an interactive Folium map for THERMOSAFE
    thermal-risk locations.
    """

    if not risk_locations:
        return None

    center_lat = sum(
        location["latitude"]
        for location in risk_locations
    ) / len(risk_locations)

    center_lon = sum(
        location["longitude"]
        for location in risk_locations
    ) / len(risk_locations)

    thermal_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles="Esri WorldStreetMap",
        control_scale=True,
    )

    for location in risk_locations:

        risk_score = float(
            location.get("risk_score", 0)
        )

        risk_level = str(
            location.get("risk_level", "UNKNOWN")
        ).upper()

        if risk_score >= 75:
            marker_color = "red"

        elif risk_score >= 50:
            marker_color = "orange"

        elif risk_score >= 30:
            marker_color = "beige"

        else:
            marker_color = "green"

        popup_html = f"""
        <div style="
            width: 210px;
            font-family: Arial, sans-serif;
        ">

            <div style="
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 8px;
            ">
                {location["location"]}
            </div>

            <div style="margin-bottom: 4px;">
                <b>Risk Score:</b>
                {risk_score:.0f}/100
            </div>

            <div style="margin-bottom: 4px;">
                <b>Risk Level:</b>
                {risk_level}
            </div>

            <div style="margin-bottom: 4px;">
                <b>Temperature:</b>
                {location["temperature"]:.1f} °C
            </div>

            <div>
                <b>Humidity:</b>
                {location["humidity"]:.0f}%
            </div>

        </div>
        """

        folium.Marker(
            location=[
                location["latitude"],
                location["longitude"],
            ],
            popup=folium.Popup(
                popup_html,
                max_width=260,
            ),
            tooltip=(
                f'{location["location"]} — '
                f'{risk_score:.0f}/100 {risk_level}'
            ),
            icon=folium.Icon(
                color=marker_color,
                icon="info-sign",
            ),
        ).add_to(thermal_map)

    return thermal_map