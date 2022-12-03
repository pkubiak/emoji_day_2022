from helpers.utils import get_tsv_data, render_as_table
import streamlit as st
from functools import reduce
import pandas as pd
from collections import Counter


@st.experimental_memo()
def get_data():
    data = get_tsv_data("emoji_frequency", with_dates=True, index_col="Emoji", dtype={"Count": "int"})

    records = {}
    for date, df in data:
        df["%"] = 100*df["Count"] / df["Count"].sum()
        # records[date] = list(f"{idx} ({row['%']:.2f}%)" for idx, row in df.head(5).iterrows())
        top = df.head(10)
        records[date] = list(f"{idx}" for idx, row in top.iterrows())

    df = pd.DataFrame.from_dict(records, orient="index")#, columns=["1st", "2nd", "3rd", "4th", "5th"])
    df.sort_index(inplace=True)
    return df

st.title(f"WIP: {__label__}")
df = get_data()

st.table(df)

count = Counter()
for _, row in df.iterrows():
    count.update(row)

st.subheader("Mostly in the top 10")
# st.write(len(df))
# st.write(count.most_common())

h = render_as_table([(k, f"{v}/{len(df)}") for k, v in count.most_common(12)])
st.markdown(h, unsafe_allow_html=True)