from utils import iteratate_tweets, render_as_table
import emoji
import streamlit as st
from collections import Counter


@st.experimental_memo(persist="disk")
def get_emojis():
    c = Counter()
    sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}
    for tweet in iteratate_tweets("streams"):
        source = tweet["data"]["source"]
        if source not in sources:
            continue
        # sensitive = tweet["data"].get("possibly_sensitive", False)
        # if sensitive is not True:
        #     continue
        text = tweet["data"]["text"]
        emojis = emoji.emoji_list(text)
        c.update(e['emoji'] for e in emojis)

    return c

# get_emojis.clear()


##################

st.title("🏆 Most Common Emojis")
st.caption("List of most common emojis")

items = list(get_emojis().most_common())

col1, col2, col3 = st.columns(3)
total = sum(i[1] for i in items)
col1.metric("Total emojis", f"{total:,d}")
col2.metric("Unique emojis", f"{len(items):,d}")

st.warning('This is a warning', icon="⚠️")

st.header("Most common Emojis Ranking")

show_as = st.radio("Show as:", ('counts', 'percentage'), horizontal=True)
if show_as == "percentage":
    items = [[i[0], round(100*i[1]/total,3)] for i in items]
print(items[:10])

start = 0
per_page = 100
while start < len(items):
    st.subheader(f"#{start+1} - #{start+per_page}")
    st.markdown(render_as_table(items[start:start+per_page]), unsafe_allow_html=True)
    start += per_page
