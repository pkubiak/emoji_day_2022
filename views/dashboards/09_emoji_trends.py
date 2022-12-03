import streamlit as st
from helpers.utils import get_tsv_data
import emoji
import pandas as pd


def get_data(e):
    results = {}
    for date, df in get_tsv_data("emoji_frequency", with_dates=True, index_col="Emoji",):
        total = df['Count'].sum()
        results[date] = round(100.0 * int(df['Count'].get(e, '0')) / total, 3)
    return results


icons = ["😀","😁", "😂", "🇬🇧", "🎻", "🔥", "🐔", "🌀", "🐈", "🍎"]

st.header(__label__)



# st.write(st.experimental_get_query_params())
st.caption("Pick emoji to analize:")

with st.container():
    cols = st.columns([1]*len(icons)+[4])
    for icon, col in zip(icons, cols):
        if col.button(icon):
            st.experimental_set_query_params(v='emoji-trends', emoji=icon)
            st.session_state.emoji_input = icon
            import time
            time.sleep(0.1)
            st.experimental_rerun()


emoji_input = cols[-1].text_input("Pick emoji to analize:", key='emoji_input', label_visibility='collapsed', placeholder="Your emoji")
emojis = emoji.emoji_list(emoji_input)

if len(emojis) != 1 or (emoji_input != emojis[0]["emoji"]):
    st.warning("Please, insert single emoji!")
    st.stop()

st.title(f"{emoji_input} ({emoji.demojize(emoji_input).strip(':')})")


# st.markdown("""
# <style>
# div[data-testid="stHorizontalBlock"] {
#     background:blue;
#     display: inline-block;
# }
# div[data-testid="stHorizontalBlock"] > div {
#     display: inline-block;
# }
# </style>
# <script>
# alert("hello");
# </script>
# """, unsafe_allow_html=True)

# cols = st.columns(len(icons))
# with st.expander("See explanation"):
#     st.write("""
#         The chart above shows some numbers I picked for you.
#         I rolled actual dice for these, so they're *guaranteed* to
#         be random.
#     """)
#     st.image("https://static.streamlit.io/examples/dice.jpg")



# if st.button("click"):
#     st.experimental_set_query_params(emoji="😀")

# if st.button("click2"):
#     st.experimental_set_query_params(emoji="🐈")

data = get_data(emoji_input)
df = pd.DataFrame.from_records(list(data.items()), columns=["Date", "Frequency"])


st.line_chart(df, x="Date", y="Frequency")

# out = st.experimental_get_query_params()

# out


# st.markdown("<a class='css-1cpxqw2 edgvbvh9' href='Emoji_Trend?emoji=😍' target='_self'>xyz</a>", unsafe_allow_html=True)