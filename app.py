# ===============================================================
#     PERFECT TABLE INPUT (X & Y) + INLINE SLIDER AS ROW 6
# ===============================================================

st.sidebar.title("🔧 Portfolio Inputs")
st.sidebar.markdown("### 📈 Return Inputs")

# 🔧 CSS FOR ALIGNMENT (same height, compact, right justification)
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

# ---- Default Dataset ----
default_X = [6.6, 5.6, -9.0, 12.6, 14.0]
default_Y = [24.5, -5.9, 19.9, -7.8, 14.8]

X, Y = [], []

# ---- Rows 1–5: Input rows ----
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

# ---- Row 6: Inline Weight Slider ----
st.sidebar.markdown(
    f"<div class='return-table-row'><div class='return-obs'>6</div>"
    f"<div style='flex:1; padding-left:5px;'>Weight of X,Y:</div></div>",
    unsafe_allow_html=True
)
w_x_slider = st.sidebar.slider("", 0, 100, 50, 1)  # no label, inline
w_user = w_x_slider / 100  # decimal for calculation

# ---- Convert Inputs to numpy arrays ----
X = np.array(X)
Y = np.array(Y)
