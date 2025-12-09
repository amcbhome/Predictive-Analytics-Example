import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diversification App", layout="wide")
st.title("📊 Diversification of Risk – All-in-One Dashboard")

# ============================================================
# LAYOUT GRID (3 columns)
# ============================================================
col1, col2, col3 = st.columns([1.2, 1, 1.5])   # width ratios

# ─────────────────────────────────────────────────────────────
#  COLUMN 1 → DATA + RESULTS TABLE
# ─────────────────────────────────────────────────────────────
with col1:
    st.subheader("📥 Enter Data")
    default_df = pd.DataFrame({
        "S": [6.6, 5.6, -9.0, 12.6, 14.0],
        "T": [24.5, -5.9, 19.9, -7.8, 14.8]
    })
    
    mode = st.radio("", ["Use Watson & Head Data", "Enter My Own"], label_visibility="collapsed")

    if mode == "Use Watson & Head Data":
        df = default_df.copy()
        st.dataframe(df, use_container_width=True)
    else:
        df = st.data_editor(pd.DataFrame({"S":[None]*5, "T":[None]*5}),
                             num_rows="fixed", use_container_width=True)

    if df.isnull().any().any():
        st.warning("Enter 5 values for S and T to continue.")
        st.stop()

    df = df.astype(float) / 100  # convert % to decimals

    # stats
    mean_s, mean_t = df.mean()
    sd_s, sd_t = df.std(ddof=0)
    corr = df["S"].corr(df["T"])

    # TABLE OUTPUT
    st.subheader("📊 Results Table")
    summary = pd.DataFrame({
        "Mean Return (%)": [mean_s*100, mean_t*100],
        "Std Dev (%)": [sd_s*100, sd_t*100]
    }, index=["S", "T"]).round(2)
    st.dataframe(summary, use_container_width=True)
    

# ─────────────────────────────────────────────────────────────
#  COLUMN 2 → CORRELATION + WEIGHTS
# ─────────────────────────────────────────────────────────────
with col2:
    st.subheader("🔗 Correlation")
    st.metric("r (S,T)", f"{corr:.2f}")

    st.subheader("⚖️ Portfolio Weights")
    weight_s = st.slider("Weight in Asset S", 0.0, 1.0, 0.5, 0.05)
    weight_t = 1 - weight_s
    st.write(f"**S = {weight_s:.2f}**, **T = {weight_t:.2f}**")

    # Calculate current portfolio stats
    port_return = weight_s * mean_s + weight_t * mean_t
    port_var = (weight_s**2 * sd_s**2) + (weight_t**2 * sd_t**2) + \
               (2 * weight_s * weight_t * sd_s * sd_t * corr)
    port_sd = np.sqrt(port_var)

    st.metric("Portfolio Risk (Std Dev %)", f"{port_sd*100:.2f}")


# ─────────────────────────────────────────────────────────────
#  COLUMN 3 → GRAPH
# ─────────────────────────────────────────────────────────────
with col3:
    st.subheader("📈 Efficient Frontier")

    # smooth curve
    w = np.linspace(0, 1, 50)
    pf_returns = w * mean_s + (1-w) * mean_t
    pf_sd = np.sqrt(w**2*sd_s**2 + (1-w)**2*sd_t**2 + 2*w*(1-w)*sd_s*sd_t*corr)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(pf_sd*100, pf_returns*100, label="Efficient Frontier")
    ax.scatter(port_sd*100, port_return*100, color="red", label="Current Portfolio")
    ax.set_xlabel("Risk (Std Dev %)")
    ax.set_ylabel("Expected Return (%)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # diversification message
    min_risk = min(pf_sd) * 100
    st.success(f"Minimum achievable risk: **{min_risk:.2f}%**")

