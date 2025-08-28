# utils/audio_utils.py
from gtts import gTTS
from io import BytesIO
import base64
import streamlit as st

@st.cache_data
def text_to_speech(text, lang='en', filename=None):
    """
    Convert text to speech.
    
    Parameters:
        text (str): Text to convert.
        lang (str): Language code ('en', 'en-uk', etc.).
        filename (str, optional): If provided, saves the mp3 to this file.
    
    Returns:
        bytes: Audio bytes if filename is None.
    """
    tts = gTTS(text=text, lang=lang)
    
    if filename:
        tts.save(filename)
        return None
    
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def autoplay_audio(audio_bytes):
    """
    Autoplay audio in Streamlit via HTML.
    """
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_html = f"""
        <audio autoplay class="hidden-audio">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
