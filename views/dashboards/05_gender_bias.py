import streamlit as st
from helpers.utils import get_tsv_data
from collections import Counter
import pandas as pd
from functools import reduce
import emoji


def get_emoji_count():
    # TODO: Add source filtering
    # sources = {"Twitter for Android", "Twitter for iPhone", "Twitter Web App", "Twitter for Mac", "Twitter for iPad"}

    data = get_tsv_data("emoji_frequency", index_col="Emoji", dtype={"Count": "int"})
    data = list(data)

    # ref: https://stackoverflow.com/a/38472352/5822988
    df = reduce(lambda a, b: a.add(b, fill_value=0), data)
    df["Count"] = df["Count"].astype("int")
    df.sort_values(by="Count", ascending=False, inplace=True)

    return df


def render_emoji_as_image(emoji: str) -> str:
    codes = ["%x" % ord(i) for i in emoji]
    url = "https://abs-0.twimg.com/emoji/v2/svg/%s.svg" % ("-".join(codes))
    return url


@st.experimental_memo()
def get_data() -> pd.DataFrame:
    df = get_emoji_count()

    gender_related_emoji = set()
    cc = Counter()
    for i in df.index:
        z = str(i)

        for c in [0x1F3FB,0x1F3FC,0x1F3FD,0x1F3FE,0x1F3FF,0xFE0F]:
            z = z.replace(chr(c), "")

        m = None
        if z.endswith("\u200d\u2640"):
            z = z.removesuffix("\u200d\u2640")
            m = "\u2640"
        elif z.endswith("\u200d\u2642"):
            z = z.removesuffix("\u200d\u2642")
            m = "\u2642"

        if m:
            gender_related_emoji.add(z)
        cc[(z, m)] += df.loc[i]["Count"]
    # print(gender_related_emoji, len(gender_related_emoji))

    rows = []
    for i in gender_related_emoji:
        a, b, c = cc[(i,None)], cc[i,"\u2640"], cc[i,"\u2642"]
        # t = a+b+c
        # print(i, , round(100*a/t, 3), round(100*b/t, 3), round(100*c/t, 3))
        rows.append([i, emoji.demojize(i), a,b,c, "Neutral" if a == max([a,b,c]) else ("Male" if b<c else "Female")])

    df = pd.DataFrame.from_records(rows, columns=["Emoji", "Text", "Neutral", "Female", "Male", "Best"])
    df["Total"] = df["Neutral"] + df["Female"] + df["Male"]

    for k in ["Neutral", "Female", "Male"]:
        df[k] = (100.0*df[k]/df["Total"])
    df.sort_values(by="Total", ascending=False, inplace=True)
    return df

df = get_data()

st.dataframe(df)

#---------
st.subheader("Twitter Emoji Preview")

output = []

for i in df["Emoji"]:
    line = []
    for m in ["", "\u200d\u2640\ufe0f", "\u200d\u2642\ufe0f"]:
        url = render_emoji_as_image(i+m)
        line.append(f'<img src="{url}" style="height:48px"/>')
    output.append("".join(line))

st.markdown("<br>".join(output), unsafe_allow_html=True)