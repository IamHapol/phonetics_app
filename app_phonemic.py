import streamlit as st
from utils.css import inject_css
from sections import phonemic

st.set_page_config(page_title="Phonemic", layout="wide")
inject_css()
phonemic.show()
