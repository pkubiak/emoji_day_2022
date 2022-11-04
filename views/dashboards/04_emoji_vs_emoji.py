import streamlit as st
import emoji
import plotly.express as px
from helpers.constants import LANG_TO_COUNTRY
from helpers.utils import get_tsv_data
from collections import defaultdict, Counter

def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}
    data = get_tsv_data("top_language_emojis", index_col="Language", dtype={"Count": "int"})

    counts = defaultdict(Counter)
    for df in data:
        # print(df)
        for lang, row in df.iterrows():
            for item in row["Counts"].split(","):
                k, v = item.split(":")
                counts[lang][k] += int(v)
    return counts

def get_results(e1, e2) -> dict[str, str]:
    counts = get_data()
    results = {}
    for k, v in LANG_TO_COUNTRY.items():
        v1 = counts[k].get(e1, 0)
        v2 = counts[k].get(e2, 0)

        if v1 == v2 == 0:
            val = None
        else:
            val = e1 if v1 >= v2 else e2
        if isinstance(v,str): v = [v]
        for i in v:
            results[i] = val
    # missing = Counter()
    # for k in counts:
    #     if k not in LANG_TO_COUNTRY:
    #         missing[k] += sum(counts[k].values())
    # st.write(missing.most_common())
    overall = {
        e1: sum(counts[k].get(e1,0) for k in counts),
        e2: sum(counts[k].get(e2,0) for k in counts),
    }
    return results, overall


st.title("🥊 Emoji vs Emoji")
st.markdown("""
Dashboard compare usage of two emoji among different countries, and show the most used.

Countries matching is based on national languages, and therefore may not be 100% accurate.
""")
examples = [("😭", "😂"), ("🐈", "🐕"), ("🍏","🍎"), ("🍆", "🍑"), ("🍷", "🍺"),]

output = st.container()
cols_inputs = st.columns(2)
cols = st.columns(len(examples)+1)


# st.markdown("<a href='x'>Hello World</a>", unsafe_allow_html=True)


cols[0].write("Try these:")
for col, example in zip(cols[1:], examples):
    with col:
        if st.button(f"{example[0]} vs {example[1]}"):
            st.session_state.emoji1 = example[0]
            st.session_state.emoji2 = example[1]


with cols_inputs[0]:
    emoji1 = st.text_input("Emoji 1", key='emoji1')
with cols_inputs[1]:
    emoji2 = st.text_input("Emoji 2", key="emoji2")




if not(emoji1 and emoji2):
    with output:
        st.warning("Select two emojis to show comparison")
    st.stop()

if (emoji1 not in emoji.EMOJI_DATA) or (emoji2 not in emoji.EMOJI_DATA):
    st.error("Inserted text is not emoji!")
    st.stop()


results, overall = get_results(emoji1, emoji2)
keys = list(results.keys())
values = list(results.values())

c1 = "#636EFA"
c2 = "#EF553B"

colors = [(c1 if v == emoji1 else c2) if v else v for v in values]

fig = px.choropleth(locations=keys, color=colors, color_discrete_map="identity")

fig.add_scattergeo(
  locations = keys,
  text = values,
  mode = 'text',textfont_size=24
) 
fig.update(
    layout_showlegend=False,            
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    height=330,

)



with output:
    st.plotly_chart(fig, use_container_width=False)
    perc = (100.0 * overall[emoji1]) / (overall[emoji1] + overall[emoji2])
    st.markdown(f"""
        <div style="display:flex; align-items: center;padding-bottom: 20px;">
            <span>{emoji1}</span>
            <div style="flex-grow:1;height:10px;background:{c2};margin: 0 10px;position:relative;">
                <span style="position:absolute;left:0;top:100%;">{perc:.2f}%</span>
                <div style="width:{perc}%;background:{c1};height:100%"></div>
                <span style="position:absolute;right:0;top:100%;">{100-perc:.2f}%</span>
            </div>
            <span>{emoji2}</span>
        </div>
    """, unsafe_allow_html=True)