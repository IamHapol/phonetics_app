import streamlit as st
from utils.css import inject_css
from sections import vowels

st.set_page_config(page_title="Vowels", layout="wide")
inject_css()
vowels.show()
