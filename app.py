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
#        HEADER (3 COLUMNS)
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
    st.write("")

# ================================
#         INPUT TRAY (EXPANDER)
# ================================
with st.expander("🔢 Input Asset Data (Click to Expand)"):
    
    col1, col2 = st.columns(2)

    # ---- 5 input rows for asset X ----
    with col1:
        st.markdown("**Asset X Values**")
        x1 = st.number_input("X1", value=5.0, step=0.1, format="%.2f")
        x2 = st.number_input("X2", value=7.0, step=0.1, format="%.2f")
        x3 = st.number_input("X3", value=8.0, step=0.1, format="%.2f")
        x4 = st.number_input("X4", value=9.0, step=0.1, format="%.2f")
        x5 = st.number_input("X5", value=12.0, step=0.1, format="%.2f")

    # ---- 5 input rows for asset Y ----
    with col2:
        st.markdown("**Asset Y Values**")
        y1 = st.number_input("Y1", value=6.0, step=0.1, format="%.2f")
        y2 = st.number_input("Y2", value=8.0, step=0.1, format="%.2f")
        y3 = st.number_input("Y3", value=9.0, step=0.1, format="%.2f")
        y4 = st.number_input("Y4", value=11.0, step=0.1, format="%.2f")
        y5 = st.number_input("Y5", value=15.0, step=0.1, format="%.2f")

    # ---- Weight inputs that must sum to 100 ----
    st.markdown("---")
    st.markdown("### ⚖️ Portfolio Weights (Must sum to 100%)")

    weight_col1, weight_col2 = st.columns(2)
    with weight_col1:
        weight_x = st.number_input("Weight of X (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)

    with weight_col2:
        weight_y = st.number_input("Weight of Y (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)

# ---------- Convert to numpy arrays ----------
x_values = np.array([x1, x2, x3, x4, x5])
y_values = np.array([y1, y2, y3, y4, y5])

# ================================
#     CALCULATE AND GRAPH
# ================================
if st.button("Calculate Portfolio Curve"):

    if weight_x + weight_y != 100:
        st.error("❌ The weights must sum to **100%**. Please adjust X% and Y%.")
    else:
        st.subheader("📈 Risk & Return Relationship Curve")

        # Convert weights to decimals
        wx = weight_x / 100
        wy = weight_y / 100

        # Weighted return
        weighted_return = wx * x_values.mean() + wy * y_values.mean()

        # x-axis is weights of X from 0 to 1
        weights = np.linspace(0, 1, 100)
        portfolio = weights * x_values.mean() + (1 - weights) * y_values.mean()

        # ---- Matplotlib plot ----
        fig, ax = plt.subplots(figsize=(8, 4.5))

        ax.plot(weights, portfolio, linewidth=2)
        ax.scatter([1], [x_values.mean()], color='blue')
        ax.scatter([0], [y_values.mean()], color='red')
        ax.scatter([wx], [weighted_return], color='green', s=80)

        ax.text(1, x_values.mean(), "X", fontsize=10, ha='center', va='bottom')
        ax.text(0, y_values.mean(), "Y", fontsize=10, ha='center', va='bottom')
        ax.text(wx, weighted_return, "Your Mix", fontsize=10, ha='left', va='bottom', color='green')

        ax.set_xlabel("Weight of X")
        ax.set_ylabel("Return")
        ax.set_ylim(5, None)
        ax.set_xlim(0, 1)

        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

else:
    st.info("Press **Calculate Portfolio Curve** to display the graph.")
