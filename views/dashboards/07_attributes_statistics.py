import streamlit as st
from helpers.utils import sum_tsv_data
from collections import Counter
import pandas as pd


@st.experimental_memo()
def get_data(key: str):
    df = sum_tsv_data(f"statistics_{key}", index_col="Value", dtype={"Count": "int"})

    df["Count"] = df["Count"].astype("int")
    df["%"] = (100.0*df["Count"] / df["Count"].sum()).round(3)
    df.sort_values(by="Count", ascending=False, inplace=True)

    return df.head(500)


col1, col2 = st.columns([2,3])

with col1:
    st.subheader("Tweet Language")
    st.table(get_data("lang"))

with col2:
    st.subheader("Tweet Source")
    st.table(get_data("source"))