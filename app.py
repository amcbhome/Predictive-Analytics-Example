import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Risk Demo", layout="wide")

# ---------- APP STYLING ----------
st.markdown("""
<style>
/* tighten row spacing */
[data-testid="stNumberInput"] > div {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}
/* tighten input label spacing */
.st-emotion-cache-16idsys p {
    margin-bottom: -10px !important;
}
/* table text align center */
th, td {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("📊 Portfolio Diversification Visualiser")

# ---------- INPUT DATA ----------
st.subheader("Input Asset Data (5 values)")

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

x_values = np.array([x1, x2, x3, x4, x5])
y_values = np.array([y1, y2, y3, y4, y5])

# ---------- PLOT CURVE ----------
st.subheader("📈 Risk & Return Relationship Curve")

# Create a smooth curve from the values
weights = np.linspace(0, 1, 100)
portfolio = weights * x_values.mean() + (1 - weights) * y_values.mean()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=weights,
    y=portfolio,
    mode="lines",
    name="Portfolio Curve"
))

# Highlight X and Y
fig.add_trace(go.Scatter(x=[1], y=[x_values.mean()], mode="markers+text",
                         text=["X"], textposition="top center", marker=dict(size=10)))

fig.add_trace(go.Scatter(x=[0], y=[y_values.mean()], mode="markers+text",
                         text=["Y"], textposition="top center", marker=dict(size=10)))

# Force axes to start at 5
fig.update_yaxes(range=[5, None])
fig.update_xaxes(range=[0, 1])

fig.update_layout(
    xaxis_title="Weight of X",
    yaxis_title="Return",
    height=450,
    template="simple_white"
)

st.plotly_chart(fig, use_container_width=True)
