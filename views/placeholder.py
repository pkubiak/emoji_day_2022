import streamlit as st
import random
from helpers.multi_app import navigate_to

count = int(st.experimental_get_query_params().get("number", [0])[0])

st.title(f"🐈 {__view__}")
st.write(st.experimental_get_query_params())
st.header("🐟" * count)


navigate_to("Set 1", "about-us", {"number": 1})
navigate_to("Set 6", "about-us", {"number": 6})
navigate_to("Random", "about-us", {"number": random.randint(0,10)})

navigate_to("Error page", "asdada")