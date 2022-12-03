from helpers.utils import get_tsv_data, render_as_table
import streamlit as st
from functools import reduce
import emoji, re
import pandas as pd

@st.experimental_memo()
def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}

    data = get_tsv_data("emoji_frequency", with_dates=True, index_col="Emoji", dtype={"Count": "int"})
    records = {}
    for date, df in data:
        df["%"] = 100*df["Count"] / df["Count"].sum()
        # print(date, i.head(5))
        # records[date] = list(f"{idx} ({row['%']:.2f}%)" for idx, row in df.head(5).iterrows())
        records[date] = list(f"{idx}" for idx, row in df.head(13).iterrows())
    print(records)

    return pd.DataFrame.from_dict(records, orient="index")#, columns=["1st", "2nd", "3rd", "4th", "5th"])

    # # ref: https://stackoverflow.com/a/38472352/5822988
    # df = reduce(lambda a, b: a.add(b, fill_value=0), data)
    # df["Count"] = df["Count"].astype("int")
    # df.sort_values(by="Count", ascending=False, inplace=True)    
    
    # return df

st.title(f"WIP: {__label__}")
x = get_data()

st.table(x)