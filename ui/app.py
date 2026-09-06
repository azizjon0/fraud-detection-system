import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================

API_URL = os.getenv("API_URL", "http://app:8000")

st.set_page_config(
    page_title="Sentinel | Fraud Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CSS
# =========================================================

st.html(
    """
    <style>
    /* ---------- Global ---------- */

    html, body, [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(108, 92, 231, 0.08),
                transparent 28%
            ),
            #f6f7f9;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ---------- Header ---------- */

    .bank-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #111111;
        color: white;
        border-radius: 14px;
        font-size: 18px;
        font-weight: 800;
    }

    .brand-name {
        font-size: 20px;
        font-weight: 750;
        color: #111111;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        color: #8c8d91;
        font-size: 12px;
        margin-top: 1px;
    }

    .online-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        border: 1px solid #e5e5e5;
        background: rgba(255,255,255,0.8);
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        color: #343434;
    }

    .online-dot {
        width: 7px;
        height: 7px;
        background: #26c281;
        border-radius: 999px;
        box-shadow: 0 0 0 4px rgba(38,194,129,0.10);
    }


    /* ---------- Hero ---------- */

    .hero-card {
        position: relative;
        overflow: hidden;
        min-height: 250px;

        background:
            radial-gradient(
                circle at 90% 20%,
                rgba(148, 106, 255, 0.75),
                transparent 30%
            ),
            radial-gradient(
                circle at 70% 100%,
                rgba(58, 74, 255, 0.65),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #111111 0%,
                #191919 58%,
                #282335 100%
            );

        color: white;
        border-radius: 32px;
        padding: 32px 34px;
        margin-bottom: 22px;
        box-shadow:
            0 18px 50px rgba(20, 20, 30, 0.14);
    }

    .hero-card::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -90px;
        top: -110px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,0.14);
    }

    .hero-eyebrow {
        color: rgba(255,255,255,0.62);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-bottom: 20px;
        font-weight: 600;
    }

    .hero-title {
        font-size: 40px;
        line-height: 1;
        font-weight: 740;
        letter-spacing: -1.7px;
        margin-bottom: 13px;
    }

    .hero-text {
        max-width: 600px;
        color: rgba(255,255,255,0.65);
        font-size: 14px;
        line-height: 1.6;
    }

    .hero-bottom {
        display: flex;
        gap: 28px;
        margin-top: 35px;
    }

    .hero-stat-value {
        color: #ffffff;
        font-weight: 700;
        font-size: 18px;
    }

    .hero-stat-label {
        color: rgba(255,255,255,0.52);
        font-size: 11px;
        margin-top: 2px;
    }


    /* ---------- Generic cards ---------- */

    .section-title {
        color: #111111;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.55px;
        margin-bottom: 4px;
    }

    .section-caption {
        color: #909196;
        font-size: 13px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(0,0,0,0.055);
        border-radius: 24px;
        padding: 23px 24px;
        min-height: 136px;
        box-shadow: 0 5px 22px rgba(20,20,20,0.035);
    }

    .metric-icon {
        width: 34px;
        height: 34px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f2f2f3;
        margin-bottom: 18px;
        font-size: 15px;
    }

    .metric-label {
        color: #8d8e93;
        font-size: 12px;
        font-weight: 550;
    }

    .metric-value {
        color: #131313;
        font-size: 29px;
        font-weight: 720;
        letter-spacing: -1px;
        margin-top: 3px;
    }

    .metric-foot {
        color: #aaa;
        font-size: 10px;
        margin-top: 7px;
    }


    /* ---------- Streamlit form card ---------- */

    .st-key-score_panel {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 28px;
        padding: 26px 28px 28px 28px;
        box-shadow: 0 7px 30px rgba(20,20,20,0.045);
    }

    .st-key-score_panel label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #68696d !important;
    }

    .st-key-score_panel input {
        border-radius: 13px !important;
    }

    .st-key-score_panel [data-baseweb="select"] > div {
        border-radius: 13px !important;
    }


    /* ---------- Buttons ---------- */

    div.stButton > button {
        border-radius: 999px;
        height: 48px;
        padding-left: 24px;
        padding-right: 24px;
        font-weight: 650;
        border: 0;
        transition:
            transform 0.15s ease,
            opacity 0.15s ease;
    }

    div.stButton > button[kind="primary"] {
        background: #111111;
        color: white;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        opacity: 0.91;
    }


    /* ---------- Prediction card ---------- */

    .prediction-shell {
        background: #111111;
        border-radius: 28px;
        padding: 29px;
        color: white;
        min-height: 310px;
        box-shadow: 0 16px 38px rgba(20,20,20,0.12);
    }

    .prediction-label {
        color: #a7a7aa;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .risk-number {
        font-size: 50px;
        font-weight: 760;
        letter-spacing: -2px;
        margin-top: 10px;
        line-height: 1;
    }

    .risk-track {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        margin-top: 25px;
        overflow: hidden;
    }

    .risk-fill {
        height: 100%;
        border-radius: 999px;
    }

    .risk-status {
        display: inline-flex;
        border-radius: 999px;
        padding: 8px 12px;
        margin-top: 19px;
        font-size: 12px;
        font-weight: 700;
    }

    .risk-description {
        color: #9fa0a5;
        line-height: 1.55;
        font-size: 13px;
        margin-top: 18px;
    }

    .prediction-id {
        margin-top: 25px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.09);
        display: flex;
        justify-content: space-between;
        color: #77787c;
        font-size: 11px;
    }


    /* ---------- Empty prediction ---------- */

    .prediction-empty {
        background: #111111;
        border-radius: 28px;
        padding: 29px;
        min-height: 310px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 16px 38px rgba(20,20,20,0.12);
    }

    .shield-circle {
        width: 60px;
        height: 60px;
        border-radius: 20px;
        background: linear-gradient(
            145deg,
            #7766ff,
            #9857ff
        );
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 25px;
        box-shadow: 0 12px 35px rgba(119,102,255,.30);
    }


    /* ---------- Table ---------- */

    .st-key-history_panel {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(0,0,0,0.055);
        border-radius: 28px;
        padding: 26px 28px;
        box-shadow: 0 7px 30px rgba(20,20,20,0.04);
        margin-top: 20px;
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }


    /* ---------- Error ---------- */

    .api-error {
        padding: 17px 19px;
        border-radius: 17px;
        background: #fff0f1;
        color: #b32632;
        border: 1px solid #ffdadd;
        font-size: 13px;
        margin: 10px 0;
    }


    /* ---------- Mobile ---------- */

    @media (max-width: 780px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-card {
            padding: 26px;
            border-radius: 25px;
        }

        .hero-title {
            font-size: 31px;
        }

        .hero-bottom {
            gap: 17px;
            flex-wrap: wrap;
        }

        .bank-header {
            align-items: flex-start;
        }
    }
    </style>
    """
)


# =========================================================
# API HELPERS
# =========================================================

def api_health() -> bool:
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )
        return response.ok

    except requests.RequestException:
        return False


