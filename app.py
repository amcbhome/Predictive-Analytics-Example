import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────────────────────
# Page Setup
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Diversification App", layout="wide")
st.title("📊 Diversification of Risk – Dashboard")

# ====== STYLE: BORDER BOXES ======
BOX_STYLE = """
    <div style="
        border:2px solid #888;
        border-radius:10px;
        padding:12px;
        margin-bottom:15px;
        background-color:#fdfdfd;">
        {content}
    </div>
"""

# ============================================================
# GRID LAYOUT (3 Columns)
# ============================================================
col1, col2, col3 = st.columns([1.2, 1, 1.4])


# ─────────────────────────────────────────────────────────────
# COLUMN 1 → DATA ENTRY
# ─────────────────────────────────────────────────────────────
with col1:
    st.markdown(BOX_STYLE.format(content="<h3>📥 Input Data</h3>"), unsafe_allow_html=True)

    default_df = pd.DataFrame({
        "S": [6.6, 5.6, -9.0, 12.6, 14.0],
        "T": [24.5, -5.9, 19.9, -7.8, 14.8]
    })

    mode = st.radio("", ["Use Watson & Head", "Enter My Own"], label_visibility="collapsed")

    if mode == "Use Watson & Head":
        df = default_df.copy()
        st.dataframe(df, use_container_width=True)
    else:
        df = st.data_editor(pd.DataFrame({"S":[None]*5, "T":[None]*5}),
                             num_rows="fixed", use_container_width=True)

    if df.isnull().any().any():
        st.warning("⚠ Please enter 5 values for BOTH S and T.")
        st.stop()

    df = df.astype(float) / 100  # convert % → decimals

    # Calculate statistics
    mean_s, mean_t = df.mean()
    sd_s, sd_t = df.std(ddof=0)
    corr = df["S"].corr(df["T"])


# ─────────────────────────────────────────────────────────────
# COLUMN 2 → CORRELATION + WEIGHTS
# ─────────────────────────────────────────────────────────────
with col2:
    # CORRELATION BOX
    corr_box = f"""
        <h3>🔗 Correlation Analysis</h3>
        <p><b>Correlation (r):</b> {corr:.2f}</p>
    """
    st.markdown(BOX_STYLE.format(content=corr_box), unsafe_allow_html=True)

    # WEIGHT BOX
    weight_box_html = "<h3>⚖️ Portfolio Weights</h3>"
    st.markdown(BOX_STYLE.format(content=weight_box_html), unsafe_allow_html=True)

    weight_s = st.slider("Weight in S", 0.0, 1.0, 0.5, 0.05)
    weight_t = 1 - weight_s
    st.write(f"**S = {weight_s:.2f}**, **T = {weight_t:.2f}**")

    # Portfolio stats
    port_return = weight_s * mean_s + weight_t * mean_t
    port_var = (weight_s**2 * sd_s**2) + (weight_t**2 * sd_t**2) + \
               (2 * weight_s * weight_t * sd_s * sd_t * corr)
    port_sd = np.sqrt(port_var)


# ─────────────────────────────────────────────────────────────
# COLUMN 3 → GRAPH + DIVERSIFICATION RESULT
# ─────────────────────────────────────────────────────────────
with col3:
    # GRAPH BORDER
    st.markdown(BOX_STYLE.format(content="<h3>📈 Efficient Frontier</h3>"), unsafe_allow_html=True)

    w = np.linspace(0, 1, 50)
    pf_returns = w * mean_s + (1-w) * mean_t
    pf_sd = np.sqrt(w**2*sd_s**2 + (1-w)**2*sd_t**2 + 2*w*(1-w)*sd_s*sd_t*corr)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(pf_sd*100, pf_returns*100, linewidth=2, label="Efficient Frontier")
    ax.scatter(port_sd*100, port_return*100, color="red", s=50, label="Current Portfolio")
    ax.set_xlabel("Risk (Std Dev %)")
    ax.set_ylabel("Expected Return (%)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # MINIMUM RISK BOX
    min_risk = min(pf_sd) * 100
    div_text = f"""
        <h3>📉 Diversification Benefit</h3>
        <p><b>Minimum achievable risk:</b> {min_risk:.2f}%<br>
        (compared to S = {sd_s*100:.2f}% and T = {sd_t*100:.2f}%)</p>
    """
    st.markdown(BOX_STYLE.format(content=div_text), unsafe_allow_html=True)
