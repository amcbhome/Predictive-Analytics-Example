# ============================================================
# 🌸 Diversification of Risk Dashboard (3-Column Final Version)
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

# ============================================================
# 🎨 FULL RESPONSIVE PASTEL THEME
# ============================================================
st.markdown("""
<style>

body, .block-container {
    background-color: #FAFAFA;
    font-family: 'Segoe UI', sans-serif;
    color: #36454F;
}

/* SOFT TAB HEADER */
.soft-tab {
  display: inline-block;
  padding: 10px 18px;
  font-weight: 600;
  font-size: 18px;
  border: 1.5px solid #D0DAE2;
  background-color: #E8F3FF;
  color: #336699 !important;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border-bottom: none;
  margin-right: 8px;
  box-shadow: 0 -1px 4px rgba(0,0,0,0.04);
}

/* FORMULA AREA CLEAN (NO BORDER/BOX) */
.tab-card {
  padding: 0px;
  background-color: transparent;
  border: none;
  box-shadow: none;
  margin-top: -5px;
}

/* 🎯 Responsive formula scaling (only on small screens) */
.calc-line {
    font-size: 11px;
    line-height: 1.1;
}
@media (max-width: 700px) {
  .calc-line {
      font-size: 9px;
  }
}

/* SLIDER BACKGROUND REMOVED */
div[data-baseweb="slider"] > div {
    background-color: transparent !important;
}

/* RED BUTTON */
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

# ============================================================
# TAB HELPER
# ============================================================
def soft_tab(title, icon):
    st.markdown(f"<div class='soft-tab'>{icon} {title}</div>", unsafe_allow_html=True)

# ============================================================
# 📌 LAYOUT (NOW 3 COLUMNS: INPUT | OUTPUT | GRAPH)
# ============================================================
col1, col_mid, col2 = st.columns([0.6, 0.6, 3.0])

# ============================================================
# LEFT COLUMN — INPUT
# ============================================================
with col1:

    soft_tab("Input", "📥")

    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    df = st.data_editor(default_df, use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter five numeric % values for both X and Y.")
        st.stop()

    df = df.astype(float) / 100
    weight_x = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.05)
    weight_y = 1 - weight_x

    calculate = st.button("Calculate")

# ============================================================
# MIDDLE COLUMN — OUTPUT LABEL ONLY
# ============================================================
with col_mid:
    soft_tab("Output", "📊")  # Title only, no border, no content

# ============================================================
# RIGHT COLUMN — CHART + METRICS
# ============================================================
if calculate:

    # Stats
    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])

    port_return = weight_x * mean_x + weight_y * mean_y
    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) \
               + (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    with col2:

        soft_tab("Efficient Frontier", "📈")

        # —— Equation Line —— 
        st.markdown("<div class='tab-card'>", unsafe_allow_html=True)
        st.markdown(
            "<div class='calc-line'>"
            +
            fr"$r={corr:.2f}$"
            " &nbsp;&nbsp;|&nbsp;&nbsp; "
            +
            fr"$\bar{{X}}={mean_x*100:.2f}\%$"
            " , "
            +
            fr"$\bar{{Y}}={mean_y*100:.2f}\%$"
            " &nbsp;&nbsp;|&nbsp;&nbsp; "
            +
            fr"$\sigma_X={sd_x*100:.2f}\%$"
            " , "
            +
            fr"$\sigma_Y={sd_y*100:.2f}\%$"
            " &nbsp;&nbsp;|&nbsp;&nbsp; "
            +
            fr"$E(R_p)={port_return*100:.2f}\%$"
            " &nbsp;&nbsp;|&nbsp;&nbsp; "
            +
            fr"$\sigma_p={port_sd*100:.2f}\%$"
            +
            "</div>",
            unsafe_allow_html=True
        )

        # —— Efficient Frontier Plot —— 
        w = np.linspace(0, 1, 50)
        pf_returns = w * mean_x + (1 - w) * mean_y
        pf_sd = np.sqrt(
            w**2 * sd_x**2 +
            (1 - w)**2 * sd_y**2 +
            2 * w * (1 - w) * sd_x * sd_y * corr
        )

        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(pf_sd*100, pf_returns*100, linewidth=2, color="#5E9BD4", label="Efficient Frontier")
        ax.scatter(port_sd*100, port_return*100, color="#F5796C", s=50, label="Current Portfolio")

        ax.set_facecolor("#FFFFFF")
        ax.set_xlabel("Risk (Std Dev %)", fontsize=10)
        ax.set_ylabel("Expected Return (%)", fontsize=10)
        ax.tick_params(axis='both', labelsize=9)
        ax.legend(fontsize=9)

        st.pyplot(fig)

        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# END OF APP
# ============================================================