def load_transactions(limit: int = 50) -> list:
    try:
        response = requests.get(
            f"{API_URL}/transactions",
            params={"limit": limit},
            timeout=8,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        return []


def score_transaction(payload: dict) -> dict:
    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# SESSION
# =========================================================

if "prediction" not in st.session_state:
    st.session_state.prediction = None


# =========================================================
# HEADER
# =========================================================

api_online = api_health()

status_html = (
    """
    <div class="online-pill">
        <div class="online-dot"></div>
        API online
    </div>
    """
    if api_online
    else
    """
    <div class="online-pill">
        API offline
    </div>
    """
)

st.html(
    f"""
    <div class="bank-header">
        <div class="brand-row">
            <div class="brand-mark">S</div>

            <div>
                <div class="brand-name">
                    Sentinel
                </div>

                <div class="brand-subtitle">
                    Fraud Intelligence
                </div>
            </div>
        </div>

        {status_html}
    </div>
    """
)


# =========================================================
# LOAD DATA
# =========================================================

transactions = load_transactions(50)

df = pd.DataFrame(transactions)


if not df.empty:

    total_transactions = len(df)

    fraud_count = int(
        df["predicted_fraud"]
        .fillna(False)
        .sum()
    )

    fraud_rate = (
        fraud_count / total_transactions
        if total_transactions > 0
        else 0
    )

    average_risk = (
        df["fraud_probability"]
        .fillna(0)
        .mean()
    )

    transaction_volume = (
        df["amount"]
        .fillna(0)
        .sum()
    )

else:

    total_transactions = 0
    fraud_count = 0
    fraud_rate = 0
    average_risk = 0
    transaction_volume = 0


# =========================================================
# HERO
# =========================================================

st.html(
    f"""
    <div class="hero-card">

        <div class="hero-eyebrow">
            Real-time risk engine
        </div>

        <div class="hero-title">
            Know the risk<br>
            before the money moves.
        </div>

        <div class="hero-text">
            Machine-learning transaction screening with
            real-time scoring, decision logging and
            PostgreSQL persistence.
        </div>

        <div class="hero-bottom">

            <div>
                <div class="hero-stat-value">
                    {total_transactions}
                </div>
                <div class="hero-stat-label">
                    recent transactions
                </div>
            </div>

            <div>
                <div class="hero-stat-value">
                    {fraud_count}
                </div>
                <div class="hero-stat-label">
                    flagged
                </div>
            </div>

            <div>
                <div class="hero-stat-value">
                    {fraud_rate:.1%}
                </div>
                <div class="hero-stat-label">
                    alert rate
                </div>
            </div>

        </div>

    </div>
    """
)


# =========================================================
# KPI CARDS
# =========================================================

metric_1, metric_2, metric_3, metric_4 = st.columns(
    4,
    gap="medium"
)

with metric_1:

    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-icon">↗</div>
            <div class="metric-label">
                Transaction volume
            </div>
            <div class="metric-value">
                £{transaction_volume:,.0f}
            </div>
            <div class="metric-foot">
                Last {total_transactions} scored payments
            </div>
        </div>
        """
    )


with metric_2:

    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-icon">◇</div>
            <div class="metric-label">
                Average risk
            </div>
            <div class="metric-value">
                {average_risk:.1%}
            </div>
            <div class="metric-foot">
                Model fraud probability
            </div>
        </div>
        """
    )


