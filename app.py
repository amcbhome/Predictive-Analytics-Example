# ============================================================
# 🌸 Diversification of Risk – Pastel Light Theme (Clean Final)
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

/* ===== CARD STYLING ===== */
.card {
  border: 1.3px solid #D8DEE3;
  border-radius: 12px;
  background-color: #FFFFFF;
  margin-bottom: 18px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
.card-body {
  padding: 12px 16px;
  font-size: 15px;
  color:#36454F !important;
}

/* ===== RADIO BUTTONS ===== */
.stRadio > div { gap: 4px; }
.stRadio label { color: #36454F !important; }

/* ===== SLIDER (NO BACKGROUND) ===== */
div[data-baseweb="slider"] > div {
    background-color: transparent !important;
}
.stSlider label {color:#36454F !important;}

/* ===== TABLE (NO SCROLL) ===== */
[data-testid="stTable"], .stDataFrame iframe {
    background-color: #FFFFFF !important;
    color: #36454F !important;
    border-radius: 8px;
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
def card(title, icon, content=""):
    st.markdown(f"""
    <div class="card">
        <div class="card-header">{icon} {title}</div>
        <div class="card-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 2-COLUMN LAYOUT (Left = Inputs, Right = Outputs)
# ============================================================
left, right = st.columns([1, 2])

# ─────────────────────────────────────────────────────────────
# LEFT COLUMN (INPUTS + CALCULATE BUTTON)
# ─────────────────────────────────────────────────────────────
with left:

    card("Input Data", "📥")

    default_df = pd.DataFrame({
        "X": [6.6, 5.6, -9.0, 12.6, 14.0],
        "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    mode = st.radio("", ["Use Watson & Head", "Enter My Own"], label_visibility="collapsed")

    # Show full table without scroll or height errors
    if mode == "Use Watson & Head":
        df = default_df.copy()
        st.dataframe(df, use_container_width=True)
    else:
        df = st.data_editor(pd.DataFrame({"X":[None]*5, "Y":[None]*5}),
                             num_rows="fixed", use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter 5 values for BOTH X and Y.")
        st.stop()

    # Convert % → decimals
    df = df.astype(float) / 100

    # Weight slider (bottom of column)
    weight_x = st.slider("Weight in Asset X", 0.0, 1.0, 0.5, 0.05)
    weight_y = 1 - weight_x

    # RED CALCULATE BUTTON
    calculate = st.button("Calculate")

# ─────────────────────────────────────────────────────────────
# RIGHT COLUMN (OUTPUTS SHOWN ONLY AFTER CLICK)
# ─────────────────────────────────────────────────────────────
if calculate:

    # Portfolio statistics
    mean_x, mean_y = df.mean()
    sd_x, sd_y = df.std(ddof=0)
    corr = df["X"].corr(df["Y"])

    port_return = weight_x * mean_x + weight_y * mean_y
    port_var = (weight_x**2 * sd_x**2) + (weight_y**2 * sd_y**2) + \
               (2 * weight_x * weight_y * sd_x * sd_y * corr)
    port_sd = np.sqrt(port_var)

    with right:
        # Open card
        st.markdown("""
        <div class='card'>
            <div class='card-header'>📈 Efficient Frontier</div>
            <div class='card-body'>
        """, unsafe_allow_html=True)

        # Correlation displayed under header
        st.markdown(f"<b>Correlation (r):</b> {corr:.2f}", unsafe_allow_html=True)

        # Efficient frontier graph
        w = np.linspace(0, 1, 50)
        pf_returns = w * mean_x + (1-w) * mean_y
        pf_sd = np.sqrt(w**2*sd_x**2 + (1-w)**2*sd_y**2 + 2*w*(1-w)*sd_x*sd_y*corr)

        plt.style.use("seaborn-v0_8-whitegrid")
        fig, ax = plt.subplots(figsize=(8,5))
        ax.plot(pf_sd*100, pf_returns*100, linewidth=2, color="#5E9BD4",
                label="Efficient Frontier")
        ax.scatter(port_sd*100, port_return*100, color="#F5796C", s=60,
                   label="Current Portfolio")

        ax.set_facecolor("#FFFFFF")
        ax.set_xlabel("Risk (Std Dev %)")
        ax.set_ylabel("Expected Return (%)")
        ax.legend()
        st.pyplot(fig)

        # Close card wrapper
        st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================
# END OF APP
# ============================================================
