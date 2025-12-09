# ===============================================================
#          Portfolio Efficient Frontier (X & Y Assets)
# ===============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Efficient Frontier Portfolio App", layout="wide")

# ===============================================================
#              SIDEBAR: TABLE INPUT (PERFECTLY ALIGNED)
# ===============================================================

st.sidebar.title("🔧 Portfolio Inputs")
st.sidebar.markdown("### 📈 Return Inputs")

# ---- CSS for alignment ----
st.sidebar.markdown("""
<style>
.return-table-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    height: 32px !important;
    padding: 0px !important;
    margin-bottom: 2px !important;
}
.return-table-header {
    display: flex;
    flex-direction: row;
    font-weight: bold;
    justify-content: space-between;
    padding-bottom: 4px;
}
.return-obs {
    width: 30px;
    text-align: center;
    padding-top: 2px;
}
.return-input {
    width: 88px;
}
.stNumberInput > div > input {
    text-align: right !important;
    padding-right: 5px !important;
    height: 28px !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Table Header ----
st.sidebar.markdown(
    "<div class='return-table-header'><div class='return-obs'>Obs</div>"
    "<div class='return-input'>X (%)</div><div class='return-input'>Y (%)</div></div>",
    unsafe_allow_html=True
)

# ---- Default Dataset (Textbook) ----
default_X = [6.6, 5.6, -9.0, 12.6, 14.0]
default_Y = [24.5, -5.9, 19.9, -7.8, 14.8]

X, Y = [], []

# ---- Rows 1–5 ----
for i in range(5):
    st.sidebar.markdown(
        f"<div class='return-table-row'><div class='return-obs'>{i+1}</div>",
        unsafe_allow_html=True
    )
    colX, colY = st.sidebar.columns([1,1])
    with colX:
        X.append(st.number_input(f"x{i}", value=default_X[i], step=0.1,
                                 format='%.2f', label_visibility="collapsed"))
    with colY:
        Y.append(st.number_input(f"y{i}", value=default_Y[i], step=0.1,
                                 format='%.2f', label_visibility="collapsed"))
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ---- Row 6 (Weight Slider) ----
st.sidebar.markdown(
    f"<div class='return-table-row'><div class='return-obs'>6</div>"
    f"<div style='flex:1; padding-left:5px;'>Weight of X,Y:</div></div>",
    unsafe_allow_html=True
)
w_x_slider = st.sidebar.slider("", 0, 100, 50, 1)
w_user = w_x_slider / 100  # decimal for maths

# ---- Convert to numpy ----
X = np.array(X)
Y = np.array(Y)

# ===============================================================
#                    EFFICIENT FRONTIER FUNCTIONS
# ===============================================================

def portfolio_return(w, r1, r2):
    return w * r1 + (1 - w) * r2

def portfolio_risk(w, sd1, sd2, corr):
    cov = corr * sd1 * sd2
    return np.sqrt(w**2 * sd1**2 + (1 - w)**2 * sd2**2 + 2 * w * (1 - w) * cov)

# ===============================================================
#                      CALCULATION & DISPLAY
# ===============================================================

if st.sidebar.button("Calculate Efficient Frontier"):

    # ---- Stats ----
    mean_X, mean_Y = X.mean(), Y.mean()
    sd_X, sd_Y = X.std(ddof=1), Y.std(ddof=1)
    corr_XY = np.corrcoef(X, Y)[0][1]

    # ---- Frontier Series ----
    W = np.linspace(0, 1, 100)
    ef_returns = portfolio_return(W, mean_X, mean_Y)
    ef_risk = portfolio_risk(W, sd_X, sd_Y, corr_XY)

    # ---- User Mix ----
    user_return = portfolio_return(w_user, mean_X, mean_Y)
    user_risk = portfolio_risk(w_user, sd_X, sd_Y, corr_XY)

    # ---- Layout: Metrics Left, Chart Right ----
    colM, colG = st.columns([1, 2])

    # 🧮 METRICS PANEL
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

    # 📈 EFFICIENT FRONTIER CHART
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

    # ============================================================
    #                    PDF EXPORT BUTTON
    # ============================================================

    def create_pdf():
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 800, "Portfolio Efficient Frontier Report")

        p.setFont("Helvetica", 12)
        p.drawString(50, 770, "Report will contain metrics, chart and explanation...")
        p.drawString(50, 750, "Content to be added later.")

        p.drawString(50, 720, f"Expected Return: {user_return:.2f}%")
        p.drawString(50, 700, f"Portfolio Risk (Std Dev): {user_risk:.4f}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf()

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="efficient_frontier_report.pdf",
        mime="application/pdf"
    )

else:
    st.info("Select weights and press **Calculate Efficient Frontier** from the sidebar.")

# ============================================================
#      AUTO-FORMAT ALL NUMBER INPUTS (2 DECIMAL PLACES)
# ============================================================
st.markdown("""
<script>
function formatDecimalInputs(){
  const inputs = document.querySelectorAll('input[type="number"]');
  inputs.forEach(input => {
    input.addEventListener('blur', event => {
      let value = parseFloat(event.target.value);
      if (!isNaN(value)){
        event.target.value = value.toFixed(2);
      } else {
        event.target.value = "0.00";
      }
    });
  });
}
formatDecimalInputs();
</script>
""", unsafe_allow_html=True)
