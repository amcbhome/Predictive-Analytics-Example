import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Portfolio Diversification Visualiser", layout="wide")

# ---------- PAGE STYLING ----------
st.markdown("""
<style>
[data-testid="stNumberInput"] > div {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}
.st-emotion-cache-16idsys p {
    margin-bottom: -10px !important;
}
th, td {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# ================================
#        TITLE (3 COLUMNS)
# ================================
colA, colB, colC = st.columns([1, 4, 1])

with colA:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2331/2331944.png",
        width=80
    )

with colB:
    st.markdown(
        "<h1 style='text-align: center;'>Portfolio Diversification Visualiser</h1>",
        unsafe_allow_html=True
    )

with colC:
    st.write("")  # Empty block for spacing symmetry

# ================================
#        INPUT SECTION (2 COLUMNS)
# ================================
st.markdown("<h3 style='text-align: center;'>Input Asset Data (5 values)</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Asset X Values**")
    x1 = st.number_input("X1", value=5.0, step=0.1, format="%.2f")
    x2 = st.number_input("X2", value=7.0, step=0.1, format="%.2f")
    x3 = st.number_input("X3", value=8.0, step=0.1, format="%.2f")
    x4 = st.number_input("X4", value=9.0, step=0.1, format="%.2f")
    x5 = st.number_input("X5", value=12.0, step=0.1, format="%.2f")

with col2:
    st.markdown("**Asset Y Values**")
    y1 = st.number_input("Y1", value=6.0, step=0.1, format="%.2f")
    y2 = st.number_input("Y2", value=8.0, step=0.1, format="%.2f")
    y3 = st.number_input("Y3", value=9.0, step=0.1, format="%.2f")
    y4 = st.number_input("Y4", value=11.0, step=0.1, format="%.2f")
    y5 = st.number_input("Y5", value=15.0, step=0.1, format="%.2f")

# Convert to numpy arrays
x_values = np.array([x1, x2, x3, x4, x5])
y_values = np.array([y1, y2, y3, y4, y5])

# ================================
#     CALCULATE AND GRAPH
# ================================
if st.button("Calculate Portfolio Curve"):

    st.subheader("📈 Risk & Return Relationship Curve")

    # Smooth weights from 0 to 1
    weights = np.linspace(0, 1, 100)
    portfolio = weights * x_values.mean() + (1 - weights) * y_values.mean()

    # ---- Matplotlib graph ----
    fig, ax = plt.subplots(figsize=(8, 4.5))

    ax.plot(weights, portfolio, linewidth=2)
    ax.scatter([1], [x_values.mean()], color='blue')
    ax.scatter([0], [y_values.mean()], color='red')

    ax.text(1, x_values.mean(), "X", fontsize=10, ha='center', va='bottom')
    ax.text(0, y_values.mean(), "Y", fontsize=10, ha='center', va='bottom')

    ax.set_xlabel("Weight of X")
    ax.set_ylabel("Return")
    ax.set_ylim(5, None)  # Start Y axis at 5
    ax.set_xlim(0, 1)

    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

else:
    st.info("Press **Calculate Portfolio Curve** to display the graph.")

