import streamlit as st
from sections import articulators, vowels, phonemic

st.set_page_config(page_title="Phonetics App", layout="wide")

# Optional: hide Streamlit default menu & footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Phonetics Learning App")
st.markdown("Click the sections below to expand them. All sections are preloaded in memory.")

# --- Helper function to wrap sections in expander with a prefix ---
def show_section(section_module, name):
    """Wrap a section in an expander and give it a unique key prefix."""
    with st.expander(name, expanded=False):
        # Inject a global prefix so all keys inside section are unique
        if hasattr(section_module, "show"):
            section_module.show(key_prefix=name.lower())

# Display sections
show_section(articulators, "Articulators")
show_section(vowels, "Vowels")
show_section(phonemic, "Phonemic Chart")
