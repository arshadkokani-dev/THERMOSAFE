from pathlib import Path
import base64


def get_svg_icon(name):
    icon_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "icons"
        / f"{name}.svg"
    )

    if not icon_path.exists():
        return ""

    svg = icon_path.read_bytes()
    encoded = base64.b64encode(svg).decode("utf-8")

    return (
        f'<img class="thermosafe-icon thermosafe-icon-{name}" '
        f'src="data:image/svg+xml;base64,{encoded}" '
        f'alt="" />'
    )


def apply_theme():
    return """
    <style>

    /* ---------- Global ---------- */

    .thermosafe-icon {
        width: 22px !important;
        height: 22px !important;
        max-width: 22px !important;
        max-height: 22px !important;
        object-fit: contain;
        display: inline-block;
        vertical-align: middle;
        flex-shrink: 0;

        /* Force dark SVG artwork to become visible */
        filter: brightness(0) saturate(100%)
                invert(73%) sepia(82%) saturate(1645%)
                hue-rotate(163deg) brightness(101%) contrast(101%);
    }

    /* ---------- Section Titles ---------- */

    .section-title {
        display: flex;
        align-items: center;
        gap: 9px;
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.8rem;
        margin-bottom: 0.9rem;
        color: #f8fafc;
        line-height: 1.3;
    }

    .section-title .thermosafe-icon {
        width: 21px !important;
        height: 21px !important;
        max-width: 21px !important;
        max-height: 21px !important;
    }

    /* ---------- Environment Cards ---------- */

    .metric-card {
        min-height: 145px;
        padding: 20px;
        border-radius: 16px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.72)
            );
        border: 1px solid rgba(56, 189, 248, 0.18);
        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.20);
        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.45);
    }

    .metric-icon {
        width: 30px;
        height: 30px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    .metric-icon .thermosafe-icon {
        width: 30px !important;
        height: 30px !important;
        max-width: 30px !important;
        max-height: 30px !important;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 5px;
    }

    /* ---------- Intelligence Cards ---------- */

    .intelligence-card {
        padding: 22px;
        border-radius: 16px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.78)
            );
        border: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.18);
    }

    .card-label {
        color: #60a5fa;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .card-title {
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .card-text {
        color: #cbd5e1;
        line-height: 1.65;
        font-size: 0.92rem;
    }

    /* ---------- Risk Hero ---------- */

    .risk-hero {
        padding: 30px;
        border-radius: 22px;
        background:
            radial-gradient(
                circle at 80% 20%,
                rgba(56, 189, 248, 0.16),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #0f172a,
                #10233a
            );
        border: 1px solid rgba(56, 189, 248, 0.28);
        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.25);
    }

    .risk-score {
        font-size: 3.8rem;
        line-height: 1;
        font-weight: 750;
        color: #f8fafc;
    }

    .risk-denominator {
        color: #64748b;
        font-size: 1rem;
    }

    .risk-description {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.55;
        margin-top: 8px;
    }

    /* ---------- Location ---------- */

    .location-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 10px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.18);
        color: #e2e8f0;
        font-size: 0.82rem;
    }

    .location-badge .thermosafe-icon {
        width: 17px !important;
        height: 17px !important;
        max-width: 17px !important;
        max-height: 17px !important;
    }

    /* ---------- Forecast ---------- */

    .forecast-card {
        min-height: 165px;
        padding: 18px;
        border-radius: 16px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.78)
            );
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    .forecast-day {
        color: #94a3b8;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .forecast-temperature {
        color: #f8fafc;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 12px;
    }

    .forecast-risk {
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 5px;
    }

    /* ---------- Forecast Intelligence ---------- */

    .forecast-card {
        min-height: 175px;
        padding: 18px;
        border-radius: 16px;
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(15, 23, 42, 0.78)
            );
        border: 1px solid rgba(56, 189, 248, 0.14);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .forecast-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    }

    .forecast-day {
        color: #60a5fa;
        font-size: 0.68rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .forecast-temperature {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 750;
        margin-top: 13px;
    }

    .forecast-risk {
        color: #94a3b8;
        font-size: 0.76rem;
        margin-top: 5px;
    }

    .forecast-risk-bar {
        width: 100%;
        height: 5px;
        margin-top: 14px;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.12);
        overflow: hidden;
    }

    .forecast-risk-fill {
        height: 100%;
        min-width: 3px;
        border-radius: 999px;
    }

    .forecast-risk-label {
        color: #64748b;
        font-size: 0.62rem;
        margin-top: 7px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ---------- Risk Pills ---------- */

    .risk-pill {
        display: inline-block;
        margin-top: 14px;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.04em;
    }

    .risk-low {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .risk-moderate {
        background: rgba(234, 179, 8, 0.15);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.3);
    }

    .risk-high {
        background: rgba(249, 115, 22, 0.15);
        color: #fb923c;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }

    .risk-extreme {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .risk-meter {
        width: 100%;
        height: 8px;
        margin-top: 22px;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.18);
        overflow: hidden;
    }

    .risk-meter-fill {
        height: 100%;
        min-width: 3px;
        border-radius: 999px;
        transition: width 0.45s ease;
    }

    .risk-meter-scale {
        display: flex;
        justify-content: space-between;
        margin-top: 7px;
        color: #64748b;
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ---------- Alert & Risk Explanation ---------- */

    .alert-card,
    .explanation-card {
        min-height: 150px;
        padding: 22px;
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.96),
            rgba(15, 23, 42, 0.78)
        );
        border: 1px solid rgba(56, 189, 248, 0.14);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
    }

    .alert-card {
        border-left: 3px solid #38bdf8;
    }

    .explanation-card {
        border-left: 3px solid #60a5fa;
    }

    .alert-status,
    .explanation-label {
        color: #60a5fa;
        font-size: 0.65rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .alert-title {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 8px;
    }

    .alert-message,
    .explanation-text {
        color: #cbd5e1;
        font-size: 0.88rem;
        line-height: 1.6;
        margin-top: 8px;
    }

    /* ---------- AI Advisor ---------- */

.ai-card {
    padding: 26px;
    border-radius: 18px;
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(56, 189, 248, 0.12),
            transparent 32%
        ),
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.98),
            rgba(12, 27, 48, 0.88)
        );
    border: 1px solid rgba(56, 189, 248, 0.22);
    box-shadow:
        0 12px 40px rgba(0, 0, 0, 0.22);
}

.ai-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.ai-status {
    padding: 5px 9px;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.10);
    border: 1px solid rgba(56, 189, 248, 0.25);
    color: #38bdf8;
    font-size: 0.62rem;
    font-weight: 750;
    letter-spacing: 0.08em;
}

.ai-advice {
    margin-top: 12px;
    color: #dbeafe;
    line-height: 1.75;
}

    /* =========================================================
    FORECAST & ANALYTICS
    ========================================================= */

    .analytics-section {
        margin-top: 30px;
        margin-bottom: 12px;
        color: #f8fafc;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .analytics-section-subtitle {
        color: #64748b;
        font-size: 0.76rem;
        margin-top: -4px;
        margin-bottom: 14px;
    }

    /* =========================================================
    FORECAST CARD POLISH
    ========================================================= */

    .analytics-metric {
        position: relative;
        overflow: hidden;
    }

    .analytics-metric::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 3px;
        height: 100%;
        background: rgba(56, 189, 248, 0.65);
    }

    .analytics-metric:first-child::before {
        background: #38bdf8;
    }

    .analytics-metric:nth-child(2)::before {
        background: #60a5fa;
    }

    .analytics-metric:nth-child(3)::before {
        background: #facc15;
    }

    .analytics-metric:nth-child(4)::before {
        background: #38bdf8;
    }

    .analytics-value {
        line-height: 1.15;
    }

    /* ---------- Forecast Summary Emphasis ---------- */

    .analytics-summary .analytics-metric:nth-child(2) {
        border-color: rgba(56, 189, 248, 0.25);
    }

    .analytics-summary .analytics-metric:nth-child(4) {
        border-color: rgba(56, 189, 248, 0.25);
    }

    /* ---------- Forecast Outlook ---------- */

    .analytics-forecast-card {
        position: relative;
        overflow: hidden;
    }

    .analytics-forecast-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: rgba(56, 189, 248, 0.55);
    }

    .analytics-forecast-card:hover::before {
        background: #38bdf8;
    }

    .analytics-temp {
        line-height: 1;
    }

    .analytics-risk {
        margin-top: 8px;
    }

    .analytics-risk-level {
        text-transform: uppercase;
    }

    /* ---------- Heatwave / Response ---------- */

    .analytics-insight {
        position: relative;
        overflow: hidden;
    }

    .analytics-insight::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: rgba(56, 189, 248, 0.035);
        transform: translate(35%, -35%);
        pointer-events: none;
    }


    /* ---------------------------------------------------------
    ANALYTICS METRICS
    --------------------------------------------------------- */

    .analytics-metric {
        min-height: 126px;
        padding: 20px;
        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(15, 23, 42, 0.78)
            );

        border: 1px solid rgba(56, 189, 248, 0.14);

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.18);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .analytics-metric:hover {
        transform: translateY(-3px);

        border-color:
            rgba(56, 189, 248, 0.32);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.23);
    }

    .analytics-label {
        color: #64748b;
        font-size: 0.64rem;
        font-weight: 750;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    .analytics-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 750;
        margin-top: 11px;
        letter-spacing: -0.02em;
    }


    /* ---------------------------------------------------------
    FORECAST SUMMARY
    --------------------------------------------------------- */

    .analytics-summary {
        margin-top: 4px;
    }


    /* ---------------------------------------------------------
    CHART CONTAINER
    --------------------------------------------------------- */

    .analytics-chart-card {
        padding: 18px 18px 8px 18px;
        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(15, 23, 42, 0.80)
            );

        border: 1px solid rgba(56, 189, 248, 0.14);

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.18);
    }


    /* ---------------------------------------------------------
    5-DAY FORECAST CARDS
    --------------------------------------------------------- */

    .analytics-forecast-card {
        min-height: 192px;
        padding: 19px;

        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(15, 23, 42, 0.78)
            );

        border: 1px solid rgba(148, 163, 184, 0.15);

        box-shadow:
            0 8px 28px rgba(0, 0, 0, 0.15);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .analytics-forecast-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(56, 189, 248, 0.34);

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.24);
    }

    .analytics-day {
        color: #60a5fa;
        font-size: 0.66rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .analytics-temp {
        color: #f8fafc;
        font-size: 1.7rem;
        font-weight: 750;
        margin-top: 14px;
        letter-spacing: -0.03em;
    }

    .analytics-risk {
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 6px;
    }

    .analytics-risk-bar {
        width: 100%;
        height: 5px;

        margin-top: 15px;

        border-radius: 999px;

        background:
            rgba(148, 163, 184, 0.12);

        overflow: hidden;
    }

    .analytics-risk-fill {
        height: 100%;
        min-width: 3px;

        border-radius: 999px;
    }

    .analytics-risk-level {
        display: inline-block;

        margin-top: 13px;

        padding: 5px 9px;

        border-radius: 999px;

        font-size: 0.61rem;
        font-weight: 750;

        letter-spacing: 0.06em;
    }


    /* ---------------------------------------------------------
    RISK LEVEL COLORS
    --------------------------------------------------------- */

    .analytics-low {
        color: #4ade80;

        background:
            rgba(34, 197, 94, 0.10);

        border:
            1px solid rgba(34, 197, 94, 0.22);
    }

    .analytics-moderate {
        color: #facc15;

        background:
            rgba(234, 179, 8, 0.10);

        border:
            1px solid rgba(234, 179, 8, 0.22);
    }

    .analytics-high {
        color: #fb923c;

        background:
            rgba(249, 115, 22, 0.10);

        border:
            1px solid rgba(249, 115, 22, 0.22);
    }

    .analytics-extreme {
        color: #f87171;

        background:
            rgba(239, 68, 68, 0.10);

        border:
            1px solid rgba(239, 68, 68, 0.22);
    }


    /* ---------------------------------------------------------
    INTELLIGENCE CARDS
    --------------------------------------------------------- */

    .analytics-insight-grid {
        display: grid;

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 16px;
    }

    .analytics-insight {
        min-height: 150px;

        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.98),
                rgba(12, 27, 48, 0.88)
            );

        border: 1px solid rgba(56, 189, 248, 0.18);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.20);
    }

    .analytics-insight.warning {
        border-left:
            3px solid #facc15;
    }

    .analytics-insight.safe {
        border-left:
            3px solid #4ade80;
    }

    .analytics-insight.danger {
        border-left:
            3px solid #fb923c;
    }

    .analytics-insight.critical {
        border-left:
            3px solid #f87171;
    }

    .analytics-insight-label {
        color: #60a5fa;

        font-size: 0.64rem;
        font-weight: 750;

        letter-spacing: 0.1em;

        text-transform: uppercase;
    }

    .analytics-insight-title {
        color: #f8fafc;

        font-size: 1.04rem;
        font-weight: 700;

        margin-top: 8px;
    }

    .analytics-insight-text {
        color: #cbd5e1;

        font-size: 0.87rem;
        line-height: 1.65;

        margin-top: 8px;
    }


    /* ---------------------------------------------------------
    MOBILE
    --------------------------------------------------------- */

    @media (max-width: 900px) {

        .analytics-metric {
            min-height: 115px;
            padding: 17px;
        }

        .analytics-forecast-card {
            min-height: 175px;
            padding: 17px;
        }

        .analytics-insight-grid {
            grid-template-columns: 1fr;
        }
    }


    @media (max-width: 640px) {

        .analytics-section {
            font-size: 1.08rem;
            margin-top: 24px;
        }

        .analytics-metric {
            min-height: 105px;
            padding: 15px;
        }

        .analytics-value {
            font-size: 1.4rem;
        }

        .analytics-chart-card {
            padding: 12px 10px 5px 10px;
            border-radius: 15px;
        }

        .analytics-forecast-card {
            min-height: 155px;
            padding: 16px;
        }

        .analytics-temp {
            font-size: 1.5rem;
        }

        .analytics-insight {
            min-height: 130px;
            padding: 18px;
        }
    }

/* ---------- Responsive Layout ---------- */

@media (max-width: 900px) {

    .risk-hero {
        padding: 24px;
    }

    .risk-hero-content {
        gap: 20px;
    }

    .metric-card {
        min-height: 130px;
        padding: 17px;
    }

    .forecast-card {
        min-height: 155px;
        padding: 16px;
    }

    .ai-card {
        padding: 22px;
    }
}

@media (max-width: 640px) {

    .thermosafe-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .risk-hero {
        padding: 20px;
        border-radius: 18px;
    }

    .risk-score {
        font-size: 3rem;
    }

    .section-title {
        font-size: 1.15rem;
    }

    .metric-card {
        min-height: 120px;
        padding: 15px;
    }

    .metric-value {
        font-size: 1.45rem;
    }

    .forecast-card {
        min-height: 145px;
    }

    .alert-card,
    .explanation-card {
        min-height: 130px;
        padding: 18px;
    }

    .ai-card {
        padding: 18px;
    }

    .ai-advice {
        font-size: 0.86rem;
        line-height: 1.65;
        }


        /* =========================================================
        THERMAL RISK MAP
        ========================================================= */

        .map-location-card {
            position: relative;
            display: grid;
            grid-template-columns: 42px 1fr auto;
            gap: 14px;
            align-items: center;

            margin-bottom: 10px;
            padding: 17px 18px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(15, 23, 42, 0.78)
                );

            border: 1px solid rgba(148, 163, 184, 0.14);

            box-shadow:
                0 7px 25px rgba(0, 0, 0, 0.16);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }

        .map-location-card:hover {
            transform: translateY(-2px);
            border-color: rgba(56, 189, 248, 0.3);
        }

        .map-location-rank {
            color: #60a5fa;
            font-size: 0.8rem;
            font-weight: 750;
        }

        .map-location-name {
            color: #f8fafc;
            font-size: 0.98rem;
            font-weight: 700;
        }

        .map-location-meta {
            margin-top: 5px;
            color: #64748b;
            font-size: 0.72rem;
        }

        .map-location-risk {
            text-align: right;
        }

        .map-risk-score {
            color: #f8fafc;
            font-size: 1.35rem;
            font-weight: 750;
        }

        .map-risk-bar {
            grid-column: 2 / 4;

            width: 100%;
            height: 4px;

            margin-top: -3px;

            border-radius: 999px;

            background:
                rgba(148, 163, 184, 0.12);

            overflow: hidden;
        }

        .map-risk-fill {
            height: 100%;
            min-width: 3px;
            border-radius: 999px;
        }

        @media (max-width: 640px) {

            .map-location-card {
                grid-template-columns: 32px 1fr auto;
                gap: 10px;
                padding: 14px;
            }

            .map-location-name {
                font-size: 0.9rem;
            }

            .map-location-meta {
                font-size: 0.67rem;
            }

            .map-risk-score {
                font-size: 1.15rem;
            }
        }

        /* =========================================================
        SIMULATION LAB
        ========================================================= */

        .simulation-delta {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;

            margin: 18px 0 22px;
            padding: 14px 16px;

            border-radius: 14px;

            background: rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .simulation-delta > div {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .simulation-delta-label {
            color: #94a3b8;
            font-size: 0.75rem;
        }

        .simulation-delta strong {
            color: #38bdf8;
            font-size: 0.82rem;
        }

        .simulation-result-card {
            position: relative;
            overflow: hidden;

            min-height: 125px;
            padding: 20px;

            border-radius: 16px;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(15, 23, 42, 0.78)
                );

            border: 1px solid rgba(148, 163, 184, 0.14);

            box-shadow:
                0 8px 28px rgba(0, 0, 0, 0.16);
        }

        .simulation-result-card::before {
            content: "";

            position: absolute;
            top: 0;
            left: 0;

            width: 3px;
            height: 100%;

            background: #38bdf8;
        }

        .simulation-score {
            margin-top: 12px;

            color: #f8fafc;

            font-size: 2rem;
            font-weight: 750;
        }

        .simulation-score span {
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .simulation-level {
            margin-top: 14px;

            color: #38bdf8;

            font-size: 1.15rem;
            font-weight: 750;
        }

        .simulation-comparison-card {
            padding: 20px;

            border-radius: 15px;

            background: rgba(15, 23, 42, 0.72);

            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .simulation-comparison-score {
            margin-top: 10px;

            color: #f8fafc;

            font-size: 1.7rem;
            font-weight: 750;
        }

        .simulation-comparison-level {
            margin-top: 6px;

            color: #60a5fa;

            font-size: 0.75rem;
            font-weight: 750;
        }

        .simulation-population-card {
            padding: 24px;

            margin-bottom: 18px;

            border-radius: 16px;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(15, 23, 42, 0.78)
                );

            border: 1px solid rgba(56, 189, 248, 0.14);
        }

        .simulation-population-number {
            color: #f8fafc;

            font-size: 2rem;
            font-weight: 750;
        }

        .simulation-population-label {
            margin-top: 3px;

            color: #64748b;

            font-size: 0.68rem;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        .simulation-population-text {
            margin-top: 12px;

            color: #94a3b8;

            font-size: 0.82rem;
        }

        .simulation-population-text strong {
            color: #e2e8f0;
        }

        @media (max-width: 640px) {

            .simulation-delta {
                grid-template-columns: 1fr;
            }

            .simulation-result-card {
                margin-bottom: 10px;
            }

            .simulation-score {
                font-size: 1.7rem;
            }

        }

        /* =========================================================
        RISK INTELLIGENCE
        ========================================================= */

        .risk-population-card {
            position: relative;
            overflow: hidden;

            min-height: 125px;
            padding: 18px;

            border-radius: 15px;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(15, 23, 42, 0.78)
                );

            border: 1px solid rgba(148, 163, 184, 0.14);

            box-shadow:
                0 7px 25px rgba(0, 0, 0, 0.15);
        }

        .risk-population-card::before {
            content: "";

            position: absolute;
            top: 0;
            left: 0;

            width: 3px;
            height: 100%;

            background: #38bdf8;
        }

        .risk-population-score {
            margin-top: 12px;

            color: #f8fafc;

            font-size: 1.65rem;
            font-weight: 750;
        }

        .risk-population-score span {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 500;
        }

        .risk-population-level {
            margin-top: 7px;

            color: #60a5fa;

            font-size: 0.7rem;
            font-weight: 750;
        }

        .risk-action-card {
            position: relative;

            margin-bottom: 10px;
            padding: 17px 20px 17px 22px;

            border-radius: 14px;

            background:
                rgba(15, 23, 42, 0.78);

            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .risk-action-card::before {
            content: "";

            position: absolute;
            left: 0;
            top: 0;

            width: 3px;
            height: 100%;

            border-radius: 3px;
            background: #38bdf8;
        }

        .risk-action-card.critical::before {
            background: #f87171;
        }

        .risk-action-card.danger::before {
            background: #fb923c;
        }

        .risk-action-card.warning::before {
            background: #facc15;
        }

        .risk-action-card.safe::before {
            background: #4ade80;
        }

        .risk-action-priority {
            margin-bottom: 5px;

            color: #64748b;

            font-size: 0.65rem;
            font-weight: 750;
            letter-spacing: 0.08em;
        }

        .risk-action-title {
            color: #f8fafc;

            font-size: 0.95rem;
            font-weight: 700;
        }

        .risk-action-message {
            margin-top: 5px;

            color: #94a3b8;

            font-size: 0.8rem;
            line-height: 1.5;
        }

        .risk-ai-card {
            position: relative;
            overflow: hidden;

            padding: 22px;

            border-radius: 16px;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 23, 42, 0.98),
                    rgba(15, 23, 42, 0.78)
                );

            border: 1px solid rgba(56, 189, 248, 0.18);

            box-shadow:
                0 8px 28px rgba(0, 0, 0, 0.16);
        }

        .risk-ai-card::before {
            content: "";

            position: absolute;
            left: 0;
            top: 0;

            width: 3px;
            height: 100%;

            background: #38bdf8;
        }

        .risk-ai-label {
            color: #38bdf8;

            font-size: 0.68rem;
            font-weight: 750;
            letter-spacing: 0.08em;
        }

        .risk-ai-text {
            margin-top: 12px;

            color: #cbd5e1;

            font-size: 0.88rem;
            line-height: 1.65;
        }

        @media (max-width: 640px) {

            .risk-population-card {
                margin-bottom: 10px;
            }

            .risk-population-score {
                font-size: 1.45rem;
            }

            .risk-ai-card {
                padding: 18px;
            }

        }

        /* =========================================================
   THERMOSAFE SIDEBAR — FINAL UI POLISH
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #07182d 0%,
            #0a1d34 55%,
            #08172a 100%
        );
    border-right: 1px solid rgba(56, 189, 248, 0.12);
}


/* ---------- Sidebar Brand ---------- */

.thermosafe-sidebar-brand {
    padding: 8px 4px 20px 4px;
}

.thermosafe-sidebar-logo {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #f8fafc;
}

.thermosafe-sidebar-logo::first-letter {
    color: #38bdf8;
}

.thermosafe-sidebar-tagline {
    margin-top: 4px;
    color: #94a3b8;
    font-size: 0.74rem;
    line-height: 1.4;
}


/* ---------- Navigation ---------- */

[data-testid="stSidebarNav"] {
    padding-top: 8px;
    padding-bottom: 12px;
}

[data-testid="stSidebarNav"] ul {
    gap: 5px;
}

[data-testid="stSidebarNav"] li {
    margin: 0;
}

[data-testid="stSidebarNav"] a {
    border-radius: 11px;
    padding: 10px 12px;
    color: #cbd5e1;
    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(56, 189, 248, 0.08);
    color: #f8fafc;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background:
        linear-gradient(
            90deg,
            rgba(37, 99, 235, 0.42),
            rgba(14, 116, 144, 0.24)
        );
    color: #f8fafc;
    border-left: 3px solid #38bdf8;
    box-shadow:
        0 6px 22px rgba(0, 0, 0, 0.18);
}


/* ---------- Navigation Icons ---------- */

[data-testid="stSidebarNav"] a span {
    color: #38bdf8;
}

[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: #67e8f9;
}


/* ---------- Environment Label ---------- */

.sidebar-section-label {
    margin-top: 14px;
    margin-bottom: 8px;
    color: #64748b;
    font-size: 0.63rem;
    font-weight: 750;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}


/* ---------- Sidebar Input ---------- */

[data-testid="stSidebar"] input {
    background: rgba(15, 23, 42, 0.72) !important;
    border: 1px solid rgba(56, 189, 248, 0.18) !important;
    color: #f8fafc !important;
    border-radius: 11px !important;
}

[data-testid="stSidebar"] input:focus {
    border-color: rgba(56, 189, 248, 0.55) !important;
    box-shadow:
        0 0 0 1px rgba(56, 189, 248, 0.18) !important;
}


/* ---------- Analyze Button ---------- */

[data-testid="stSidebar"] button[kind="primary"] {
    border-radius: 11px;
    border: 1px solid rgba(56, 189, 248, 0.28);
    background:
        linear-gradient(
            135deg,
            #0ea5e9,
            #2563eb
        );
    color: #ffffff;
    font-weight: 700;
    box-shadow:
        0 8px 22px rgba(37, 99, 235, 0.22);
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

[data-testid="stSidebar"] button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow:
        0 11px 28px rgba(37, 99, 235, 0.30);
}


/* ---------- Footer ---------- */

.thermosafe-sidebar-footer {
    margin-top: 38px;
    padding: 18px 4px 6px 4px;
    text-align: center;
}

.thermosafe-footer-line {
    height: 1px;
    width: 100%;
    margin-bottom: 18px;
    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(56, 189, 248, 0.28),
            transparent
        );
}

.thermosafe-footer-title {
    color: #64748b;
    font-size: 0.69rem;
    line-height: 1.5;
}

.thermosafe-footer-author {
    margin-top: 7px;
    color: #94a3b8;
    font-size: 0.76rem;
}

.thermosafe-footer-author strong {
    color: #38bdf8;
    font-weight: 750;
}


/* ---------- Sidebar Mobile ---------- */

@media (max-width: 768px) {

    .thermosafe-sidebar-logo {
        font-size: 1.35rem;
    }

    .thermosafe-sidebar-tagline {
        font-size: 0.68rem;
    }

    .thermosafe-sidebar-footer {
        margin-top: 26px;
    }

}

     /* =========================================================
   CUSTOM SIDEBAR NAVIGATION
   ========================================================= */

.thermosafe-sidebar-brand {
    padding: 8px 4px 20px 4px;
}

.thermosafe-sidebar-brand-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.thermosafe-sidebar-brand-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(56, 189, 248, 0.10);
    border: 1px solid rgba(56, 189, 248, 0.20);
    font-size: 18px;
}

.thermosafe-sidebar-logo {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #f8fafc;
    line-height: 1.1;
}

.thermosafe-sidebar-tagline {
    margin-top: 4px;
    color: #94a3b8;
    font-size: 0.68rem;
    line-height: 1.3;
}

.sidebar-section-label {
    margin: 8px 0 8px 4px;
    color: #64748b;
    font-size: 0.63rem;
    font-weight: 750;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Custom page links */

[data-testid="stSidebar"] a {
    border-radius: 10px;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a {
    padding: 9px 11px;
    color: #cbd5e1;
    transition:
        background 0.2s ease,
        color 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
    background: rgba(56, 189, 248, 0.08);
    color: #f8fafc;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] svg {
    color: #38bdf8;
}

/* Environment spacing */

.thermosafe-environment-label {
    margin-top: 20px;
}

/* Footer */

.thermosafe-sidebar-footer {
    margin-top: 34px;
    padding: 16px 4px 8px 4px;
    text-align: center;
}

.thermosafe-footer-line {
    height: 1px;
    width: 100%;
    margin-bottom: 16px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(56, 189, 248, 0.28),
        transparent
    );
}

.thermosafe-footer-title {
    color: #64748b;
    font-size: 0.68rem;
    line-height: 1.5;
}

.thermosafe-footer-author {
    margin-top: 6px;
    color: #94a3b8;
    font-size: 0.75rem;
}

.thermosafe-footer-author strong {
    color: #38bdf8;
    font-weight: 750;
}
    
    </style>
    """