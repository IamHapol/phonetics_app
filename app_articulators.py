import streamlit as st
from utils.css import inject_css  # keep if you have this file
from sections import articulators

st.set_page_config(page_title="Articulators", layout="wide")
inject_css()  # optional, remove if you don't have this
articulators.show()
