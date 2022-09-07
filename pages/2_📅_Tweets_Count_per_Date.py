import streamlit as st
from utils import get_tsv_data


@st.experimental_memo()
def get_data():
    return get_tsv_data("tweets_per_hour", dtype={"Hour": "str"})


st.header("📅 Tweets Count per Date")
st.caption("Number of Tweets collected per each Hour")

st.markdown(
    """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""
)

df = get_data()
days = sorted(set(df["Day"]))
################

col1, col2, col3 = st.columns(3)
col1.metric("Start Date", df["Day"].min())
col2.metric("End Date", df["Day"].max())
col3.metric("Total Days", f"{len(days)} days")

################
col1, col2, col3 = st.columns(3)
col1.metric("Total Tweets", f"{int(df['Count'].sum()):,d}")
col2.metric("Tweets per Day", "N/A")
col3.metric("Tweets per sec", "N/A")


# st.radio(
#     "What's your favorite movie genre",
#     ('Global', '🚦 Vertical (per hour)', '🚥 Horizontal (per day)'),
#     horizontal=True
# )

##########################################################################################


from bokeh.models import LinearColorMapper, LabelSet, ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Viridis256

mapper = LinearColorMapper(palette=Viridis256, low=0, high=df["Count"].max())

TOOLS = "save"

p = figure(  # title="US Unemployment",
    y_range=days,
    x_range=[str(i).zfill(2) for i in range(24)],
    x_axis_location="above",
    height=(len(days) + 1) * 24,
    tools="save,reset,xpan",  # toolbar_location="below",
    tooltips=[
        ("date", "@Day / @Hour:00"),
        ("count", "@Count"),
        ("coverage", "@{Coverage%}{0.2f}%"),
    ],
)

# p.grid.grid_line_color = None
# p.axis.axis_line_color = None
# p.axis.major_tick_line_color = None
# p.axis.major_label_text_font_size = "10px"
# p.axis.major_label_standoff = 0
# p.xaxis.major_label_orientation = 3.415926 / 3
p.rect(
    y="Day",
    x="Hour",
    width=1,
    height=1,
    source=df,
    fill_color={"field": "Count", "transform": mapper},
    line_color=None,
)
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

st.bokeh_chart(p, use_container_width=True)

st.caption("❗ ‒ denotes an interval with incomplete data, ⬜ ‒ marks missing data")
