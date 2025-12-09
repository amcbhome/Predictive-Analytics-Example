# ============================================================
# 🌸 Diversification of Risk – Soft Tabs + Watson & Head Data
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
# 🎨 PASTEL SOFT TAB THEME
# ============================================================
st.markdown("""
<style>

/* BACKGROUND */
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

/* TAB BODY (CARD) */
.tab-card {
  border: 1.5px solid #D0DAE2;
  border-radius: 0px 10px 10px 10px;
  background-color: #FFFFFF;
  padding: 14px 18px;
  margin-top: -10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* SLIDER (NO COLORED BAR BACKGROUND) */
div[data-baseweb="slider"] > div {
    background-color: transparent !important;
}

/* RED CALCULATE BUTTON */
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
# SOFT TAB FUNCTIONS
# ============================================================
def soft_tab(title, icon):
    st.markdown(f"<div class='soft-tab'>{icon} {title}</div>", unsafe_allow_html=True)

def tab_body(html=""):
    st.markdown(f"<div class='tab-card'>{html}</div>", unsafe_allow_html=True)

# ============================================================
# 2 COLUMN LAYOUT
# ============================================================
left, right = st.columns([1, 2])

# ============================================================
# LEFT COLUMN (INPUTS)
# ============================================================
with left:

    soft_tab("Input Data (X & Y Returns)", "📥")

    # Watson & Head 8th Edition Default (Editable Table)
    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    df = st.data_editor(default_df, use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter 5 percentage values for BOTH X and Y.")
        st.stop()

    # Convert % → decimals for calculation
    df = df.astype(float) / 100

    # Portfolio weight slider
    weight_x = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.05)
    weight_y = 1 - weight_x

    # Red Calculate Button
    calculate = st.button("Calculate")

# ============================================================
# RIGHT COLUMN (RESULTS)
# ============================================================
if calculate:

    # Summary statistics
    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])

    # Portfolio return and risk
    port_return = weight_x * mean_x + weight_y * mean_y
    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) \
               + (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    with right:
        # Soft Tab Header
        soft_tab("Efficient Frontier", "📈")

        # STATISTICS + ALGEBRA BOX
        tab_body(f"""
### 📌 Correlation
\( r = {corr:.2f} \)

### 📊 Mean Returns
\( \\bar{{X}} = {mean_x*100:.2f}\\% \quad ; \quad \\bar{{Y}} = {mean_y*100:.2f}\\% \)

### 📉 Risk (Standard Deviation)
\( \\sigma_X = {sd_x*100:.2f}\\% \quad ; \quad \\sigma_Y = {sd_y*100:.2f}\\% \)

### 💼 Portfolio Expected Return
\( E(R_p) = w_X\\bar{{X}} + w_Y\\bar{{Y}} \)\
👉 **{port_return*100:.2f}%**

### ⚠️ Portfolio Risk
\( \\sigma_p = \\sqrt{{ w_X^2\\sigma_X^2 + w_Y^2\\sigma_Y^2 + 2w_Xw_Y\\sigma_X\\sigma_Yr }} \)\
👉 **{port_sd*100:.2f}%**
        """)

        # ============================================================
        # EFFICIENT FRONTIER GRAPH
        # ============================================================
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

# ============================================================
# END OF APP
# ============================================================

