import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------
# PAGE SETUP
# ---------------------------------
st.set_page_config(page_title="Diversification of Risk Dashboard", layout="wide")

# ---------------------------------
# DEFAULT DATA
# ---------------------------------
default_data = pd.DataFrame({
    "X": [6.6, 5.6, -9.0, 12.6, 14.0],
    "Y": [24.5, -5.9, 19.9, -7.8, 14.8]
})

# ---------------------------------
# STYLE CSS
# ---------------------------------
st.markdown("""
<style>
/* Headings */
h1 {
    font-size: 36px !important;
    font-weight: 700 !important;
}
.section-title {
    background-color: #eaf3ff;
    padding: 8px 18px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: 600;
    display: inline-block;
    border: 1px solid #c9d7e8;
}

/* Table Styling */
.custom-table {
    border-collapse: collapse;
    width: 100%;
    font-size: 18px;
    text-align: center;
}
.custom-table th {
    background-color: #f6f8fc;
    padding: 8px;
    border: 1px solid #d0d7de;
    font-weight: 600;
}
.custom-table td {
    padding: 6px 8px;
    border: 1px solid #d0d7de;
}

/* Calculate Button */
.calc-btn button {
    background-color: #d62828 !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    font-size: 18px !important;
    padding: 10px 28px !important;
}

/* Weight Slider Label */
.weight-label {
    font-size: 17px !important;
    margin-top: 5px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# LAYOUT
# ---------------------------------
col1, col2, col3 = st.columns([1, 1, 2])

# ----------------------
# INPUT COLUMN
# ----------------------
with col1:
    st.markdown("<div class='section-title'>📥 Input</div>", unsafe_allow_html=True)
    st.write("Enter or edit your returns:")

    # Editable numeric inputs
    edited_data = {}
    for i in range(len(default_data)):
        col_x, col_y = st.columns(2)
        x_val = col_x.number_input(f" ", value=float(default_data.loc[i,"X"]), key=f"x{i}", format="%.2f")
        y_val = col_y.number_input(f"  ", value=float(default_data.loc[i,"Y"]), key=f"y{i}", format="%.2f")
        edited_data[i] = [x_val, y_val]

    df = pd.DataFrame.from_dict(edited_data, orient="index", columns=["X", "Y"])

    st.markdown("<div class='weight-label'>Weight in Asset X (wₓ)</div>", unsafe_allow_html=True)
    w = st.slider("", 0.0, 1.0, 0.50, 0.01)

    calc = st.container()
    with calc:
        st.markdown("<div class='calc-btn'>", unsafe_allow_html=True)
        pressed = st.button("Calculate")
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------
# CALCULATIONS + OUTPUT
# ----------------------
with col2:
    st.markdown("<div class='section-title'>📊 Output</div>", unsafe_allow_html=True)

    if pressed:
        df_dec = df / 100  
        mean_x = df_dec["X"].mean()
        mean_y = df_dec["Y"].mean()
        sd_x = df_dec["X"].std(ddof=0)
        sd_y = df_dec["Y"].std(ddof=0)
        corr = df_dec["X"].corr(df_dec["Y"])
        port_return = w * mean_x + (1 - w) * mean_y
        port_var = (w**2 * sd_x**2) + ((1 - w)**2 * sd_y**2) + (2*w*(1-w)*sd_x*sd_y*corr)
        port_sd = np.sqrt(port_var)

        output_table = pd.DataFrame({
            "Metric": ["Correlation", "Mean X", "Mean Y", "Std Dev X", "Std Dev Y", "Portfolio Return", "Portfolio Risk"],
            "Value (%)": [
                f"{corr*100:.2f}%", f"{mean_x*100:.2f}%", f"{mean_y*100:.2f}%",
                f"{sd_x*100:.2f}%", f"{sd_y*100:.2f}%", f"{port_return*100:.2f}%", f"{port_sd*100:.2f}%"
            ]
        })

        st.table(output_table.style.set_table_attributes('class="custom-table"'))
    else:
        st.write("Press **Calculate** to display results.")

# ----------------------
# GRAPH COLUMN
# ----------------------
with col3:
    st.markdown("<div class='section-title'>📈 Efficient Frontier</div>", unsafe_allow_html=True)

    if pressed:
        weights = np.arange(0, 1.01, 0.01)
        port_returns = w * mean_x + (1 - w) * mean_y
        returns = weights * mean_x + (1 - weights) * mean_y
        vars_ = (weights**2 * sd_x**2) + ((1 - weights)**2 * sd_y**2) + (2*weights*(1-weights)*sd_x*sd_y*corr)
        risks = np.sqrt(vars_)

        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(risks*100, returns*100, label="Efficient Frontier")
        ax.scatter(port_sd*100, port_return*100, color="red", label="Current Portfolio")
        ax.set_xlabel("Risk (Std Dev %)")
        ax.set_ylabel("Expected Return (%)")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.write("Awaiting calculation...")

