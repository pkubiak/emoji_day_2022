from typing import List, Dict
import emoji
from collections import Counter, defaultdict
import pandas as pd
from helpers.utils import render_as_table, sum_tsv_data, normalize_emoji
import streamlit as st
from functools import reduce
from helpers.constants import CATEGORIES

# TODO: Add more categories
# CATEGORIES = {
#     "hearts": "๐,๐,๐,๐,๐,๐,๐,๐,โฃ๏ธ,๐,โค๏ธโ๐ฅ,โค๏ธโ๐ฉน,โค๏ธ,๐งก,๐,๐,๐ค,๐,๐,๐ค,๐ค,๐ซ,โฅ๏ธ",
#     "birds": "๐ฆ,๐,๐,๐ฃ,๐ค,๐ฅ,๐ฆ,๐ง,๐๏ธ,๐ฆ,๐ฆ,๐ฆ,๐ฆฉ,๐ชถ,๐ฆค,๐ฆ,๐ฆข,๐ฆ",
#     "marine": "๐ณ,๐,๐ฌ,๐ฆญ,๐,๐ ,๐ก,๐ฆ,๐,๐,๐ชธ",
#     "flowers": "๐,๐ธ,๐ฎ,๐ชท,๐ต๏ธ,๐น,๐ฅ,๐บ,๐ป,๐ผ,๐ท",
#     "fruits": "๐,๐,๐,๐,๐,๐,๐,๐ฅญ,๐,๐,๐,๐,๐,๐,๐ซ,๐ฅ,๐,๐ซ,๐ฅฅ",
#     "vegetables": "๐ฅ,๐,๐ฅ,๐ฅ,๐ฝ,๐ถ๏ธ,๐ซ,๐ฅ,๐ฅฌ,๐ฅฆ,๐ง,๐ง,๐,๐ฅ,๐ซ,๐ฐ",
#     "mammals": "๐ต,๐,๐ฆ,๐ฆง,๐ถ,๐,๐ฆฎ,๐โ๐ฆบ,๐ฉ,๐บ,๐ด,๐,๐,๐ฏ,๐ฆ,๐โโฌ,๐,๐ฑ,๐ฆ,๐ฆ,๐,๐ฆ,๐ฆ,๐ฆ,๐ฆฌ,๐ฎ,๐,๐,๐,๐ท,๐,๐,๐ฝ,๐,๐,๐,๐ช,๐ซ,๐ฆ,๐ฆ,๐,๐ฐ,๐น,๐,๐,๐ญ,๐ฆ,๐ฆ,๐ฆฃ,๐,๐ฟ๏ธ,๐ฆซ,๐ฆ,๐ฆ,๐ป,๐ปโโ๏ธ,๐จ,๐ผ,๐ฆฅ,๐ฆฆ,๐พ,๐ฆก,๐ฆ,๐ฆจ",
#     "squares": "๐ฅ,๐ง,๐จ,๐ฉ,๐ฆ,๐ช,โฌ,โฌ,๐ซ",
#     "watches": "๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐,๐ ,๐ก,๐ข,๐ฃ,๐ค,๐ฅ,๐ฆ,๐ง",
#     "numbers": "0๏ธโฃ,1๏ธโฃ,2๏ธโฃ,3๏ธโฃ,4๏ธโฃ,5๏ธโฃ,6๏ธโฃ,7๏ธโฃ,8๏ธโฃ,9๏ธโฃ,๐",
#     "weather": "โ๏ธ,๐ค,โ๏ธ,๐ฅ,โ๏ธ,๐ฆ,๐ง,โ,๐ฉ,๐จ,โ๏ธ",
#     "moons": "๐,๐,๐,๐,๐,๐,๐,๐",
#     "shoes": "๐,๐,๐ฅพ,๐ฅฟ,๐ ,๐ก,๐ฉฐ,๐ข",
# }


@st.experimental_memo()
def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}
    df = sum_tsv_data("emoji_frequency", index_col="Emoji", dtype={"Count": "int"})
    df["Count"] = df["Count"].astype("int")

    most_common = defaultdict(Counter)
    for idx, row in df.iterrows():
        e = normalize_emoji(idx)
        most_common[e][idx] += int(row["Count"])

    most_common = {
        k: v.most_common()[0][0] for k, v in most_common.items()
    }
    counts = Counter()
    for idx, row in df.iterrows():
        e = normalize_emoji(idx)
        e = most_common[e]
        counts[e] += int(row["Count"])

    return most_common, counts


#############

most_common,  counts = get_data()

st.title(__label__)

st.markdown("Note: Different variants of the same emoji have been merged together!")

# TODO: Sort categories by total count
# TODO: display hover title

categories_counts = {
    c: sum(counts.get(most_common.get(normalize_emoji(e), e),0) for e in CATEGORIES[c].split(","))
    for c in CATEGORIES
}

for name, emojis in sorted(CATEGORIES.items(), key=lambda item: categories_counts[item[0]], reverse=True):
    category_counts = {
        k: counts.get(most_common.get(normalize_emoji(k), k), 0)
        for k in emojis.split(",")
    }


    total = sum(category_counts.values())
    items = sorted([
        [k, v, emoji.demojize(k)]
        for k, v in category_counts.items()], key=lambda v: v[1], reverse=True)

    st.subheader(f"{items[0][0]} {name.capitalize()} ({total:,d})")
    table_html = render_as_table(items)

    st.markdown(table_html, unsafe_allow_html=True)
    # st.markdown("<br>", unsafe_allow_html=True)