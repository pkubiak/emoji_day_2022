import os
import streamlit as st

glossary_path = os.path.join("views", "Glossary.md")
with open(glossary_path, encoding="utf-8") as file:
    st.markdown(file.read(), unsafe_allow_html=True)