import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Efficient Frontier Portfolio App", layout="wide")

# ===============================================================
#                  DEFAULT TEXTBOOK DATA (X & Y)
# ===============================================================
default_X = [6.6, 5.6, -9.0, 12.6, 14.0]
default_Y = [24.5, -5.9, 19.9, -7.8, 14.8]

# ===============================================================
#                     SIDEBAR INPUTS (TABLE STYLE)
# ===============================================================
st.sidebar.title("🔧 Portfolio Inputs")

# Table-like layout: Obs | X | Y
st.sidebar.markdown("### 📈 Return Inputs")

obs_col, x_col, y_col = st.sidebar.columns([1, 2, 2])
with obs_col:
    st.markdown("**Obs**")
    st.write("1")
    st.write("2")
    st.write("3")
    st.write("4")
    st.write("5")

# 5 input rows for X & Y
with x_col:
    st.markdown("**X (%)**")
    x1 = st.number_input("", value=default_X[0], step=0.1, format="%.2f", key="x1")
    x2 = st.number_input("", value=default_X[1], step=0.1, format="%.2f", key="x2")
    x3 = st.number_input("", value=default_X[2], step=0.1, format="%.2f", key="x3")
    x4 = st.number_input("", value=default_X[3], step=0.1, format="%.2f", key="x4")
    x5 = st.number_input("", value=default_X[4], step=0.1, format="%.2f", key="x5")

with y_col:
    st.markdown("**Y (%)**")
    y1 = st.number_input("", value=default_Y[0], step=0.1, format="%.2f", key="y1")
    y2 = st.number_input("", value=default_Y[1], step=0.1, format="%.2f", key="y2")
    y3 = st.number_input("", value=default_Y[2], step=0.1, format="%.2f", key="y3")
    y4 = st.number_input("", value=default_Y[3], step=0.1, format="%.2f", key="y4")
    y5 = st.number_input("", value=default_Y[4], step=0.1, format="%.2f", key="y5")

# ------- Slider Under Inputs -------
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚖️ Weight of X,Y")
w_x_slider = st.sidebar.slider("X %:", 0, 100, 50, 1)
w_user = w_x_slider / 100

# Convert to arrays
X = np.array([x1, x2, x3, x4, x5])
Y = np.array([y1, y2, y3, y4, y5])

# ===============================================================
#                         FRONTIER MATHS
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
    mean_X, mean_Y = X.mean(), Y.mean()
    sd_X, sd_Y = X.std(ddof=1), Y.std(ddof=1)
    corr_XY = np.corrcoef(X, Y)[0][1]

    # Efficient Frontier Range
    W = np.linspace(0, 1, 100)
    ef_returns = portfolio_return(W, mean_X, mean_Y)
    ef_risk = portfolio_risk(W, sd_X, sd_Y, corr_XY)

    # User portfolio point
    user_return = portfolio_return(w_user, mean_X, mean_Y)
    user_risk = portfolio_risk(w_user, sd_X, sd_Y, corr_XY)

    # Layout: Metrics left, chart right
    colM, colG = st.columns([1, 2])

    # -------- LEFT: Metrics Panel --------
    with colM:
        st.markdown("### 📌 Metrics Summary")
        st.markdown(f"""
        <pre style='font-size:15px'>
    Mean Return X:         {mean_X:.2f}%
    Mean Return Y:         {mean_Y:.2f}%
    Std Dev X:             {sd_X:.4f}
    Std Dev Y:             {sd_Y:.4f}
    Correlation (X,Y):     {corr_XY:.4f}

    Your Expected Return:  {user_return:.2f}%
    Your Risk (Std Dev):   {user_risk:.4f}
        </pre>
        """, unsafe_allow_html=True)

    # -------- RIGHT: Graph --------
    with colG:
        st.markdown("## 📈 Efficient Frontier (X & Y Assets)")
        fig, ax = plt.subplots(figsize=(8, 4))

        ax.plot(ef_risk, ef_returns, linewidth=2)

        ax.scatter(sd_X, mean_X, color='blue', s=80)
        ax.text(sd_X, mean_X, " X", fontsize=9, color='blue')

        ax.scatter(sd_Y, mean_Y, color='red', s=80)
        ax.text(sd_Y, mean_Y, " Y", fontsize=9, color='red')

        ax.scatter(user_risk, user_return, color='green', s=100)
        ax.text(user_risk, user_return, "  Your Mix", fontsize=9, color='green')

        ax.set_xlabel("Risk (Std. Deviation)")
        ax.set_ylabel("Return (%)")
        ax.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig)

else:
    st.info("Select weights and press **Calculate Efficient Frontier** from the sidebar.")
