import streamlit as st


def show_forecast(report):
    forecast = report["forecast"]
    summary = report["summary"]
    heatwave = report["heatwave"]

    st.subheader("5-Day Heatwave Forecast")
    st.caption("THERMOSAFE projected thermal-risk outlook")

    # Daily forecast
    cols = st.columns(len(forecast))

    for col, day in zip(cols, forecast):
        with col:
            st.metric(
                f"Day {day['day']}",
                f"{day['temperature_c']} °C"
            )
            st.write(f"💧 {day['humidity']}% humidity")
            st.write(f"⚠️ Risk: {day['risk_score']}/100")
            st.write(f"**{day['risk_level']}**")

    st.divider()

    # Forecast summary
    st.subheader("Forecast Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Average Temperature",
            f"{summary['average_temperature']} °C"
        )

    with c2:
        st.metric(
            "Average Risk",
            f"{summary['average_risk_score']}/100"
        )

    with c3:
        st.metric(
            "Highest Risk",
            f"Day {summary['highest_risk_day']}"
        )

    with c4:
        st.metric(
            "High / Extreme Days",
            summary["high_or_extreme_days"]
        )

    # Heatwave alert
    if heatwave["detected"]:
        st.error(
            f"🔥 HEATWAVE ALERT — {heatwave['severity']}\n\n"
            f"{heatwave['message']}"
        )
    else:
        st.success(
            "No sustained heatwave pattern detected."
        )