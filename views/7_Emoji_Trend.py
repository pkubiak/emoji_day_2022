import streamlit as st
from utils import get_tsv_data


st.header("Emoji Trend")


icons = ["😀","😁", "😂", "🤣", "😃", "😄", "😅", "😆", "🐈", "🍎"]

st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    background:blue;
    display: inline-block;
}
div[data-testid="stHorizontalBlock"] > div {
    display: inline-block;
}
</style>
<script>
alert("hello");
</script>
""", unsafe_allow_html=True)

# cols = st.columns(len(icons))
with st.expander("See explanation"):
    st.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
    st.image("https://static.streamlit.io/examples/dice.jpg")

with st.container():
    for icon in icons:
        if st.button(icon):
            st.experimental_set_query_params(emoji=icon)

# if st.button("click"):
#     st.experimental_set_query_params(emoji="😀")

# if st.button("click2"):
#     st.experimental_set_query_params(emoji="🐈")

out = st.experimental_get_query_params()

out


st.markdown("<a class='css-1cpxqw2 edgvbvh9' href='Emoji_Trend?emoji=😍' target='_self'>xyz</a>", unsafe_allow_html=True)