import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="DEMATEL Explorer", layout="wide")
st.title("DEMATEL Method Explorer")

st.markdown("""
Upload a square pairwise‐influence matrix (CSV) where rows and columns
are the same set of factors, and each cell [i,j] is the degree to which
factor i influences factor j.
""")

# Upload
uploaded = st.file_uploader("Upload your influence matrix CSV", type=["csv"])
if uploaded is None:
    st.info("Please upload a CSV file to proceed.")
    st.stop()

# Read matrix
df = pd.read_csv(uploaded, index_col=0)
if df.shape[0] != df.shape[1]:
    st.error("Matrix must be square (same number of rows and columns).")
    st.stop()

factors = list(df.index)
D = df.values.astype(float)

st.subheader("Direct Relation Matrix (D)")
st.dataframe(df.style.format("{:.3f}"))

# Normalize direct relation matrix
row_sum = D.sum(axis=1)
col_sum = D.sum(axis=0)
norm_factor = max(row_sum.max(), col_sum.max())
D_norm = D / norm_factor

st.subheader("Normalized Direct Relation Matrix (D_norm)")
st.dataframe(pd.DataFrame(D_norm, index=factors, columns=factors).style.format("{:.3f}"))

# Total relation matrix: T = D_norm * (I - D_norm)^(-1)
I = np.eye(len(D))
T = D_norm.dot(np.linalg.inv(I - D_norm))

st.subheader("Total Relation Matrix (T)")
st.dataframe(pd.DataFrame(T, index=factors, columns=factors).style.format("{:.3f}"))

# Compute row (r), column (c), prominence (r+c), net effect (r-c)
r = T.sum(axis=1)
c = T.sum(axis=0)
prominence = r + c
net_effect = r - c

results = pd.DataFrame({
    "r (influence given)": r,
    "c (influence received)": c,
    "Prominence (r+c)": prominence,
    "Net effect (r-c)": net_effect
}, index=factors)

st.subheader("DEMATEL Results")
st.dataframe(results.style.format("{:.3f}"))

# Identify cause vs effect groups
cause = results[results["Net effect (r-c)"] > 0]
effect = results[results["Net effect (r-c)"] < 0]

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Cause Group** (Net > 0)")
    st.write(cause.style.format("{:.3f}"))
with col2:
    st.markdown("**Effect Group** (Net < 0)")
    st.write(effect.style.format("{:.3f}"))

# Visualizations
st.subheader("Prominence & Net Effect Bar Chart")
chart_data = results.reset_index().melt(id_vars="index", 
                                        value_vars=["Prominence (r+c)", "Net effect (r-c)"],
                                        var_name="Measure", value_name="Value")
chart_data.rename(columns={"index":"Factor"}, inplace=True)

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X("Value:Q"),
    y=alt.Y("Factor:N", sort='-x'),
    color="Measure:N",
    column=alt.Column("Measure:N", header=alt.Header(title=None))
).properties(width=200, height=300)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.caption("DEMATEL implementation courtesy of standard methodology.")
