# filename: phonemic.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Interactive Phonetics Lab", layout="wide")

# --------------------- CSS Injection ---------------------
def inject_css():
    st.markdown("""
    <style>
    /* Main container background: more neutral */
    .main {
        background: linear-gradient(135deg, #eef1f5 0%, #e3e7ee 100%);
    }

    /* App-level background, neutral + dark-mode ready */
    .stApp {
        background: linear-gradient(135deg, #f2f4f8 0%, #e6e9ef 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2b2f38;
    }

    /* Real dark-mode */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
            color: #e5e7eb;
        }
    }

    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 10px;
    }

    /* Section Headings */
    .section-heading {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        color: #2c3e50 !important;
        border-bottom: 3px solid #7B68EE;
        padding-bottom: 0.5rem;
    }

    /* Expandable Title */
    .expandable-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1C39BB;
        margin: 1.5rem 0 0.8rem 0;
        padding: 0.8rem;
        background-color: #f0f8ff;
        border-radius: 12px;
        border-left: 5px solid #1C39BB;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .expandable-title:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    /* Hover Text */
    .hover-text {
        font-weight: 700 !important;
        color: #1f2937 !important;
        transition: all 0.3s ease !important;
        line-height: 1.6;
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(255,255,255,0.7);
    }

    .hover-text:hover {
        color: #1C39BB !important;
        background-color: rgba(255,255,255,0.9);
        transform: scale(1.01);
    }

    /* Phonetic Symbols */
    .phonetic {
        color: #16a085 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Courier New', monospace;
        background-color: #f8f9fa;
        padding: 4px 8px;
        border-radius: 4px;
        border: 1px solid #e9ecef;
    }

    /* Container cards (neutral + dark mode) */
    .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        padding: 25px;
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(230,235,245,0.9);
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.12);
    }
    @media (prefers-color-scheme: dark) {
        .card {
            background: rgba(17, 24, 39, 0.7);
            border: 1px solid rgba(55, 65, 81, 0.7);
        }
    }

    /* Section dividers */
    .divider {
        height: 4px;
        border-radius: 3px;
        background: linear-gradient(to right, #7B68EE, #87CEEB, #32CD32, #FF69B4);
        margin: 30px 0;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    /* Headings */
    h2, h3 {
        color: #1C39BB;
        text-align: center;
        font-weight: 700;
        transition: color 0.3s ease;
        margin-top: 1.5rem;
    }
    h2:hover, h3:hover { color: #4169E1; }

    /* Default buttons (blue) */
    .stButton > button {
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 0.8em 1.5em;
        font-size: 1em;
        font-weight: 700 !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        background: linear-gradient(135deg, #1C39BB 0%, #4169E1 100%) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .stButton > button:after {
        content: "";
        position: absolute;
        background: rgba(255, 255, 255, 0.4);
        width: 5px;
        height: 200%;
        top: -50%;
        left: -40px;
        transform: rotate(25deg);
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { left: -40px; }
        60% { left: 110%; }
        100% { left: 110%; }
    }
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* IPA Table Styling */
    .ipa-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .ipa-table th, .ipa-table td {
        border: 1px solid #4a6572;
        padding: 12px;
        text-align: left;
        color: white !important;
    }
    .ipa-table th {
        font-weight: bold;
        background-color: #1C39BB !important;
        font-size: 1.1rem;
    }
    .ipa-table tr:nth-child(even) { background-color: rgba(255,255,255,0.05) !important; }
    .ipa-table tr:hover { background-color: rgba(255,255,255,0.1) !important; }

    /* Progress bar */
    .progress-container {
        width: 100%;
        background-color: #e0e0e0;
        border-radius: 10px;
        margin: 20px 0;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
    }
    .progress-bar {
        height: 20px;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 20px;
    }

    /* Tooltip */
    .tooltip { position: relative; display: inline-block; border-bottom: 1px dotted #16a085; cursor: help; }
    .tooltip .tooltiptext {
        visibility: hidden; width: 200px; background-color: #2c3e50; color: #fff; text-align: center; border-radius: 6px; padding: 10px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -100px; opacity: 0; transition: opacity 0.3s; font-weight: normal; box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }

    /* Practice question text: bold + black */
    .practice-question {
        font-weight: 800 !important;
        color: #0f172a !important;
        font-size: 1.05rem;
        margin-bottom: 10px;
    }
    @media (prefers-color-scheme: dark) {
        .practice-question { color: #f1f5f9 !important; }
    }

    /* ---- Green "card buttons" for options using radio ---- */
    .stRadio [role="radiogroup"]{
        display: flex; gap: 12px; flex-wrap: wrap;
    }
    .stRadio [role="radiogroup"] label {
        background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
        color: #ffffff !important;
        font-weight: 800 !important;
        padding: 12px 18px;
        border-radius: 16px;
        text-align: center;
        margin: 6px 0;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        user-select: none;
    }
    .stRadio [role="radiogroup"] label:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    /* hide default radio circle */
    .stRadio [role="radiogroup"] input { position: absolute; opacity: 0; width: 0; height: 0; }

    /* Selected state */
    .stRadio [role="radiogroup"] label:has(input:checked) {
        border-color: #f7fafc;
        box-shadow: 0 0 0 3px #38a169;
        transform: scale(1.02);
        filter: brightness(1.05);
    }

    /* Toggles/CTA badges */
    .lux-btn {
        display: inline-block;
        font-weight: 700 !important;
        border-radius: 15px !important;
        padding: 12px 24px !important;
        border: none !important;
        color: black !important;
        margin: 8px 6px !important;
        transition: all 0.3s ease !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
        font-size: 1rem;
    }
    .lux-btn:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 18px rgba(0,0,0,0.25) !important;
    }
    .lux-btn::after {
        content: "";
        position: absolute;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        top: 50%;
        left: 50%;
        pointer-events: none;
        transform: translate(-50%, -50%) scale(0);
        background: rgba(255,255,255,0.3);
        animation: ripple 3s infinite;
    }
    @keyframes ripple {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0.7; }
        50% { transform: translate(-50%, -50%) scale(2.5); opacity: 0; }
        100% { opacity: 0; }
    }
    .answer-btn { background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%) !important; }
    .recap-btn { background: linear-gradient(135deg, #87ceeb 0%, #ffffff 100%) !important; color:#1e3c72 !important; }
    .funfact-btn { background: linear-gradient(135deg, #93c5fd 0%, #60a5fa 100%) !important; color:#0b1953 !important; }
    .mindblower-btn { background: linear-gradient(135deg, #b8860b 0%, #ffd700 100%) !important; }

    /* Persian lines: remove yellow, keep blue-only + hover */
    .farsi-line {
        background: linear-gradient(135deg, #0ea5e9 0%, #1d4ed8 100%) !important;
        color: white !important;
        padding: 12px 18px !important;
        border-left: 5px solid #1e40af !important;
        margin-bottom: 8px !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .farsi-line:hover {
        transform: translateX(5px);
        filter: brightness(1.06);
    }

    /* Fade-in animation */
    .fade-in { animation: fadeIn 1s ease-in-out; }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# --------------------- Encouragement Messages ---------------------
ENCOURAGEMENTS_CORRECT = [
    "You crushed it, mate!", "Nice one, bro!", "On fire, fam!", "Keep it up, legend!",
    "Boom! Nailed it!", "You're a star!", "Legendary work!", "You got this!",
    "Solid job!", "You're killing it!", "Smashed it!", "Proper good, mate!",
    "Dead brilliant!", "That's the one!", "Spot on!", "You're nailing it!",
    "Too easy for you!", "Big brain moves!", "Certified genius!", "That's how it's done!"
]

ENCOURAGEMENTS_WRONG = [
    "Try again, champ!", "Close, but not quite!", "Almost got it!", "Give it another go!",
    "Not quite. Try again!", "Oops, have another shot!", "Hang in there!", "Don't give up!",
    "Take another look!", "Hmm, not this one!", "Nah, that ain't it!", "You'll get the next one!",
    "Shake it off, try again!", "Nearly there!", "Bit off there, mate!", "Have another crack at it!",
    "No stress, try again!", "Keep grinding!", "You'll suss it!", "Almost, fam!", "Next time for sure!"
]

# --------------------- Text to Speech ---------------------
@st.cache_data(show_spinner=False)
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception:
        return None

# --------------------- Vowel Table ---------------------
def vowel_table():
    st.markdown('<div class="expandable-title">📍 Vowel Space Map</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <table class="ipa-table">
        <tr><th>Front</th><th>Central</th><th>Back</th></tr>
        <tr><td>Close: [i] ~ (English: [iː])</td><td>—</td><td>Close: [u] ~ (English: [uː])</td></tr>
        <tr><td>Open: [a] ~ (English: [æ] not as open)</td><td>—</td><td>Open: [ɑ] ~ (English: [ɑː])</td></tr>
      </table>
      <div class="divider"></div>
      <table class="ipa-table">
        <tr><th>Lip Posture</th><th>Example</th></tr>
        <tr><td>Rounded</td><td>[u] (think 'too')</td></tr>
        <tr><td>Spread</td><td>[i] (think 'see')</td></tr>
        <tr><td>Neutral</td><td>English hesitation "er"</td></tr>
      </table>
    </div>
    """, unsafe_allow_html=True)

