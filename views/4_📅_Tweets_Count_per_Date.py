from distutils.command.build import build
import streamlit as st
from utils import get_tsv_data
import pandas as pd
from bokeh.models import LinearColorMapper, LabelSet, ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Viridis256




@st.experimental_memo()
def get_data():
    dfs = get_tsv_data("tweets_per_hour", dtype={"Hour": "str"})
    return pd.concat(dfs, ignore_index=True)


def build_bokeh_chart(df, field: str):
    days = sorted(set(df["Day"]))

    p = figure(  # title="US Unemployment",
        y_range=days,
        x_range=[str(i).zfill(2) for i in range(24)],
        x_axis_location="above",
        height=(len(days) + 2) * 24,
        tools="save",  # toolbar_location="below",
        tooltips=[
            ("date", "@Day / @Hour:00"),
            ("count", "@{Count}{0,}"),
            ("coverage", "@{Coverage%}{0.2f}%"),
            ("tweets per sec.", "@{Tweets/s}{0.2f}"),
        ],
        x_axis_label="Hour [UTC]",
    )

    p.grid.grid_line_color = None
    # p.axis.axis_line_color = None
    # p.axis.major_tick_line_color = None
    # p.axis.major_label_text_font_size = "10px"
    # p.axis.major_label_standoff = 0
    # p.xaxis.major_label_orientation = 3.415926 / 3

    mapper = LinearColorMapper(palette=Viridis256, low=0, high=df[field].max())
    p.rect(
        y="Day",
        x="Hour",
        width=1,
        height=1,
        source=df,
        fill_color={"field": field, "transform": mapper},
        line_color=None,
    )

    if field != "Coverage%":
        df["Label"] = df["Coverage%"].map(lambda v: "❗" if v < 100.00 else "")

        labels = LabelSet(
            x="Hour",
            y="Day",
            text="Label",
            text_align="center",
            text_baseline="middle",
            text_color="white",
            x_offset=0,
            y_offset=0,
            source=ColumnDataSource(df),
        )
        p.add_layout(labels)
    
    return p

#############

st.header("📅 Tweets Count per Date")
st.caption("Number of Tweets collected per each Hour")

st.markdown(
    """
Dashboard present detailed statistics about collected Tweets, which are used as a data source for other dashboards.

Tweets are collected using [Twitter Streaming API](https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream).
"""
)

st.info(
    "Due to limitation of Twitter Streaming API, only around 1% of all tweets is collected!",
    icon="ℹ️",
)

df = get_data()
df["Tweets/s"] = df["Count"] / (3600 * df["Coverage%"] / 100.0)

total_tweets = df["Count"].sum()
total_seconds = 3600.0 * df["Coverage%"].sum() / 100
tweets_per_sec = total_tweets / total_seconds

################

col1, col2, col3 = st.columns(3)
col1.metric("Start Date", df["Day"].min())
col2.metric("End Date", df["Day"].max())
# col3.metric("Total Days", f"{len(days)} days")
d, h = divmod(total_seconds / 3600.0, 24)

col3.metric("Total time", f"{int(d):d}days {int(h):d}hours")

################
col1, col2, col3 = st.columns(3)


col1.metric("Total Tweets", f"{total_tweets:,d}")
col2.metric("Tweets per day [avg]", f"{24*60*60*tweets_per_sec:,.0f}")
col3.metric("Tweets per sec [avg]", f"{tweets_per_sec:.2f}")


field = st.radio(
    "",  # "What's your favorite movie genre",
    ("Count", "Coverage%", "Tweets/s"),
    format_func={
        "Count": "Number of Tweets",
        "Coverage%": "Data coverage",
        "Tweets/s": "Tweets per second",
    }.get,
    horizontal=True,
)


st.bokeh_chart(build_bokeh_chart(df, field), use_container_width=True)

st.caption("❗ ‒ denotes an interval with incomplete data, ⬜ ‒ marks missing data")
