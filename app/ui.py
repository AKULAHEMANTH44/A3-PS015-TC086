import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* =====================================================
           NETNEXUS PREMIUM CYBER / NOC THEME
           ===================================================== */

        :root {
            --bg: #050816;
            --panel: #0b1224;
            --panel-light: #101a33;
            --cyan: #22d3ee;
            --blue: #3b82f6;
            --violet: #8b5cf6;
            --green: #22c55e;
            --amber: #f59e0b;
            --red: #ef4444;
            --white: #f8fafc;
            --muted: #94a3b8;
            --border: rgba(148, 163, 184, 0.16);
        }

        /* =====================================================
           MAIN BACKGROUND
           ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 0%,
                    rgba(34, 211, 238, 0.13),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139, 92, 246, 0.13),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 50% 100%,
                    rgba(59, 130, 246, 0.08),
                    transparent 30%
                ),
                #050816;

            color: #f8fafc;
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        /* =====================================================
           HEADER
           ===================================================== */

        .nx-header {
            position: relative;
            overflow: hidden;

            padding: 30px 34px;
            margin-bottom: 25px;

            border-radius: 22px;

            background:
                linear-gradient(
                    135deg,
                    rgba(11, 18, 36, 0.97),
                    rgba(16, 26, 51, 0.94)
                );

            border: 1px solid rgba(34, 211, 238, 0.20);

            box-shadow:
                0 0 40px rgba(34, 211, 238, 0.07),
                0 20px 55px rgba(0, 0, 0, 0.35);
        }

        .nx-header::before {
            content: "";

            position: absolute;

            top: 0;
            left: 0;
            right: 0;

            height: 4px;

            background:
                linear-gradient(
                    90deg,
                    #22d3ee,
                    #3b82f6,
                    #8b5cf6,
                    #22d3ee
                );
        }

        .nx-header::after {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            right: -70px;
            top: -70px;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(34, 211, 238, 0.16),
                    transparent 65%
                );
        }

        .nx-brand {
            font-size: 36px;
            font-weight: 900;
            letter-spacing: 3px;

            background:
                linear-gradient(
                    90deg,
                    #ffffff,
                    #22d3ee,
                    #8b5cf6
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nx-subtitle {
            margin-top: 8px;

            color: #94a3b8;

            font-size: 14px;

            letter-spacing: 0.5px;
        }

        .nx-status {
            display: inline-block;

            margin-top: 18px;

            padding: 7px 15px;

            border-radius: 999px;

            color: #86efac;

            background: rgba(34, 197, 94, 0.09);

            border: 1px solid rgba(34, 197, 94, 0.30);

            font-size: 12px;

            font-weight: 800;

            letter-spacing: 1px;

            box-shadow:
                0 0 18px rgba(34, 197, 94, 0.08);
        }

        /* =====================================================
           HEADINGS
           ===================================================== */

        h1,
        h2,
        h3 {
            color: #f8fafc !important;
        }

        h1 {
            letter-spacing: -0.5px;
        }

        h2 {
            margin-top: 18px;
        }

        /* =====================================================
           METRIC CARDS
           ===================================================== */

        [data-testid="stMetric"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(16, 26, 51, 0.96),
                    rgba(8, 15, 30, 0.96)
                );

            border: 1px solid rgba(59, 130, 246, 0.20);

            border-radius: 17px;

            padding: 18px;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.20);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);

            border-color: rgba(34, 211, 238, 0.45);

            box-shadow:
                0 0 28px rgba(34, 211, 238, 0.10);
        }

        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
        }

        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }

        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {
            border: 1px solid rgba(34, 211, 238, 0.38);

            border-radius: 11px;

            background:
                linear-gradient(
                    135deg,
                    #075985,
                    #1d4ed8,
                    #4338ca
                );

            color: #ffffff;

            font-weight: 800;

            padding: 0.62rem 1.35rem;

            box-shadow:
                0 6px 20px rgba(37, 99, 235, 0.22);

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #22d3ee;

            box-shadow:
                0 0 28px rgba(34, 211, 238, 0.25);

            transform: translateY(-2px);
        }

        /* =====================================================
           TABS
           ===================================================== */

        button[data-baseweb="tab"] {
            color: #64748b !important;

            font-weight: 800;

            transition: color 0.2s ease;
        }

        button[data-baseweb="tab"]:hover {
            color: #22d3ee !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #22d3ee !important;
        }

        /* =====================================================
           SELECT BOX
           ===================================================== */

        div[data-baseweb="select"] > div {
            background: #0b1224;

            border: 1px solid rgba(59, 130, 246, 0.25);

            border-radius: 11px;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: rgba(34, 211, 238, 0.55);
        }

        /* =====================================================
           DATAFRAME
           ===================================================== */

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(59, 130, 246, 0.20);

            border-radius: 14px;

            overflow: hidden;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.16);
        }

        /* =====================================================
           ALERTS
           ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 13px;
        }

        /* =====================================================
           TEXT AREA
           ===================================================== */

        textarea {
            background: #070e1d !important;

            color: #dbeafe !important;

            border:
                1px solid rgba(59, 130, 246, 0.25)
                !important;

            border-radius: 13px !important;
        }

        /* =====================================================
           DOWNLOAD BUTTON
           ===================================================== */

        .stDownloadButton > button {
            border-radius: 10px;

            background:
                linear-gradient(
                    135deg,
                    #0f766e,
                    #0369a1
                );

            color: #ffffff;

            font-weight: 800;

            border: 1px solid rgba(34, 211, 238, 0.30);
        }

        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {
            border-color:
                rgba(148, 163, 184, 0.10) !important;
        }

        /* =====================================================
           FOOTER
           ===================================================== */

        .nx-footer {
            text-align: center;

            color: #64748b;

            font-size: 12px;

            padding: 25px 0 5px;

            border-top:
                1px solid rgba(148, 163, 184, 0.10);

            margin-top: 30px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