# --------------------- Progress Tracking ---------------------
def update_progress():
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'completed_sections' not in st.session_state:
        st.session_state.completed_sections = set()
    total_sections = 7  # Added Listening Challenge section
    completed = len(st.session_state.completed_sections)
    st.session_state.progress = (completed / total_sections) * 100

# --------------------- Toast Notification ---------------------
def show_toast(message, is_success=True):
    if is_success:
        st.success(message)
    else:
        st.error(message)
    time.sleep(2)

# --------------------- Practice helpers ---------------------
def init_question_state(qidx):
    if f"q{qidx}_selected" not in st.session_state:
        st.session_state[f"q{qidx}_selected"] = None
    if f"q{qidx}_is_correct" not in st.session_state:
        st.session_state[f"q{qidx}_is_correct"] = None
    if f"q{qidx}_attempts" not in st.session_state:
        st.session_state[f"q{qidx}_attempts"] = 0

def reset_question(qidx):
    st.session_state.pop(f"q{qidx}_selected", None)
    st.session_state.pop(f"q{qidx}_is_correct", None)
    st.session_state.pop(f"q{qidx}_attempts", None)
    st.session_state.pop(f"radio_{qidx}", None)

# --------------------- Listening Challenge ---------------------
def listening_challenge():
    st.markdown('<div class="expandable-title">🎧 Listening Challenge</div>', unsafe_allow_html=True)
    with st.expander("Test your ears! Click to play a word and identify the vowel sound", expanded=False):
        
        # Word bank with words and their vowel sounds
        word_bank = [
            {"word": "bit", "vowel": "ɪ", "accent": "UK"},
            {"word": "beat", "vowel": "iː", "accent": "UK"},
            {"word": "bet", "vowel": "e", "accent": "UK"},
            {"word": "bat", "vowel": "æ", "accent": "UK"},
            {"word": "cut", "vowel": "ʌ", "accent": "UK"},
            {"word": "cart", "vowel": "ɑː", "accent": "UK"},
            {"word": "put", "vowel": "ʊ", "accent": "UK"},
            {"word": "boot", "vowel": "uː", "accent": "UK"},
            {"word": "bird", "vowel": "ɜː", "accent": "UK"},
            {"word": "about", "vowel": "ə", "accent": "UK"},
            {"word": "bit", "vowel": "ɪ", "accent": "US"},
            {"word": "beat", "vowel": "i", "accent": "US"},
            {"word": "bet", "vowel": "ɛ", "accent": "US"},
            {"word": "bat", "vowel": "æ", "accent": "US"},
            {"word": "cut", "vowel": "ʌ", "accent": "US"},
            {"word": "cart", "vowel": "ɑ", "accent": "US"},
            {"word": "put", "vowel": "ʊ", "accent": "US"},
            {"word": "boot", "vowel": "u", "accent": "US"},
            {"word": "bird", "vowel": "ɝ", "accent": "US"},
            {"word": "about", "vowel": "ə", "accent": "US"}
        ]
        
        # Initialize session state for challenge
        if 'current_word' not in st.session_state:
            st.session_state.current_word = random.choice(word_bank)
        if 'challenge_attempts' not in st.session_state:
            st.session_state.challenge_attempts = 0
        if 'challenge_correct' not in st.session_state:
            st.session_state.challenge_correct = 0
        
        current_word = st.session_state.current_word
        
        # Play button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔊 Play Word", key="play_challenge"):
                audio_bytes = text_to_speech(current_word["word"], lang='en' if current_word["accent"] == "US" else 'en-uk')
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')
                else:
                    st.info("🔇 Audio preview")
        
        with col2:
            st.markdown(f"**Word:** {current_word['word'].capitalize()}")
        
        # Vowel identification
        st.markdown("**What vowel sound did you hear?**")
        vowel_options = ["ɪ", "iː", "e", "æ", "ʌ", "ɑː", "ʊ", "uː", "ɜː", "ə", "i", "ɛ", "ɑ", "ɝ"]
        selected_vowel = st.radio(
            "Select the vowel sound:",
            options=vowel_options,
            key="vowel_selection",
            horizontal=True
        )
        
        # Accent identification
        st.markdown("**Which accent was it?**")
        accent = st.radio(
            "Select the accent:",
            options=["UK", "US"],
            key="accent_selection",
            horizontal=True
        )
        
        # Check answers
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Check Answer", key="check_challenge"):
                st.session_state.challenge_attempts += 1
                vowel_correct = selected_vowel == current_word["vowel"]
                accent_correct = accent == current_word["accent"]
                
                if vowel_correct and accent_correct:
                    st.session_state.challenge_correct += 1
                    st.success("✅ Perfect! You got both the vowel and accent right!")
                    st.info(random.choice(ENCOURAGEMENTS_CORRECT))
                elif vowel_correct:
                    st.warning("Almost! You got the vowel right but the accent wrong.")
                    st.info(f"The accent was {current_word['accent']} English.")
                elif accent_correct:
                    st.warning("Close! You got the accent right but the vowel wrong.")
                    st.info(f"The vowel sound was {current_word['vowel']}.")
                else:
                    st.error("Not quite right. Try again!")
                    st.warning(random.choice(ENCOURAGEMENTS_WRONG))
                
                st.markdown(f"**Correct answer:** {current_word['vowel']} in {current_word['accent']} English")
        
        with col2:
            if st.button("New Word", key="new_word"):
                st.session_state.current_word = random.choice(word_bank)
                st.rerun()
        
        # Score tracking
        if st.session_state.challenge_attempts > 0:
            accuracy = (st.session_state.challenge_correct / st.session_state.challenge_attempts) * 100
            st.markdown(f"**Score:** {st.session_state.challenge_correct}/{st.session_state.challenge_attempts} ({accuracy:.1f}% accuracy)")
        
        st.session_state.completed_sections.add('listening_challenge')
        update_progress()

