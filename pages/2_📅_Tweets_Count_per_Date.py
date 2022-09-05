from typing import Iterable, Dict
import glob, os, json
import pandas as pd
import streamlit as st

Tweet = Dict

from utils import iteratate_tweets, iterate_dates_range

    

def count_timestamps(tweets):
    from collections import Counter
    c = Counter()

    for tweet in tweets:
        created_at = tweet['data']['created_at']
        key = created_at.split(":")[0]
        c[key] += 1
    print(c)
    dates = sorted({date.split('T')[0] for date in c.keys()})
    dates = list(iterate_dates_range(min(dates), max(dates)))
    
    records = [
        {"Day": day, "Hour": str(h).zfill(2), "Count": c.get(f"{day}T{h:02}")}
        for day in dates
        for h in range(24)
    ]
    return pd.DataFrame.from_records(records)


@st.experimental_memo(persist="disk")
def get_data():
    tweets = iteratate_tweets("streams")

    df = count_timestamps(tweets)
    return df


st.header("📅 Tweets Count per Date")
st.caption("Number of Tweets collected per each Hour")

st.markdown("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
""")

df = get_data()

################

col1, col2, col3 = st.columns(3)
col1.metric("Start Date", df['Day'].min())
col2.metric("End Date", df['Day'].max())
col3.metric("Total Days", "3 days")

################
col1, col2, col3 = st.columns(3)
col1.metric("Total Tweets", f"{int(df['Count'].sum()):,d}")
col2.metric("Tweets per Day", "N/A")
col3.metric("Tweets per sec", "N/A")


st.radio(
    "What's your favorite movie genre",
    ('Global', '🚦 Vertical (per hour)', '🚥 Horizontal (per day)'),
    horizontal=True
)

##########################################################################################


from bokeh.models import LinearColorMapper
from bokeh.plotting import figure
from bokeh.palettes import Viridis256

mapper = LinearColorMapper(palette=Viridis256, low=0, high=df['Count'].max())

TOOLS = "save"
days = sorted(set(df['Day']))
p = figure(#title="US Unemployment",
           y_range=days, x_range=[str(i).zfill(2) for i in range(24)],
           x_axis_location="above", height=(len(days)+1)*24,
           tools="save", # toolbar_location="below",
           tooltips=[('date', '@Day / @Hour:00'), ('count', '@Count')]
)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10px"
p.axis.major_label_standoff = 0
# p.xaxis.major_label_orientation = pi / 3

p.rect(y="Day", x="Hour", width=1, height=1,
       source=df,
       fill_color={'field': 'Count', 'transform': mapper},
       line_color=None)

st.bokeh_chart(p, use_container_width=True)
