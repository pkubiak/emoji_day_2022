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
#     "hearts": "💘,💝,💖,💗,💓,💞,💕,💟,❣️,💔,❤️‍🔥,❤️‍🩹,❤️,🧡,💛,💚,🤎,💙,💜,🖤,🤍,🫀,♥️",
#     "birds": "🦃,🐔,🐓,🐣,🐤,🐥,🐦,🐧,🕊️,🦅,🦜,🦚,🦩,🪶,🦤,🦉,🦢,🦆",
#     "marine": "🐳,🐋,🐬,🦭,🐟,🐠,🐡,🦈,🐙,🐚,🪸",
#     "flowers": "💐,🌸,💮,🪷,🏵️,🌹,🥀,🌺,🌻,🌼,🌷",
#     "fruits": "🍇,🍈,🍉,🍊,🍋,🍌,🍍,🥭,🍎,🍏,🍐,🍑,🍒,🍓,🫐,🥝,🍅,🫒,🥥",
#     "vegetables": "🥑,🍆,🥔,🥕,🌽,🌶️,🫑,🥒,🥬,🥦,🧄,🧅,🍄,🥜,🫘,🌰",
#     "mammals": "🐵,🐒,🦍,🦧,🐶,🐕,🦮,🐕‍🦺,🐩,🐺,🐴,🐆,🐅,🐯,🦁,🐈‍⬛,🐈,🐱,🦝,🦊,🐎,🦄,🦓,🦌,🦬,🐮,🐂,🐃,🐄,🐷,🐖,🐗,🐽,🐏,🐑,🐐,🐪,🐫,🦙,🦒,🐇,🐰,🐹,🐀,🐁,🐭,🦛,🦏,🦣,🐘,🐿️,🦫,🦔,🦇,🐻,🐻‍❄️,🐨,🐼,🦥,🦦,🐾,🦡,🦘,🦨",
#     "squares": "🟥,🟧,🟨,🟩,🟦,🟪,⬛,⬜,🟫",
#     "watches": "🕐,🕑,🕒,🕓,🕔,🕕,🕖,🕗,🕘,🕙,🕚,🕛,🕜,🕝,🕞,🕟,🕠,🕡,🕢,🕣,🕤,🕥,🕦,🕧",
#     "numbers": "0️⃣,1️⃣,2️⃣,3️⃣,4️⃣,5️⃣,6️⃣,7️⃣,8️⃣,9️⃣,🔟",
#     "weather": "☀️,🌤,⛅️,🌥,☁️,🌦,🌧,⛈,🌩,🌨,❄️",
#     "moons": "🌕,🌖,🌗,🌘,🌑,🌒,🌓,🌔",
#     "shoes": "👞,👟,🥾,🥿,👠,👡,🩰,👢",
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