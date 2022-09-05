import streamlit as st
from utils import iteratate_tweets
from collections import Counter
import pandas as pd


@st.experimental_memo(persist="disk")
def get_data():
    sources = Counter()
    for tweet in iteratate_tweets("streams"):
        source = tweet["data"]["source"]
        sources[source] += 1

    return sources

data = get_data().most_common()
total = sum(i[1] for i in data)
# data = [i for i in data if i[0].startswith("Twitter")]

df = pd.DataFrame.from_records(data, columns=["Source", "Frequency"])
df["%"] = (100.0*df["Frequency"] / df["Frequency"].sum()).round(3)

st.dataframe(df, width=None)