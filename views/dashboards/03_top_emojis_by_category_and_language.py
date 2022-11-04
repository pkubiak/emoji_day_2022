import plotly.express as px
import streamlit as st
import plotly.figure_factory as ff
import numpy as np
from helpers.constants import CATEGORIES
from helpers.utils import get_tsv_data
from collections import Counter, defaultdict
import pandas as pd

# @st.experimental_memo()
def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}
    mapping = {
        e: k
        for k, v in CATEGORIES.items()
        for e in v.split(",")
    }
    
    data = get_tsv_data("top_language_emojis", index_col="Language", dtype={"Count": "int"})

    counts = defaultdict(Counter)
    for df in data:
        # print(df)
        for lang, row in df.iterrows():
            for item in row["Counts"].split(","):
                k, v = item.split(":")
                counts[lang][k] += int(v)

    results = []
    missing = Counter()
    categories_count = Counter()
    for lang, emojis in counts.items():
        best = {}
        # if lang == 'en':
        #     print(emojis.most_common())
        for e, v in emojis.most_common():
            if e not in mapping:
                missing[e] += v
            else:
                categories_count[mapping[e]] += v
                if mapping[e] not in best:
                    best[mapping[e]] = e
        for k in CATEGORIES:
            best.setdefault(k, None)
        # print(lang, best)
        best["total"] = sum(emojis.values())
        best["language"] = lang
        results.append(best)
    print(missing.most_common(200))
    keys = sorted(CATEGORIES, key=categories_count.__getitem__, reverse=True)
    return pd.DataFrame(results, columns=["language", "total"] + keys).set_index("language").sort_values(by=["total"], ascending=False)

    
    

    return best


st.title("📊 Top Emojis by Category and Language")
st.write(get_data())

if False:

    df = px.data.gapminder().query("year==2007")
    print(df)
    fig = px.choropleth(
        locations=["POL", "ESP"],
        # color="lifeExp", # lifeExp is a column of gapminder
        # hover_name="country", # column to add to hover information
        # color_continuous_scale=px.colors.sequential.Plasma
    )
    fig.update(
        layout_showlegend=False
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")
    # # fig.show()


    # fig.add_scattergeo(
    #   locations = df['iso_alpha'],
    #   text = "❤\uFE0F", ##df['pop'],
    #   mode = 'text'
    # ) 

    # Plot!

    st.title("🌍 Top Emojis by Country")
    st.plotly_chart(fig, use_container_width=True)

