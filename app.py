# ============================================================
# 📌 Diversification of Risk – Business Theme (Streamlit)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Diversification App", layout="wide")

st.markdown("<h1 style='color:#E8E8E8;'>📊 Diversification of Risk Dashboard</h1>", 
            unsafe_allow_html=True)

# ======== BUSINESS THEME STYLE ==========
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body, .block-container {
    background-color: #1C1F23;
    color: #EAEAEA;
}

/* ===== TEXT COLORS ===== */
h1,h2,h3,h4,p,div, label, span {
    color: #E8E8E8 !important;
}

/* ===== CARD DESIGN ===== */
.card {
  border: 1.5px solid #2F3238;
  border-radius: 10px;
  background-color: #23272B;
  margin-bottom: 15px;
}

/* ===== CARD HEADER ===== */
.card-header {
  background-color: #2A2E33;
  padding: 10px 14px;
  font-weight: 600;
  font-size: 18px;
  border-bottom: 1.5px solid #40454D;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  color: #8AC7FF !important;
}

/* ===== CARD BODY ===== */
.card-body {
  padding: 12px 14px;
  font-size: 15px;
}

/* ===== RADIO ===== */
.stRadio > div { gap: 6px; }
.stRadio label { color: #E8E8E8 !important; font-weight:500; }

/* ===== SLIDER ===== */
div[data-baseweb="slider"] > div {
    background-color: #0078D4 !important;
}

/* ===== DATAFRAME ===== */
[data-testid="stTable"], .stDataFrame iframe {
    background-color: #2A2E33 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ======== CARD FUNCTION ==========
def card(title, icon, content=""):
    return st.markdown(f"""
    <div class="card">
        <div class="card-header">{icon} {title}</div>
        <div class="card-body">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GRID LAYOUT (3 Columns)
# ============================================================
col1, col2, col3 = st.columns([1.3, 1, 1.4])

# ─────────────────────────────────────────────────────────────
# COLUMN 1 → DATA ENTRY
# ─────────────────────────────────────────────────────────────
with col1:
    card("Input Data", "📥")

    default_df = pd.DataFrame({
        "S": [6.6, 5.6, -9.0, 12.6, 14.0],
        "T": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    mode = st.radio("", ["Use Watson & Head", "Enter My Own"], label_visibility="collapsed")

    if mode == "Use Watson & Head":
        df = default_df.copy()
        st.dataframe(df, use_container_width=True, height=160)
    else:
        df = st.data_editor(pd.DataFrame({"S":[None]*5, "T":[None]*5}),
                             num_rows="fixed", use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter 5 values for BOTH S and T.")
        st.stop()

    df = df.astype(float) / 100    # Convert to decimals

    # Basic stats
    mean_s, mean_t = df.mean()
    sd_s, sd_t = df.std(ddof=0)
    corr = df["S"].corr(df["T"])

# ─────────────────────────────────────────────────────────────
# COLUMN 2 → CORRELATION + WEIGHTS
# ─────────────────────────────────────────────────────────────
with col2:
    # CORRELATION CARD
    card("Correlation Analysis", "🔗", f"<b>Correlation (r):</b> {corr:.2f}")

    # WEIGHTS
    weight_s = st.slider("Weight in Asset S", 0.0, 1.0, 0.5, 0.05)
    weight_t = 1 - weight_s
    card("Portfolio Weights", "⚖️", f"S = {weight_s:.2f}, T = {weight_t:.2f}")

    # Portfolio Calculations
    port_return = weight_s * mean_s + weight_t * mean_t
    port_var = (weight_s**2 * sd_s**2) + (weight_t**2 * sd_t**2) + \
               (2 * weight_s * weight_t * sd_s * sd_t * corr)
    port_sd = np.sqrt(port_var)

# ─────────────────────────────────────────────────────────────
# COLUMN 3 → GRAPH + RESULT
# ─────────────────────────────────────────────────────────────
with col3:
    card("Efficient Frontier", "📈")

    # Efficient Frontier Curve
    w = np.linspace(0, 1, 50)
    pf_returns = w * mean_s + (1-w) * mean_t
    pf_sd = np.sqrt(w**2*sd_s**2 + (1-w)**2*sd_t**2 + 2*w*(1-w)*sd_s*sd_t*corr)

    # Business theme graph
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6,4))

    ax.plot(pf_sd*100, pf_returns*100, linewidth=2, color="#3EA6FF", label="Efficient Frontier")
    ax.scatter(port_sd*100, port_return*100, color="#FF4B4B", s=60, label="Current Portfolio")

    ax.set_facecolor("#23272B")
    ax.set_xlabel("Risk (Std Dev %)")
    ax.set_ylabel("Expected Return (%)")
    ax.grid(color="#555", linestyle="--", alpha=0.5)
    ax.legend()

    st.pyplot(fig)

    # Minimum Risk Summary
    min_risk = min(pf_sd) * 100
    card("Diversification Benefit", "📉",
         f"<b>Minimum achievable risk:</b> {min_risk:.2f}%<br>"
         f"(S = {sd_s*100:.2f}%, T = {sd_t*100:.2f}%)")

# ============================================================
# END OF APP
# ============================================================