with metric_3:

    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-icon">!</div>
            <div class="metric-label">
                Fraud alerts
            </div>
            <div class="metric-value">
                {fraud_count}
            </div>
            <div class="metric-foot">
                Transactions requiring review
            </div>
        </div>
        """
    )


with metric_4:

    st.html(
        f"""
        <div class="metric-card">
            <div class="metric-icon">✓</div>
            <div class="metric-label">
                API status
            </div>
            <div class="metric-value">
                {"Live" if api_online else "Down"}
            </div>
            <div class="metric-foot">
                FastAPI scoring service
            </div>
        </div>
        """
    )


st.write("")
st.write("")


# =========================================================
# SCORE TRANSACTION
# =========================================================

st.html(
    """
    <div class="section-title">
        Risk check
    </div>

    <div class="section-caption">
        Analyse a payment before approving the transaction.
    </div>
    """
)


form_column, result_column = st.columns(
    [1.65, 1],
    gap="large",
)


# =========================================================
# FORM
# =========================================================

with form_column:

    with st.container(
        key="score_panel"
    ):

        st.markdown("#### New transaction")

        st.caption(
            "Enter the transaction information received by the payment system."
        )

        top_left, top_right = st.columns(2)

        with top_left:

            transaction_type = st.selectbox(
                "Transaction type",
                [
                    "TRANSFER",
                    "CASH_OUT",
                    "PAYMENT",
                    "DEBIT",
                    "CASH_IN",
                ],
            )

        with top_right:

            step = st.number_input(
                "Time step",
                min_value=0,
                value=356,
                step=1,
            )


        amount = st.number_input(
            "Payment amount",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            format="%.2f",
        )


        customer_left, customer_right = st.columns(2)

        with customer_left:

            name_orig = st.text_input(
                "Sender ID",
                value="C100001",
            )

            old_balance_orig = st.number_input(
                "Sender balance",
                min_value=0.0,
                value=5000.0,
                step=100.0,
                format="%.2f",
            )


        with customer_right:

            name_dest = st.text_input(
                "Recipient ID",
                value="C200001",
            )

            old_balance_dest = st.number_input(
                "Recipient balance",
                min_value=0.0,
                value=100.0,
                step=100.0,
                format="%.2f",
            )


        st.write("")

        analyse = st.button(
            "Analyse payment  →",
            type="primary",
            use_container_width=True,
        )


        if analyse:

            payload = {
                "step": int(step),
                "transaction_type": transaction_type,
                "amount": float(amount),
                "name_orig": name_orig,
                "old_balance_orig": float(old_balance_orig),
                "name_dest": name_dest,
                "old_balance_dest": float(old_balance_dest),
            }

            try:

                with st.spinner(
                    "Running fraud model..."
                ):

                    result = score_transaction(
                        payload
                    )

                st.session_state.prediction = result

                st.rerun()

            except requests.RequestException as error:

                st.error(
                    f"Prediction API error: {error}"
                )


# =========================================================
# PREDICTION PANEL
# =========================================================

with result_column:

    prediction = st.session_state.prediction

    if prediction:

        probability = float(
            prediction["fraud_probability"]
        )

        predicted_fraud = bool(
            prediction["predicted_fraud"]
        )

        percentage = probability * 100

        if probability >= 0.75:

            risk_label = "HIGH RISK"
            risk_color = "#ff5263"
            risk_background = "rgba(255,82,99,.15)"
            description = (
                "The model detected a strong fraud signal. "
                "This transaction should be manually reviewed "
                "before approval."
            )

        elif probability >= 0.35:

            risk_label = "REVIEW"
            risk_color = "#ffb020"
            risk_background = "rgba(255,176,32,.15)"
            description = (
                "The transaction contains unusual signals. "
                "Additional verification may be appropriate."
            )

        else:

            risk_label = "LOW RISK"
            risk_color = "#40d79c"
            risk_background = "rgba(64,215,156,.15)"
            description = (
                "No strong fraudulent behaviour was identified "
                "by the current model."
            )


        st.html(
            f"""
            <div class="prediction-shell">

                <div class="prediction-label">
                    Fraud probability
                </div>

                <div class="risk-number">
                    {percentage:.1f}%
                </div>

                <div class="risk-track">
                    <div
                        class="risk-fill"
                        style="
                            width:{min(percentage, 100):.1f}%;
                            background:{risk_color};
                        "
                    ></div>
                </div>

                <div
                    class="risk-status"
                    style="
                        color:{risk_color};
                        background:{risk_background};
                    "
                >
                    {risk_label}
                </div>

                <div class="risk-description">
                    {description}
                </div>

                <div class="prediction-id">
                    <span>
                        Transaction
                    </span>

                    <span>
                        #{prediction["transaction_id"]}
                    </span>
                </div>

            </div>
            """
        )

    else:

        st.html(
            """
            <div class="prediction-empty">

                <div>
                    <div class="shield-circle">
                        ◆
                    </div>
                </div>

                <div>
                    <div class="prediction-label">
                        Risk intelligence
                    </div>

                    <div
                        style="
                            font-size:27px;
                            font-weight:720;
                            letter-spacing:-0.8px;
                            margin-top:8px;
                        "
                    >
                        Ready to analyse
                    </div>

                    <div class="risk-description">
                        Submit a transaction to generate
                        a machine-learning fraud score.
                    </div>
                </div>

            </div>
            """
        )


# =========================================================
# TRANSACTIONS
# =========================================================

st.write("")
st.write("")

with st.container(
    key="history_panel"
):

    history_header_left, history_header_right = st.columns(
        [4, 1]
    )

    with history_header_left:

        st.markdown("### Activity")

        st.caption(
            "Latest transactions scored by the fraud engine."
        )

    with history_header_right:

        only_fraud = st.toggle(
            "Fraud only",
            value=False,
        )


    transactions = load_transactions(50)

    if transactions:

        history_df = pd.DataFrame(
            transactions
        )

        if only_fraud:

            history_df = history_df[
                history_df["predicted_fraud"] == True
            ]


        if not history_df.empty:

            history_df["fraud_probability"] = (
                history_df["fraud_probability"]
                .fillna(0)
                .mul(100)
                .round(1)
            )

            history_df["amount"] = (
                history_df["amount"]
                .fillna(0)
                .map(lambda x: f"£{x:,.2f}")
            )

            history_df["Decision"] = (
                history_df["predicted_fraud"]
                .map(
                    {
                        True: "Review",
                        False: "Approved",
                    }
                )
            )

            history_df["created_at"] = (
                pd.to_datetime(
                    history_df["created_at"],
                    errors="coerce",
                )
                .dt.strftime(
                    "%d %b  %H:%M"
                )
            )


            history_df = history_df[
                [
                    "id",
                    "transaction_type",
                    "amount",
                    "name_orig",
                    "name_dest",
                    "fraud_probability",
                    "Decision",
                    "created_at",
                ]
            ]


            history_df.columns = [
                "ID",
                "Type",
                "Amount",
                "From",
                "To",
                "Risk %",
                "Decision",
                "Time",
            ]


            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True,
                height=420,
                column_config={
                    "Risk %": st.column_config.ProgressColumn(
                        "Risk %",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%",
                    ),
                    "Decision": st.column_config.TextColumn(
                        "Decision"
                    ),
                },
            )

        else:

            st.info(
                "No transactions match the selected filter."
            )

    else:

        st.info(
            "No transactions have been scored yet."
        )


# =========================================================
# FOOTER
# =========================================================

st.html(
    f"""
    <div style="
        text-align:center;
        padding-top:34px;
        color:#aaa;
        font-size:11px;
    ">
        Sentinel Fraud Intelligence ·
        Random Forest · FastAPI · PostgreSQL ·
        {datetime.now().year}
    </div>
    """
)