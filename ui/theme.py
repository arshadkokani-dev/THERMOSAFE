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
}

    </style>
    """