from helpers.utils import get_tsv_data, render_as_table
import streamlit as st
from functools import reduce
import emoji, re


@st.experimental_memo()
def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}

    data = get_tsv_data("emoji_frequency", index_col="Emoji", dtype={"Count": "int"})
    data = list(data)

    # ref: https://stackoverflow.com/a/38472352/5822988
    df = reduce(lambda a, b: a.add(b, fill_value=0), data)
    df["Count"] = df["Count"].astype("int")
    df.sort_values(by="Count", ascending=False, inplace=True)
    from collections import Counter, defaultdict
    # c =  Counter()
    # d = defaultdict(list)
    # for i in df.index:
    #     c.update(map(ord,i))
    #     for j in map(ord, i):
    #         d[j].append(i)
    
    # print("-"*80)
    # for k,v in c.most_common(40):
    #     print(k, v, hex(k), chr(k), d[k][:10])
    # print("-"*80)
    #     # if chr(0xFE0E) in i or chr(0xFE0F) in i:
    #     # # if chr(127987) in i:
    #     #     print(i, list(map(ord,i)))
    # print("*"*80)
    
    
    
    return df

# 


##################

st.title("🏆 Most Common Emojis")
st.caption("List of most common emojis")

counts = get_data()

col1, col2, col3 = st.columns(3)
total = counts["Count"].sum()
col1.metric("Total emojis", f"{total:,d}")
col2.metric("Unique emojis", f"{len(counts):,d}")

# st.subheader("Log-Frequency plot")
# st.info("TBA")

st.subheader("Ranking")

show_as = st.radio("Show as:", ("counts", "percentage"), horizontal=True)

if show_as == "percentage":
    counts["Count"] = (100.0 * counts["Count"] / total).round(3)

items = counts.reset_index().values.tolist()
items = [
    item + [f"#{i} - {emoji.demojize(item[0])}"]
    for i, item in enumerate(items, start=1)
]

start = 0
per_page = 100
while start < len(items):
    st.subheader(f"#{start+1} - #{start+per_page}")
    html_table = render_as_table(items[start : start + per_page])
    st.markdown(html_table, unsafe_allow_html=True)
    start += per_page
