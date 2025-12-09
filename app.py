import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Efficient Frontier Portfolio App", layout="wide")

# ===============================================================
#                       DEFAULT TEXTBOOK DATA (X & Y)
# ===============================================================
default_X = [6.6, 5.6, -9.0, 12.6, 14.0]
default_Y = [24.5, -5.9, 19.9, -7.8, 14.8]

# ===============================================================
#                           SIDEBAR INPUTS
# ===============================================================
st.sidebar.title("🔧 Portfolio Inputs")
st.sidebar.markdown("### 📚 X & Y Data (Default from Textbook)")
st.sidebar.info("Returns automatically loaded from the dataset shown previously.")

col1, col2 = st.sidebar.columns(2)

# ---- 5 input rows for X ----
with col1:
    st.markdown("**X Returns (%)**")
    x1 = st.number_input("X1", value=default_X[0], step=0.1, format="%.2f")
    x2 = st.number_input("X2", value=default_X[1], step=0.1, format="%.2f")
    x3 = st.number_input("X3", value=default_X[2], step=0.1, format="%.2f")
    x4 = st.number_input("X4", value=default_X[3], step=0.1, format="%.2f")
    x5 = st.number_input("X5", value=default_X[4], step=0.1, format="%.2f")

# ---- 5 input rows for Y ----
with col2:
    st.markdown("**Y Returns (%)**")
    y1 = st.number_input("Y1", value=default_Y[0], step=0.1, format="%.2f")
    y2 = st.number_input("Y2", value=default_Y[1], step=0.1, format="%.2f")
    y3 = st.number_input("Y3", value=default_Y[2], step=0.1, format="%.2f")
    y4 = st.number_input("Y4", value=default_Y[3], step=0.1, format="%.2f")
    y5 = st.number_input("Y5", value=default_Y[4], step=0.1, format="%.2f")

# ------- Weight Slider Under Inputs -------
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚖️ Weight of Asset X")
w_x_slider = st.sidebar.slider("X %:", 0, 100, 50, 1)
w_y_auto = 100 - w_x_slider
st.sidebar.write(f"📌 Weight of Y: **{w_y_auto}%**")

# Convert data to arrays
X = np.array([x1, x2, x3, x4, x5])
Y = np.array([y1, y2, y3, y4, y5])

# ===============================================================
#                        EFFICIENT FRONTIER MATHS
# ===============================================================
def portfolio_return(w, r1, r2):
    return w * r1 + (1 - w) * r2

def portfolio_risk(w, sd1, sd2, corr):
    cov = corr * sd1 * sd2
    return np.sqrt(w**2 * sd1**2 + (1 - w)**2 * sd2**2 + 2 * w * (1 - w) * cov)

# ===============================================================
#                        CALCULATE + PLOT
# ===============================================================
if st.sidebar.button("Calculate Efficient Frontier"):

    # Descriptive statistics
    mean_X = X.mean()
    mean_Y = Y.mean()
    sd_X = X.std(ddof=1)
    sd_Y = Y.std(ddof=1)
    corr_XY = np.corrcoef(X, Y)[0][1]

    # Slider choice (user portfolio)
    w_user = w_x_slider / 100

    # Efficient Frontier Range
    W = np.linspace(0, 1, 100)
    ef_returns = portfolio_return(W, mean_X, mean_Y)
    ef_risk = portfolio_risk(W, sd_X, sd_Y, corr_XY)

    # User portfolio risk & return
    user_return = portfolio_return(w_user, mean_X, mean_Y)
    user_risk = portfolio_risk(w_user, sd_X, sd_Y, corr_XY)

    # ===================== GRAPH ===========================
    st.markdown("## 📈 Efficient Frontier (X & Y Assets)")
    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(ef_risk, ef_returns, linewidth=2, label="Efficient Frontier")

    # Asset points
    ax.scatter(sd_X, mean_X, color='blue', s=80)
    ax.text(sd_X, mean_X, " X", fontsize=9, color='blue')

    ax.scatter(sd_Y, mean_Y, color='red', s=80)
    ax.text(sd_Y, mean_Y, " Y", fontsize=9, color='red')

    # User chosen mix
    ax.scatter(user_risk, user_return, color='green', s=100)
    ax.text(user_risk, user_return, "  Your Mix", fontsize=9, color='green')

    ax.set_xlabel("Risk (Std. Deviation)")
    ax.set_ylabel("Return (%)")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)

    # ===================== METRICS PANEL =====================
    st.markdown("### 📌 Portfolio Metrics Summary")
    st.write(f"**Mean Return X:** {mean_X:.2f}%")
    st.write(f"**Mean Return Y:** {mean_Y:.2f}%")
    st.write(f"**Std Dev X:** {sd_X:.4f}")
    st.write(f"**Std Dev Y:** {sd_Y:.4f}")
    st.write(f"**Correlation (X,Y):** {corr_XY:.4f}")
    st.write(f"**Your Portfolio Expected Return:** {user_return:.2f}%")
    st.write(f"**Your Portfolio Risk (Std Dev):** {user_risk:.4f}")

else:
    st.info("Select weights and press **Calculate Efficient Frontier** from the sidebar.")
