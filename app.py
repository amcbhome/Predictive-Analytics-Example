# ===============================================================
#          Portfolio Efficient Frontier (X & Y Assets)
# ===============================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Efficient Frontier Portfolio App", layout="wide")

# ===============================================================
#          SIDEBAR DATAFRAME INPUT  (NO CSS NEEDED)
# ===============================================================

st.sidebar.title("Portfolio Inputs")
st.sidebar.markdown("### Return Inputs")

# Default textbook dataset (as editable table)
df_default = pd.DataFrame({
    "X (%)": [6.6, 5.6, -9.0, 12.6, 14.0],
    "Y (%)": [24.5, -5.9, 19.9, -7.8, 14.8]
})
df_default.index = df_default.index + 1  # Obs 1–5

# Editable dataframe in sidebar
df = st.sidebar.data_editor(
    df_default,
    use_container_width=True,
    key="returns_table"
)

# Extract updated values
X = df["X (%)"].to_numpy()
Y = df["Y (%)"].to_numpy()

# Weight slider
w_x_slider = st.sidebar.slider("Weight of X (%)", 0, 100, 50, 1)
w_user = w_x_slider / 100  # convert to decimal

# ===============================================================
#          PORTFOLIO FUNCTIONS
# ===============================================================

def portfolio_return(w, r1, r2):
    return w * r1 + (1 - w) * r2

def portfolio_risk(w, sd1, sd2, corr):
    cov = corr * sd1 * sd2
    return np.sqrt(w**2 * sd1**2 + (1 - w)**2 * sd2**2 + 2 * w * (1 - w) * cov)

# ===============================================================
#                CALCULATE AND DISPLAY OUTPUT
# ===============================================================

if st.sidebar.button("Calculate Efficient Frontier"):

    # Calculate stats
    mean_X, mean_Y = X.mean(), Y.mean()
    sd_X, sd_Y = X.std(ddof=1), Y.std(ddof=1)
    corr_XY = np.corrcoef(X, Y)[0][1]

    # Frontier curve
    W = np.linspace(0, 1, 100)
    ef_returns = portfolio_return(W, mean_X, mean_Y)
    ef_risk = portfolio_risk(W, sd_X, sd_Y, corr_XY)

    # User portfolio
    user_return = portfolio_return(w_user, mean_X, mean_Y)
    user_risk = portfolio_risk(w_user, sd_X, sd_Y, corr_XY)

    # Layout columns
    colM, colG = st.columns([1, 2])

    # ------- METRICS PANEL --------
    with colM:
        st.markdown("### Metrics Summary")
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

    # ------- GRAPH --------
    with colG:
        st.markdown("## Efficient Frontier (X & Y Assets)")

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

    # ------- PDF EXPORT ------
    def create_pdf():
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 800, "Portfolio Efficient Frontier Report")

        p.setFont("Helvetica", 12)
        p.drawString(50, 770, "Report fields and chart will be expanded later.")
        p.drawString(50, 750, f"Expected Return: {user_return:.2f}%")
        p.drawString(50, 730, f"Portfolio Risk (Std Dev): {user_risk:.4f}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    st.download_button(
        label="📄 Download PDF Report",
        data=create_pdf(),
        file_name="efficient_frontier_report.pdf",
        mime="application/pdf"
    )

# ------- if not yet pressed -------
else:
    st.info("Select weights and press **Calculate Efficient Frontier** from the sidebar.")
