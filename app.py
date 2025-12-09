# ===============================================================
#           SIDEBAR TABLE WITHOUT +/- BUTTONS (TIGHT & CLEAN)
# ===============================================================

st.sidebar.title("🔧 Portfolio Inputs")
st.sidebar.markdown("### 📈 Return Inputs")

# ---- CSS FOR PERFECT SPACING & NO ARROWS ----
st.sidebar.markdown("""
<style>

.return-table-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    height: 28px !important;
    margin-bottom: 3px !important;
}

.return-table-header {
    display: flex;
    flex-direction: row;
    font-weight: bold;
    justify-content: space-between;
    padding-bottom: 4px;
}

.return-obs {
    width: 32px;
    text-align: center;
}

.return-input {
    width: 80px;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
    text-align: right !important;
    padding-right: 6px !important;
    height: 26px !important;
    font-size: 13px !important;
}

</style>
""", unsafe_allow_html=True)

# ---- Header Row ----
st.sidebar.markdown(
    "<div class='return-table-header'><div class='return-obs'>Obs</div>"
    "<div class='return-input'>X (%)</div><div class='return-input'>Y (%)</div></div>",
    unsafe_allow_html=True
)

default_X = [6.6, 5.6, -9.0, 12.6, 14.0]
default_Y = [24.5, -5.9, 19.9, -7.8, 14.8]

X, Y = [], []

for i in range(5):
    st.sidebar.markdown(
        f"<div class='return-table-row'><div class='return-obs'>{i+1}</div>",
        unsafe_allow_html=True
    )
    colX, colY = st.sidebar.columns([1,1])
    with colX:
        X.append(st.sidebar.number_input(f"x{i}", value=default_X[i], step=None, format="%.2f", label_visibility="collapsed"))
    with colY:
        Y.append(st.sidebar.number_input(f"y{i}", value=default_Y[i], step=None, format="%.2f", label_visibility="collapsed"))
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ---- Weight Slider Row (Row 6) ----
st.sidebar.markdown(
    f"<div class='return-table-row'><div class='return-obs'>6</div>"
    f"<div style='flex:1; padding-left:5px;'>Weight of X,Y:</div></div>",
    unsafe_allow_html=True
)

w_x_slider = st.sidebar.slider("", 0, 100, 50, 1)
w_user = w_x_slider / 100

X = np.array(X)
Y = np.array(Y)
