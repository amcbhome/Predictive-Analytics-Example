# ============================================================
# 🌸 Diversification of Risk Dashboard (Large Input/Output Text)
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
    margin-bottom: 0;
    font-size: 32px;
'>📊 Diversification of Risk Dashboard</h1>
""", unsafe_allow_html=True)

# ============================================================
# 🎨 STYLE: PASTEL + LARGER I/O TEXT (18px)
# ============================================================
st.markdown("""
<style>

body, .block-container {
    background-color: #FAFAFA;
    font-family: 'Segoe UI', sans-serif;
    color: #36454F;
}

/* 🔹 STANDARD APP TEXT REMAINS */
body, .block-container, .stMarkdown, .stText, .stSlider {
    font-size: 14px;
}

/* 🔸 ENLARGED INPUT + OUTPUT TEXT */
.large-io {
    font-size: 18px !important;
    font-weight: 500;
}

/* 🏷️ Soft Tab Headers */
.soft-tab {
  display: inline-block;
  padding: 8px 16px;
  font-weight: 600;
  font-size: 18px;
  border: 1.5px solid #D0DAE2;
  background-color: #E8F3FF;
  color: #336699 !important;
  border-radius: 14px 14px 0px 0px;
  border-bottom: none;
  margin-bottom: 0;
}

/* 🧮 Output Lines */
.output-line {
    font-size: 18px !important;
    line-height: 1.4;
    margin: 4px 0;
}

/* 🛠 Increase slider label + values */
.stSlider label, .stSlider .css-1y4p8pa {
    font-size: 18px !important;
}

/* 🧾 Data Editor font increase */
[data-testid="stDataFrame"] * {
    font-size: 18px !important;
}

/* 🔘 Red Button */
.stButton > button {
    background-color: #E57373 !important;
    color: white !important;
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid #CC5B5B !important;
    padding: 0.45rem 0.8rem;
    font-size: 16px !important;
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
# 📌 LAYOUT (INPUT | OUTPUT | GRAPH)
# ============================================================
col1, col_mid, col2 = st.columns([0.6, 0.6, 3.0])

# ============================================================
# 🟦 LEFT COLUMN — INPUT
# ============================================================
with col1:
    soft_tab("Input", "📥")

    st.markdown("<div class='large-io'>Enter or edit your returns:</div>", unsafe_allow_html=True)

    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    df = st.data_editor(default_df, use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter five numeric % values for both X and Y.")
        st.stop()

    df = df.astype(float) / 100

    st.markdown("<br>", unsafe_allow_html=True)
    weight_x = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.05)
    weight_y = 1 - weight_x

    calculate = st.button("Calculate")

# ============================================================
# 🟨 MIDDLE COLUMN — OUTPUT BOX
# ============================================================
with col_mid:
    soft_tab("Output", "📊")

# ============================================================
# 🟥 RIGHT COLUMN — GRAPH + CALCULATIONS
# ============================================================
if calculate:

    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])
    port_return = weight_x * mean_x + weight_y * mean_y

    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) \
               + (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    # ================= OUTPUT TEXT ================= #
    with col_mid:
        st.markdown(f"<div class='output-line'>Correlation: {corr:.2f}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Mean X: {mean_x*100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Mean Y: {mean_y*100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Std Dev X: {sd_x*100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Std Dev Y: {sd_y*100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Portfolio Return: {port_return*100:.2f}%</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-line'>Portfolio Risk: {port_sd*100:.2f}%</div>", unsafe_allow_html=True)

    # ================= GRAPH ================= #
    with col2:
        soft_tab("Efficient Frontier", "📈")

        w = np.linspace(0, 1, 50)
        pf_returns = w * mean_x + (1 - w) * mean_y
        pf_sd = np.sqrt(
            w**2 * sd_x**2 +
            (1 - w)**2 * sd_y**2 +
            2 * w * (1 - w) * sd_x * sd_y * corr
        )

        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(6.5, 3.5))

        ax.plot(pf_sd*100, pf_returns*100, linewidth=1.8, color="#5E9BD4")
        ax.scatter(port_sd*100, port_return*100, color="#F5796C", s=45)

        ax.set_facecolor("#FFFFFF")
        ax.set_xlabel("Risk (Std Dev %)")
        ax.set_ylabel("Expected Return (%)")

        st.pyplot(fig)

# ============================================================
# END OF APP
# ============================================================
