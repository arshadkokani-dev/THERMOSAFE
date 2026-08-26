import streamlit as st


def show_dashboard(data):

    st.markdown(
        """
        <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .subtitle {
            color: #8b95a7;
            font-size: 16px;
            margin-bottom: 28px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 12px;
        }

        .risk-box {
            padding: 24px;
            border-radius: 16px;
            background: linear-gradient(135deg, #111827, #1f2937);
            border: 1px solid #374151;
            margin-top: 10px;
        }

        .risk-number {
            font-size: 42px;
            font-weight: 700;
        }

        .risk-label {
            font-size: 18px;
            font-weight: 600;
            margin-top: 4px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">THERMOSAFE Command Center</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Real-time environmental monitoring and human thermal risk intelligence.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Current Environment</div>',
        unsafe_allow_html=True
    )

    temperature = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    heat_index = data.get("heat_index", temperature)
    wind = data.get("wind", 0)

    cols = st.columns(4)

    cols[0].metric(
        "TEMPERATURE",
        f"{temperature:.1f} °C"
    )

    cols[1].metric(
        "HUMIDITY",
        f"{humidity:.0f} %"
    )

    cols[2].metric(
        "HEAT INDEX",
        f"{heat_index:.1f} °C"
    )

    cols[3].metric(
        "WIND",
        f"{wind:.1f} km/h"
    )

    st.markdown(
        '<div class="section-title">Human Thermal Risk</div>',
        unsafe_allow_html=True
    )

    risk_score = data.get("risk_score", 0)
    risk_level = data.get("risk_level", "ANALYZING")

    risk_cols = st.columns(2)

    risk_cols[0].metric(
        "THERMAL STRESS SCORE",
        f"{risk_score}/100"
    )

    risk_cols[1].metric(
        "RISK LEVEL",
        risk_level
    )

    st.info(
        "THERMOSAFE has analyzed the current environmental conditions."
    )