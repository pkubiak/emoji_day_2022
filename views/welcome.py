import os
import streamlit as st

readme_path = os.path.join("README.md")
with open(readme_path, encoding="utf-8") as file:
    st.markdown(file.read(), unsafe_allow_html=True)