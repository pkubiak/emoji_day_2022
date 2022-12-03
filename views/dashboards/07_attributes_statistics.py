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


def build_tab(label, data):
    st.subheader(label)

    head = data.head(10)['%']
    head.loc['other'] = 100.0 - head.sum()
    head = head.reset_index()

    chart = alt.Chart(head).mark_bar().encode(
        x=alt.X('Value', type='nominal', sort=None),
        y="%:Q",
        color=alt.condition(
            alt.datum.Value == 'other',
            alt.value('orange'),
            alt.value('steelblue') 
        )
    ).properties(
        title="Top 10 values",
        height=300,
    )

    st.altair_chart(chart, use_container_width=True)

    with st.expander("See details"):
        st.table(data)

st.title(__label__)

tab1, tab2 = st.tabs(["Language", "Source"])
import altair as alt

with tab1:
    df = get_data("lang")

    build_tab("Tweet Language", df)
    
with tab2:
    data = get_data("source")
    build_tab("Tweet Source", data)