# ============================================================
# 🌸 Diversification of Risk Dashboard (Matching Tables Version)
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
# 🎨 STYLE: PASTEL UI + MATCHING TABLES (NO INDEX)
# ============================================================
st.markdown("""
<style>

body, .block-container {
    background-color: #FAFAFA;
    font-family: 'Segoe UI', sans-serif;
    color: #36454F;
}

/* Soft Tab Headers */
.soft-tab {
  display: inline-block;
  padding: 8px 16px;
  font-weight: 700;
  font-size: 18px;
  border: 1.5px solid #D0DAE2;
  background-color: #E8F3FF;
  color: #336699 !important;
  border-radius: 14px 14px 0px 0px;
  border-bottom: none;
  margin-bottom: 0;
}

/* Matching table styling */
.table-box table {
    font-size: 18px !important;
    width: 100%;
}

/* Center headers + values */
.table-box th {
    text-align: center !important;
    font-weight: 700 !important;
    font-size: 18px;
}
.table-box td {
    text-align: center !important;
    padding: 6px 10px !important;
    font-size: 18px;
}

/* 🔘 Bold red Calculate */
.stButton > button {
    background-color: #E53935 !important;
    color: white !important;
    border-radius: 10px;
    font-weight: 800;
    border: 2px solid #B71C1C !important;
    padding: 0.5rem 1rem;
    font-size: 18px !important;
}
.stButton > button:hover {
    background-color: #B71C1C !important;
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
col1, col_mid, col2 = st.columns([0.9, 0.9, 3])

# ============================================================
# 🟦 LEFT COLUMN — FORMATTED INPUT TABLE + CONTROLS
# ============================================================
with col1:
    soft_tab("Input", "📥")

    st.write("Enter or edit your returns:")

    # Original data
    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    # Input editor without index column
    df = st.data_editor(
        default_df,
        use_container_width=True,
        hide_index=True
    )

    if df.isnull().any().any():
        st.warning("⚠ Please enter numeric % values for both X and Y.")
        st.stop()

    # Convert to decimals
    df = df.astype(float) / 100

    weight_x = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.01)
    weight_y = 1 - weight_x

    calculate = st.button("Calculate")

# ============================================================
# 🟨 MIDDLE COLUMN — MATCHING OUTPUT TABLE (NO INDEX)
# ============================================================
with col_mid:
    soft_tab("Output", "📊")

# ============================================================
# 🟥 RIGHT COLUMN — GRAPH
# ============================================================
if calculate:

    # ================= CALCULATIONS ================= #
    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])
    port_return = weight_x * mean_x + weight_y * mean_y

    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) \
               + (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    # ================= OUTPUT TABLE ================= #
    summary_df = pd.DataFrame({
        "Metric": [
            "Correlation",
            "Mean X",
            "Mean Y",
            "Std Dev X",
            "Std Dev Y",
            "Portfolio Return",
            "Portfolio Risk"
        ],
        "Value (%)": [
            f"{corr*100:.2f}%",
            f"{mean_x*100:.2f}%",
            f"{mean_y*100:.2f}%",
            f"{sd_x*100:.2f}%",
            f"{sd_y*100:.2f}%",
            f"{port_return*100:.2f}%",
            f"{port_sd*100:.2f}%"
        ]
    })

    with col_mid:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='table-box'>", unsafe_allow_html=True)
        st.table(summary_df)  # no index automatically
        st.markdown("</div>", unsafe_allow_html=True)

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
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(pf_sd*100, pf_returns*100, linewidth=2.0, color="#5E9BD4")
        ax.scatter(port_sd*100, port_return*100, color="#E53935", s=60)

        ax.set_xlabel("Risk (Std Dev %)")
        ax.set_ylabel("Expected Return (%)")

        st.pyplot(fig)

# ============================================================
# END OF APP
# ============================================================
