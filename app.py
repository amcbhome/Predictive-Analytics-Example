import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Efficient Frontier Portfolio App", layout="wide")

# -----------------------------  SIDEBAR INPUTS  --------------------------------
st.sidebar.title("🔧 Portfolio Inputs")

st.sidebar.markdown("### 📈 Asset X Daily Returns (5 values)")
x1 = st.sidebar.number_input("X1", value=5.0, step=0.1, format="%.2f")
x2 = st.sidebar.number_input("X2", value=7.0, step=0.1, format="%.2f")
x3 = st.sidebar.number_input("X3", value=8.0, step=0.1, format="%.2f")
x4 = st.sidebar.number_input("X4", value=9.0, step=0.1, format="%.2f")
x5 = st.sidebar.number_input("X5", value=12.0, step=0.1, format="%.2f")

st.sidebar.markdown("### 📉 Asset Y Daily Returns (5 values)")
y1 = st.sidebar.number_input("Y1", value=6.0, step=0.1, format="%.2f")
y2 = st.sidebar.number_input("Y2", value=8.0, step=0.1, format="%.2f")
y3 = st.sidebar.number_input("Y3", value=9.0, step=0.1, format="%.2f")
y4 = st.sidebar.number_input("Y4", value=11.0, step=0.1, format="%.2f")
y5 = st.sidebar.number_input("Y5", value=15.0, step=0.1, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚖️ Portfolio Weights (Must total 100%)")

wx = st.sidebar.number_input("Weight of X (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)
wy = st.sidebar.number_input("Weight of Y (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)

# -------------------------- DATA CONVERSION -------------------------------------
x_values = np.array([x1, x2, x3, x4, x5])
y_values = np.array([y1, y2, y3, y4, y5])

# -------------------------- EF2 MATHEMATICS -------------------------------------
def portfolio_return(w, r1, r2):
    return w * r1 + (1 - w) * r2

def portfolio_risk(w, sd1, sd2, corr):
    cov = corr * sd1 * sd2
    return np.sqrt(w**2 * sd1**2 + (1 - w)**2 * sd2**2 + 2 * w * (1 - w) * cov)

# ---------------------- CALCULATE BUTTON ----------------------------------------
if st.sidebar.button("Calculate Efficient Frontier"):

    if wx + wy != 100:
        st.error("❌ The weights must sum to **100%**.")
    else:
        # Convert user weights to decimals
        w_user = wx / 100

        # Statistics
        mean_x = x_values.mean()
        mean_y = y_values.mean()
        sd_x = x_values.std(ddof=1)
        sd_y = y_values.std(ddof=1)
        corr_xy = np.corrcoef(x_values, y_values)[0][1]

        # Weight range for frontier
        W = np.linspace(0, 1, 100)

        # Efficient Frontier
        ef_returns = portfolio_return(W, mean_x, mean_y)
        ef_risk = portfolio_risk(W, sd_x, sd_y, corr_xy)

        # User portfolio point
        user_return = portfolio_return(w_user, mean_x, mean_y)
        user_risk = portfolio_risk(w_user, sd_x, sd_y, corr_xy)

        # -------------------------- MAIN CHART ---------------------------------
        st.markdown("## 📈 Efficient Frontier (True Portfolio Risk & Return)")
        fig, ax = plt.subplots(figsize=(8, 4.5))

        # Frontier line
        ax.plot(ef_risk, ef_returns, linewidth=2, label="Efficient Frontier")

        # User selected point
        ax.scatter(user_risk, user_return, color='green', s=80, label="Your Portfolio")
        ax.text(user_risk, user_return, f"  (You)", fontsize=9, color='green', va='center')

        # Individual assets
        ax.scatter(sd_x, mean_x, color='blue', s=80, label="Asset X")
        ax.text(sd_x, mean_x, f" X", fontsize=9, color='blue')
        ax.scatter(sd_y, mean_y, color='red', s=80, label="Asset Y")
        ax.text(sd_y, mean_y, f" Y", fontsize=9, color='red')

        # Labels & Grid
        ax.set_xlabel("Risk (Standard Deviation)")
        ax.set_ylabel("Return")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()

        st.pyplot(fig)

        # ------------------- Numerical Summary -----------------------
        st.markdown("---")
        st.markdown("### 📌 Portfolio Metrics Summary")
        st.write(f"**Mean Return X:** {mean_x:.2f}")
        st.write(f"**Mean Return Y:** {mean_y:.2f}")
        st.write(f"**Std Dev X:** {sd_x:.4f}")
        st.write(f"**Std Dev Y:** {sd_y:.4f}")
        st.write(f"**Correlation (X,Y):** {corr_xy:.4f}")
        st.write(f"**Your Portfolio Expected Return:** {user_return:.2f}")
        st.write(f"**Your Portfolio Risk (Std Dev):** {user_risk:.4f}")

else:
    st.info("Set values and press **Calculate Efficient Frontier** from the sidebar.")

