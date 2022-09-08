from typing import List, Dict
import emoji
from collections import Counter
import pandas as pd
from utils import render_as_table, sum_tsv_data
import streamlit as st
from functools import reduce

# TODO: Add more categories
CATEGORIES = {
    "hearts": "💘,💝,💖,💗,💓,💞,💕,💟,❣️,💔,❤️‍🔥,❤️‍🩹,❤️,🧡,💛,💚,🤎,💙,💜,🖤,🤍,🫀,♥️",
    "birds": "🦃,🐔,🐓,🐣,🐤,🐥,🐦,🐧,🕊️,🦅,🦜,🦚,🦩,🪶,🦤,🦉,🦢,🦆",
    "marine": "🐳,🐋,🐬,🦭,🐟,🐠,🐡,🦈,🐙,🐚,🪸",
    "flowers": "💐,🌸,💮,🪷,🏵️,🌹,🥀,🌺,🌻,🌼,🌷",
    "fruits": "🍇,🍈,🍉,🍊,🍋,🍌,🍍,🥭,🍎,🍏,🍐,🍑,🍒,🍓,🫐,🥝,🍅,🫒,🥥",
    "vegetables": "🥑,🍆,🥔,🥕,🌽,🌶️,🫑,🥒,🥬,🥦,🧄,🧅,🍄,🥜,🫘,🌰",
    "mammals": "🐵,🐒,🦍,🦧,🐶,🐕,🦮,🐕‍🦺,🐩,🐺,🐴,🐆,🐅,🐯,🦁,🐈‍⬛,🐈,🐱,🦝,🦊,🐎,🦄,🦓,🦌,🦬,🐮,🐂,🐃,🐄,🐷,🐖,🐗,🐽,🐏,🐑,🐐,🐪,🐫,🦙,🦒,🐇,🐰,🐹,🐀,🐁,🐭,🦛,🦏,🦣,🐘,🐿️,🦫,🦔,🦇,🐻,🐻‍❄️,🐨,🐼,🦥,🦦,🐾,🦡,🦘,🦨",
    "squares": "🟥,🟧,🟨,🟩,🟦,🟪,⬛,⬜,🟫",
    "watches": "🕐,🕑,🕒,🕓,🕔,🕕,🕖,🕗,🕘,🕙,🕚,🕛,🕜,🕝,🕞,🕟,🕠,🕡,🕢,🕣,🕤,🕥,🕦,🕧",
    "numbers": "0️⃣,1️⃣,2️⃣,3️⃣,4️⃣,5️⃣,6️⃣,7️⃣,8️⃣,9️⃣,🔟",
    "weather": "☀️,🌤,⛅️,🌥,☁️,🌦,🌧,⛈,🌩,🌨,❄️",
    "moons": "🌕,🌖,🌗,🌘,🌑,🌒,🌓,🌔",
    "shoes": "👞,👟,🥾,🥿,👠,👡,🩰,👢",
}

@st.experimental_memo()
def get_data():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}
    df = sum_tsv_data("emoji_frequency", index_col="Emoji", dtype={"Count": "int"})
    df["Count"] = df["Count"].astype("int")

    counts = Counter()
    for idx, row in df.iterrows():
        counts[idx] = int(row["Count"])

    return counts


#############

counts = get_data()

st.title("📊 Top Emojis by Category")


# TODO: Sort categories by total count
# TODO: display hover title
for name, emojis in CATEGORIES.items():
    category_counts = {
        k: counts.get(k, 0)
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