import streamlit as st

st.set_page_config(page_title="Hello World", page_icon="random", layout="centered", initial_sidebar_state="auto", menu_items=None)

"""
Hello World
"""
import random
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
st.write(random.random())

st.title('This is a title')

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    code = '''def hello():
        print("Hello, Streamlit!")'''
    st.code(code, language='python')

st.button("Hello")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

