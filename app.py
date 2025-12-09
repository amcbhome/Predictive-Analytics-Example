# ============================================================
# 🌸 Diversification of Risk – Pastel Light Theme (W&H Default)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Diversification App", layout="wide")

st.markdown("""
<h1 style='
    color:#36454F;
    font-family: Segoe UI, sans-serif;
    font-weight: 650;
'>📊 Diversification of Risk Dashboard</h1>
""", unsafe_allow_html=True)

# ======== PASTEL LIGHT THEME STYLE ==========
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body, .block-container {
    background-color: #FAFAFA;
    font-family: 'Segoe UI', sans-serif;
    color: #36454F;
}

/* ===== CARD ===== */
.card {
  border: 1.3px solid #D8DEE3;
  border-radius: 12px;
  background-color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-bottom: 18px;
}
.card-header {
  background-color: #E8F3FF;
  padding: 10px 14px;
  font-weight: 600;
  font-size: 18px;
  border-bottom: 1.3px solid #C9D5E1;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  color: #336699 !important;
}
.card-body { padding: 12px 16px; }

/* ===== SLIDER NO BACKGROUND ===== */
div[data-baseweb="slider"] > div {
    background-color: transparent !important;
}

/* ===== RED CALCULATE BUTTON ===== */
.stButton > button {
    background-color: #E57373 !important;
    color: white !important;
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid #CC5B5B !important;
}
.stButton > button:hover {
    background-color: #CC5B5B !important;
}

</style>
""", unsafe_allow_html=True)


# ======== CARD FUNCTION ==========
def card(title, icon, body_html=""):
    st.markdown(f"""
    <div class="card">
        <div class="card-header">{icon} {title}</div>
        <div class="card-body">
            {body_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LAYOUT (Left Input, Right Output)
# ============================================================
left, right = st.columns([1, 2])

# ─────────────────────────────────────────────────────────────
# LEFT COLUMN — INPUT TABLE + SLIDER + BUTTON
# ─────────────────────────────────────────────────────────────
with left:

    card("Input Data (X & Y Returns)", "📥")

    # Watson & Head (8th Edition Corporate Finance)
    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    df = st.data_editor(default_df, use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter 5 percentage values for BOTH X and Y.")
        st.stop()

    # IMPORTANT: Convert user % → decimals
    df = df.astype(float) / 100

    # Weight slider
    weight_x = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.05)
    weight_y = 1 - weight_x

    # Calculate button
    calculate = st.button("Calculate")


# ─────────────────────────────────────────────────────────────
# RIGHT COLUMN — ONLY SHOW AFTER BUTTON CLICK
# ─────────────────────────────────────────────────────────────
if calculate:

    # Statistics
    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])

    # Portfolio algebra
    port_return = weight_x * mean_x + weight_y * mean_y
    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) + \
               (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    # ──────────────────────────────────────
    # OUTPUT CARD
    # ──────────────────────────────────────
    with right:
        st.markdown("""
        <div class='card'>
            <div class='card-header'>📈 Efficient Frontier</div>
            <div class='card-body'>
        """, unsafe_allow_html=True)

        # Statistics section with algebra
        st.markdown(f"""
        <b>Correlation (r):</b> {corr:.2f}<br><br>

        <b>Mean Returns:</b>  \( \\bar{{X}} = {mean_x*100:.2f}\\%, \quad \\bar{{Y}} = {mean_y*100:.2f}\\% \)<br>
        <b>Risk (Std Dev):</b>  \( \\sigma_X = {sd_x*100:.2f}\\%, \quad \\sigma_Y = {sd_y*100:.2f}\\% \)<br><br>

        <b>Portfolio Expected Return:</b><br>
        \( E(R_p) = w_X\\bar{{X}} + w_Y\\bar{{Y}} \)<br>
        → **{port_return*100:.2f}%**<br><br>

        <b>Portfolio Risk:</b><br>
        \( \\sigma_p = \\sqrt{{ w_X^2\\sigma_X^2 + w_Y^2\\sigma_Y^2 + 2w_Xw_Y\\sigma_X\\sigma_Yr }} \)<br>
        → **{port_sd*100:.2f}%**
        """, unsafe_allow_html=True)

        # Graph — Efficient Frontier
        w = np.linspace(0, 1, 50)
        pf_returns = w * mean_x + (1-w) * mean_y
        pf_sd = np.sqrt(w**2*sd_x**2 + (1-w)**2*sd_y**2 + 2*w*(1-w)*sd_x*sd_y*corr)

        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(pf_sd*100, pf_returns*100, linewidth=2, color="#5E9BD4", label="Efficient Frontier")
        ax.scatter(port_sd*100, port_return*100, color="#F5796C", s=60, label="Current Portfolio")

        ax.set_facecolor("#FFFFFF")
        ax.set_xlabel("Risk (Std Dev %)")
        ax.set_ylabel("Expected Return (%)")
        ax.legend()
        st.pyplot(fig)

        st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================
# END OF APP
# ============================================================