# --------------------- Render Function ---------------------
def render():
    # Initialize session state variables
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'completed_sections' not in st.session_state:
        st.session_state.completed_sections = set()

    # --------------------- Section Data ---------------------
    section = {
        "summary": "Aight, let's break it down real simple: Vowels let air flow freely, consonants block it a bit. Your tongue position (front/back, high/low) and what your lips do (rounded/spread/neutral) make each vowel unique. Some sounds are tricky and depend on context in words.",
        "examples": [
            ("bit", "[ɪ]"),
            ("beat", "[iː]"),
            ("bet", "[e]"),
            ("bat", "[æ]"),
            ("cut", "[ʌ]"),
            ("cart", "[ɑː]"),
            ("put", "[ʊ]"),
            ("boot", "[uː]"),
            ("bird", "[ɜː]"),
            ("about", "[ə]")
        ],
        "important_qs": [
            "What's the main difference between short and long vowels?",
            "Why do some vowels sound different in US vs UK English?",
            "How does tongue position affect vowel sounds?",
            "What makes a vowel 'rounded' vs 'spread'?"
        ],
        "important_answers": [
            "Short vowels are quicker and often have a different quality, not just length! Long vowels tend to be more tense and pronounced with more mouth movement.",
            "Accents change how we pronounce vowels - like how 'cart' has a longer [ɑː] in UK English but a shorter [ɑ] in US English. The 'r' sound also changes vowel quality.",
            "Tongue position (front/back, high/low) is everything! High tongue = close vowels like [i], low tongue = open vowels like [a]. Front/back position changes the resonance.",
            "Rounded vowels like [u] and [o] have puckered lips, while spread vowels like [i] and [e] have stretched lips. Neutral vowels like [ə] are somewhere in between."
        ],
        "practice": [
            {"question":"Which is a short vowel?","options":["[iː]","[uː]","[ɪ]","[ɜː]"],"answer":"[ɪ]"},
            {"question":"What's the vowel in 'bird' in UK English?","options":["[ɜː]","[ɝ]","[ʌ]","[ə]"],"answer":"[ɜː]"},
            {"question":"Which vowel is usually rounded?","options":["[i]","[e]","[u]","[æ]"],"answer":"[u]"},
            {"question":"What's the main difference between [ɪ] and [iː]?","options":["Just length","Length and quality","Lip position","Tongue height only"],"answer":"Length and quality"},
            {"question":"Which word has a different vowel sound?","options":["bit","sit","fit","beat"],"answer":"beat"},
            {"question":"What makes [ə] special?","options":["It's always long","It's always stressed","It's the neutral vowel","It's always rounded"],"answer":"It's the neutral vowel"},
            {"question":"Which is a back vowel?","options":["[i]","[e]","[æ]","[u]"],"answer":"[u]"}
        ],
        "recap": "Here's the lowdown: Short vowels are quick, long vowels are longer with different quality. Vowels change based on tongue position (high/low, front/back) and lip shape (rounded/spread/neutral). US and UK English pronounce some vowels differently, especially with 'r' sounds.",
        "farsi": [
            "حروف صدادار کوتاه و بلند داریم. حروف کوتاه مثل [ɪ] در 'bit' و حروف بلند مثل [iː] در 'beat'.",
            "موقعیت زبان (جلو/عقب، بالا/پایین) و حالت لب‌ها (گرد، کشیده، معمولی) کیفیت صدا رو مشخص می‌کنه.",
            "بعضی حروف صدادار در انگلیسی آمریکایی و بریتانیایی متفاوت تلفظ می‌شن، مخصوصاً وقتی حرف 'r' درگیره.",
            "حرف صدادار [ə] خنثی هست و در کلمات بدون تکیه مثل 'about' شنیده میشه."
        ],
        "funfact": "Did you know the longest word in English without a vowel is rhythms?",
        "mindblower": "The word queue is just the letter Q followed by four silent letters.",
        "quicktip": "💡 Try placing your fingers on your throat when making different vowel sounds. You'll feel how some vowels vibrate more in the front or back of your mouth!",
        "eminem_note": "🎤 In 'Lose Yourself', Eminem says 'opportunity' with that classic US rap flow: the 't' sounds like a quick 'd' (oppor-du-nity) and the vowel in the second syllable is a neutral schwa [ə]. In UK English, the 't' would be clearer and the vowel might be more pronounced."
    }

    st.markdown('<div class="main-header">Interactive Phonetics Lab: Short & Long Vowels</div>', unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {st.session_state.progress}%">{int(st.session_state.progress)}% Complete</div>
    </div>
    """, unsafe_allow_html=True)

    # Vowel table
    vowel_table()
    st.session_state.completed_sections.add('vowel_table')
    update_progress()

    # --------------------- Summary ---------------------
    st.markdown('<div class="expandable-title">1. Quick Summary</div>', unsafe_allow_html=True)
    with st.expander("", expanded=True):
        st.markdown(f'<div class="hover-text">{section["summary"]}</div>', unsafe_allow_html=True)
        st.session_state.completed_sections.add('summary')
        update_progress()

    # --------------------- Examples ---------------------
    st.markdown('<div class="expandable-title">2. Examples <span class="tooltip">ℹ️<span class="tooltiptext">Click the audio icons to hear pronunciation examples</span></span></div>', unsafe_allow_html=True)
    with st.expander("", expanded=True):
        for word, ipa in section["examples"]:
            col1, col2, col3, col4 = st.columns([2,2,2,4])
            col1.markdown(f"**{word}**")
            audio_bytes_uk = text_to_speech(word, lang='en-uk')
            audio_bytes_us = text_to_speech(word, lang='en')
            if audio_bytes_uk:
                col2.caption("UK")
                col2.audio(audio_bytes_uk, format='audio/mp3')
            else:
                col2.info("🔇 UK")
            if audio_bytes_us:
                col3.caption("US")
                col3.audio(audio_bytes_us, format='audio/mp3')
            else:
                col3.info("🔇 US")
            col4.markdown(f'<span class="phonetic">{ipa}</span>', unsafe_allow_html=True)
        st.session_state.completed_sections.add('examples')
        update_progress()

    # --------------------- Important Questions ---------------------
    st.markdown('<div class="expandable-title">3. Key Questions</div>', unsafe_allow_html=True)
    if "show_answers" not in st.session_state:
        st.session_state["show_answers"] = [False]*len(section["important_answers"])
    with st.expander("", expanded=False):
        for i, q in enumerate(section["important_qs"]):
            st.markdown(f'<div class="practice-question">Q{i+1}. {q}</div>', unsafe_allow_html=True)
            if st.button(f"Show Answer {i+1}", key=f"answer_{i}"):
                st.session_state["show_answers"][i] = not st.session_state["show_answers"][i]
            if st.session_state["show_answers"][i]:
                st.markdown(f'<div class="lux-btn answer-btn">{section["important_answers"][i]}</div>', unsafe_allow_html=True)
        st.session_state.completed_sections.add('key_questions')
        update_progress()

    # --------------------- Listening Challenge ---------------------
    listening_challenge()

    # --------------------- Practice ---------------------
    st.markdown('<div class="expandable-title">5. Practice Zone</div>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        total_questions = len(section["practice"])

        for idx, p in enumerate(section["practice"], 1):
            init_question_state(idx)

            # Bold, readable question
            st.markdown(f'<div class="practice-question">Q{idx}. {p["question"]}</div>', unsafe_allow_html=True)

            # Radio as green "option cards"
            current = st.session_state.get(f"q{idx}_selected", None)
            options = p["options"]
            if current in options:
                default_index = options.index(current)
            else:
                default_index = None

            radio_kwargs = {
                "label": "",
                "options": options,
                "key": f"radio_{idx}",
                "horizontal": True
            }
            if default_index is not None:
                radio_kwargs["index"] = default_index

            selected = st.radio(**radio_kwargs)

            # Persist selection
            st.session_state[f"q{idx}_selected"] = selected

            cols = st.columns([1,1,1])
            with cols[0]:
                if st.button(f"Check Q{idx}", key=f"check_{idx}"):
                    st.session_state[f"q{idx}_attempts"] += 1
                    is_correct = (st.session_state[f"q{idx}_selected"] == p["answer"])
                    st.session_state[f"q{idx}_is_correct"] = is_correct
                    if is_correct:
                        st.success("✅ Correct!")
                        st.info(random.choice(ENCOURAGEMENTS_CORRECT))
                    else:
                        st.error("❌ Incorrect.")
                        st.warning(random.choice(ENCOURAGEMENTS_WRONG))
                    st.markdown(f"**Explanation:** The correct answer is **{p['answer']}**")

            with cols[1]:
                if st.button(f"Reset Q{idx}", key=f"reset_{idx}"):
                    reset_question(idx)
                    st.rerun()

            # Attempts/status line
            status = st.session_state[f"q{idx}_is_correct"]
            attempts = st.session_state[f"q{idx}_attempts"]
            if status is True:
                st.caption(f"✅ Marked correct in {attempts} attempt(s).")
            elif status is False:
                st.caption(f"❌ Not correct yet. Attempts: {attempts}")
            else:
                st.caption("Select an option and press **Check**.")

            st.markdown("---")

        # Compute score from session_state
        score = sum(1 for i in range(1, total_questions+1) if st.session_state.get(f"q{i}_is_correct") is True)
        st.markdown(f"**Your score: {score}/{total_questions}**")
        if score == total_questions and total_questions > 0:
            st.balloons()

        st.session_state.completed_sections.add('practice')
        update_progress()

    # --------------------- Toggles ---------------------
    if "toggle_states" not in st.session_state:
        st.session_state["toggle_states"] = {"recap":False,"funfact":False,"mindblower":False,"quicktip":False,"eminem":False}

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⚡ Quick Recap", key="recap_btn"):
            st.session_state["toggle_states"]["recap"] = not st.session_state["toggle_states"]["recap"]
    with col2:
        if st.button("🌟 Fun Fact", key="funfact_btn"):
            st.session_state["toggle_states"]["funfact"] = not st.session_state["toggle_states"]["funfact"]
    with col3:
        if st.button("🧠 Mind Blower", key="mindblower_btn"):
            st.session_state["toggle_states"]["mindblower"] = not st.session_state["toggle_states"]["mindblower"]
    with col4:
        if st.button("💡 Quick Tip", key="quicktip_btn"):
            st.session_state["toggle_states"]["quicktip"] = not st.session_state["toggle_states"]["quicktip"]
    with col5:
        if st.button("🎤a lil help from E", key="eminem_btn"):
            st.session_state["toggle_states"]["eminem"] = not st.session_state["toggle_states"]["eminem"]

    if st.session_state["toggle_states"]["recap"]:
        st.markdown(f'<div class="lux-btn recap-btn">{section["recap"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["funfact"]:
        st.markdown(f'<div class="lux-btn funfact-btn">{section["funfact"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["mindblower"]:
        st.markdown(f'<div class="lux-btn mindblower-btn">{section["mindblower"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["quicktip"]:
        st.markdown(f'<div class="lux-btn funfact-btn">{section["quicktip"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["eminem"]:
        st.markdown(f'<div class="lux-btn mindblower-btn">{section["eminem_note"]}</div>', unsafe_allow_html=True)

    # --------------------- Persian Section ---------------------
    st.markdown('<div class="expandable-title">📝 Clarification in Persian</div>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        for line in section["farsi"]:
            st.markdown(f'<div class="farsi-line">{line}</div>', unsafe_allow_html=True)
        st.session_state.completed_sections.add('persian')
        update_progress()

    # --------------------- Feedback Section ---------------------
    st.markdown("---")
    st.markdown("### 💬 Feedback & Suggestions")
    st.caption("Yes — you can receive feedback! Submissions are saved to a CSV file on the server (./data/feedback.csv).")

    os.makedirs("data", exist_ok=True)
    feedback_path = os.path.join("data", "feedback.csv")

    with st.form("feedback_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name (optional)")
        with c2:
            email = st.text_input("Email (optional)")
        rating = st.slider("Overall experience (1 = poor, 5 = excellent)", 1, 5, 4)
        message = st.text_area("Your thoughts or suggestions:")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if not message.strip():
                st.warning("Please write something before submitting.")
            else:
                row = {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "name": name.strip(),
                    "email": email.strip(),
                    "rating": rating,
                    "message": message.strip()
                }
                df_new = pd.DataFrame([row])
                if os.path.exists(feedback_path):
                    df_new.to_csv(feedback_path, mode="a", header=False, index=False, encoding="utf-8")
                else:
                    df_new.to_csv(feedback_path, index=False, encoding="utf-8")
                st.success("Thanks for your feedback! Saved successfully.")

    # Admin utilities
    with st.expander("📥 View / Download received feedback (admin)"):
        if os.path.exists(feedback_path):
            df = pd.read_csv(feedback_path, encoding="utf-8")
            st.dataframe(df, use_container_width=True)
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download all feedback (CSV)", data=csv_bytes, file_name="feedback.csv", mime="text/csv")
        else:
            st.info("No feedback submitted yet.")

# --------------------- Main ---------------------
def show():
    render()
if __name__ == "__main__":
    render()
