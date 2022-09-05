from typing import List, Dict
import emoji
from collections import Counter
import pandas as pd
from utils import iteratate_tweets, render_as_table
import streamlit as st

Tweet = Dict

class TopEmojiByCategory():
    CATEGORIES = {
        "hearts": "💘,💝,💖,💗,💓,💞,💕,💟,❣️,💔,❤️‍🔥,❤️‍🩹,❤️,🧡,💛,💚,🤎,💙,💜,🖤,🤍,🫀,♥️",
        "birds": "🦃,🐔,🐓,🐣,🐤,🐥,🐦,🐧,🕊️,🦅,🦜,🦚,🦩,🪶,🦤,🦉,🦢,🦆",
        "marine": "🐳,🐋,🐬,🦭,🐟,🐠,🐡,🦈,🐙,🐚,🪸,",
        "flowers": "💐,🌸,💮,🪷,🏵️,🌹,🥀,🌺,🌻,🌼,🌷",
        "fruits": "🍇,🍈,🍉,🍊,🍋,🍌,🍍,🥭,🍎,🍏,🍐,🍑,🍒,🍓,🫐,🥝,🍅,🫒,🥥",
        "vegetables": "🥑,🍆,🥔,🥕,🌽,🌶️,🫑,🥒,🥬,🥦,🧄,🧅,🍄,🥜,🫘,🌰",
        "mammals": "🐵,🐒,🦍,🦧,🐶,🐕,🦮,🐕‍🦺,🐩,🐺,🐴,🐆,🐅,🐯,🦁,🐈‍⬛,🐈,🐱,🦝,🦊,🐎,🦄,🦓,🦌,🦬,🐮,🐂,🐃,🐄,🐷,🐖,🐗,🐽,🐏,🐑,🐐,🐪,🐫,🦙,🦒,🐇,🐰,🐹,🐀,🐁,🐭,🦛,🦏,🦣,🐘,🐿️,🦫,🦔,🦇,🐻,🐻‍❄️,🐨,🐼,🦥,🦦,🐾,🦡,🦘,🦨",
    }

    def __init__(self):
        self.counter = Counter()

    def update(self, tweets: List[Tweet]):
        for tweet in tweets:
            text = tweet["data"]["text"]
            
            self.counter.update(i["emoji"] for i in emoji.emoji_list(text))

    def render(self) -> Dict[str, pd.DataFrame]:
        results = {}

        for category, emojis in self.CATEGORIES.items():
            # df = pd.DataFrame.from_dict({
            #     k: self.counter.get(k, 0)
            #     for k in emojis
            # }, orient="index", columns=["count"]).sort_values(by="count")

            results[category] = {
                k: self.counter.get(k, 0)
                for k in emojis.split(",")
            }
        return results


# @st.experimental_memo()
def get_data():
    tweets = iteratate_tweets("streams")

    cc = TopEmojiByCategory()
    cc.update(tweets)

    return cc

#############

cc = get_data()

st.title("💗 Top Emojis by Category")

for k, v in cc.render().items():
    count = sum(v.values())
    items = sorted(v.items(), key=lambda v: v[1], reverse=True)

    st.subheader(f"{items[0][0]} {k.capitalize()} ({count:,d})")
    table_html = render_as_table(items)

    st.markdown(table_html, unsafe_allow_html=True)
    # st.markdown("<br>", unsafe_allow_html=True)