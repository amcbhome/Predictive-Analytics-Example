import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------
# ---- BASIC APP CONFIG & STYLE ----
# ------------------------------------------------
st.set_page_config(page_title="Diversification Dashboard", layout="wide")
st.markdown("""
<style>
h1 { font-size: 40px; font-weight: 700; }
.table-style td, .table-style th { text-align:center !important; padding:5px !important; }
.stButton>button { font-weight:700 !important; font-size:20px !important; border-radius:10px !important; padding:8px 25px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# ---- DEFAULT DATA (Watson & Head style) ----
# ------------------------------------------------
df = pd.DataFrame({
    "X": [6.6, 5.6, -9, 12.6, 14],
    "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
})

# ------------------------------------------------
# ---- SIDEBAR INPUT ----
# ------------------------------------------------
c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    st.markdown("### 📥 Input")
    st.write("Enter or edit your returns:")
    for i in range(len(df)):
        cols = st.columns(2)
        df.at[i, "X"] = cols[0].number_input("", value=float(df.at[i, "X"]), step=0.1, key=f"x{i}")
        df.at[i, "Y"] = cols[1].number_input("", value=float(df.at[i, "Y"]), step=0.1, key=f"y{i}")

    weight = st.slider("Weight in Asset X (wₓ)", 0.0, 1.0, 0.5, 0.01)

with c2:
    st.markdown("### 📊 Output")

# ------------------------------------------------
# ---- CALCULATIONS ----
# ------------------------------------------------
mean_X = df["X"].mean()
mean_Y = df["Y"].mean()
std_X = df["X"].std()
std_Y = df["Y"].std()
c_xy = df["X"].corr(df["Y"])

# Portfolio statistics
port_ret = weight * mean_X + (1 - weight) * mean_Y
port_risk = np.sqrt((weight**2 * std_X**2) +
                    ((1 - weight)**2 * std_Y**2) +
                    (2 * weight * (1 - weight) * std_X * std_Y * c_xy))

# Output Table
output = pd.DataFrame({
    "Metric": ["Correlation", "Mean X", "Mean Y", "Std Dev X", "Std Dev Y", "Portfolio Return", "Portfolio Risk"],
    "Value (%)": [f"{c_xy*100:.2f}%", f"{mean_X:.2f}%", f"{mean_Y:.2f}%", f"{std_X:.2f}%",
                  f"{std_Y:.2f}%", f"{port_ret:.2f}%", f"{port_risk:.2f}%"]
})
with c2:
    st.table(output)

# ------------------------------------------------
# ---- EFFICIENT FRONTIER (PLOTLY) ----
# ------------------------------------------------
# Generate points
w = np.linspace(0, 1, 200)
front_ret = w * mean_X + (1 - w) * mean_Y
front_risk = np.sqrt((w**2 * std_X**2) + ((1 - w)**2 * std_Y**2) +
                      (2 * w * (1 - w) * std_X * std_Y * c_xy))

# Create Plotly chart
fig = go.Figure()

# Efficient Frontier
fig.add_trace(go.Scatter(
    x=front_risk, y=front_ret,
    mode='lines', name='Efficient Frontier',
    line=dict(color='blue', width=3)
))

# Current Portfolio (Animated Movement)
fig.add_trace(go.Scatter(
    x=[port_risk], y=[port_ret],
    mode='markers', name="📌 Current Portfolio",
    marker=dict(color='red', size=12)
))

# Asset X point
fig.add_trace(go.Scatter(
    x=[std_X], y=[mean_X], mode="markers+text",
    text=["🟢 Asset X"], textposition="top center",
    name="Asset X", marker=dict(color='green', size=12)
))

# Asset Y point
fig.add_trace(go.Scatter(
    x=[std_Y], y=[mean_Y], mode="markers+text",
    text=["🟠 Asset Y"], textposition="top center",
    name="Asset Y", marker=dict(color='orange', size=12)
))

# Minimum Risk Portfolio
min_index = np.argmin(front_risk)
fig.add_trace(go.Scatter(
    x=[front_risk[min_index]], y=[front_ret[min_index]],
    mode="markers+text", text=["🔵 Min Risk"], textposition="bottom right",
    name="Min Risk", marker=dict(color='blue', size=13, symbol='diamond')
))

# Add dashed guide lines
for x, y in [(port_risk, port_ret), (std_X, mean_X), (std_Y, mean_Y)]:
    fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=y,
                  line=dict(color="gray", width=1, dash="dash"))
    fig.add_shape(type="line", x0=0, y0=y, x1=x, y1=y,
                  line=dict(color="gray", width=1, dash="dash"))

# Layout
fig.update_layout(
    title="📈 Efficient Frontier (Hover + Animation)",
    xaxis_title="Risk (Std Dev %)",
    yaxis_title="Expected Return (%)",
    hovermode="closest",
    template="plotly_white",
    width=800, height=500
)

with c3:
    st.plotly_chart(fig, use_container_width=True)
