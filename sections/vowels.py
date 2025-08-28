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
        color: white !important;
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
    .mindblower-btn { background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%) !important; }

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
    # Removed the "Click to show/hide" expander title — just show the content.
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
    total_sections = 6  # Summary, Examples, Key Questions, Practice, Persian, Vowel Table
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
    # also reset radio widget value
    st.session_state.pop(f"radio_{qidx}", None)

# --------------------- Render Function ---------------------
def render():
    # Initialize session state variables
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'completed_sections' not in st.session_state:
        st.session_state.completed_sections = set()

    # --------------------- Section Data ---------------------
    section = {
        # "Alright" -> "Aight"
        "summary": "Aight, let's break it down real simple: Vowels let air flow freely, consonants block it a bit. Your tongue position (front/back, high/low) and what your lips do (rounded/spread/neutral) make each vowel unique. Some sounds are tricky and depend on context in words.",
        "examples": [
            ("see", "[i:]"),
            ("cat", "[æ]"),
            ("calm", "[a:]"),
            ("too", "[u:]"),
            ("ship", "[ɪ]"),
            ("book", "[ʊ]"),
            ("father", "[ɑ:]"),
            ("bird", "[ɜ:]")
        ],
        "important_qs": [
            "Production view: what separates vowels from consonants?",
            "Why is the border fuzzy for sounds like [j] and [w]?",
            "What's an English distribution test that splits vowels vs consonants?",
            "Name the three big articulatory dimensions of vowel quality."
        ],
        "important_answers": [
            "Vowels have no constriction—air flows free; consonants involve some blockage or narrowing.",
            "Because they're like the in-betweeners: minimal constriction like vowels but often act like consonants in word structure.",
            "Word-initial h + vowel is common (like 'hen'), but h + consonant is rare; after b, consonants follow easily (bid, bill) but a bare vowel doesn't.",
            "Tongue height (close/open), tongue position (front/back), and lip posture (rounded/spread/neutral)."
        ],
        "practice": [
            {"question":"Which one is a vowel (production-wise)?","options":["[s]","[d]","the vowel in 'see' [iː]"],"answer":"the vowel in 'see' [iː]"},
            {"question":"Which start is typical in English words?","options":["h + vowel (e.g., 'hen')","h + consonant (e.g., 'hdo')","both equally common"],"answer":"h + vowel (e.g., 'hen')"},
            {"question":"Pick the back vowel:","options":["[iː] (see)","[æ] (cat)","[uː] (too)"],"answer":"[uː] (too)"},
            {"question":"Which is usually rounded?","options":["[u]","[i]","neutral 'er' sound"],"answer":"[u]"},
            {"question":"What's the main difference between vowels and consonants?","options":["Vowels have constriction, consonants don't","Consonants have constriction, vowels don't","They're the same thing"],"answer":"Consonants have constriction, vowels don't"},
            {"question":"How does tongue height affect vowels?","options":["It doesn't affect them","High tongue = close vowel, Low tongue = open vowel","It changes the lip position"],"answer":"High tongue = close vowel, Low tongue = open vowel"},
            {"question":"Name the three lip positions for vowels.","options":["Up, down, middle","Rounded, spread, neutral","Left, right, center"],"answer":"Rounded, spread, neutral"}
        ],
        "recap": "Here's the lowdown: Vowels = open airflow, consonants = some blockage. English also splits them by where they can appear. Vowel quality depends on three things: height, front/back, and lip posture. Easy peasy!",
        "farsi": [
            "حروف صدادار هوا رو آزادانه رد می‌کنن، حروف بی‌صدا یه کم راه رو می‌بندن.",
            "موقعیت زبان (جلو/عقب، بالا/پایین) مشخص می‌کنه چه صدایی تولید میشه.",
            "حالت لب‌ها هم مهمه: می‌تونه گرد، کشیده یا معمولی باشه.",
            "بعضی صداها بستگی به کلمه دارن که چطور تلفظ میشن."
        ],
        "funfact": "Your tongue is a total acrobat! It can hit every spot in your mouth to make different sounds. The average person produces about 15 different vowel sounds in their language!",
        "mindblower": "🤯 Some languages have sounds that don't even exist in others! The !Xóõ language in Botswana has over 100 distinct sounds, including clicks that English speakers can't easily produce!",
        "quicktip": "💡 Try placing your fingers on your throat when making different sounds. You'll feel the vibration for voiced sounds like [z] vs. the lack of vibration for voiceless sounds like [s]!"
    }

    st.markdown('<div class="main-header">Interactive Phonetics Lab</div>', unsafe_allow_html=True)

    # Progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {st.session_state.progress}%">{int(st.session_state.progress)}% Complete</div>
    </div>
    """, unsafe_allow_html=True)

    # Vowel table (no expander label)
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
            col1, col2, col3 = st.columns([3,3,4])
            col1.markdown(f"**{word}**")
            audio_bytes = text_to_speech(word)
            if audio_bytes:
                col2.audio(audio_bytes, format='audio/mp3')
            else:
                col2.info("🔇 Audio preview")
            col3.markdown(f'<span class="phonetic">{ipa}</span>', unsafe_allow_html=True)
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

    # --------------------- Practice (fixed logic) ---------------------
    st.markdown('<div class="expandable-title">4. Practice Zone</div>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        total_questions = len(section["practice"])

        for idx, p in enumerate(section["practice"], 1):
            init_question_state(idx)

            # Bold, readable question
            st.markdown(f'<div class="practice-question">Q{idx}. {p["question"]}</div>', unsafe_allow_html=True)

            # Radio as green "option cards"
            current = st.session_state.get(f"q{idx}_selected", None)
            # set default index based on current
            options = p["options"]
            if current in options:
                default_index = options.index(current)
            else:
                default_index = None

            selected = st.radio(
                label="",
                options=options,
                index=default_index if default_index is not None else 0 if current is not None else None,
                key=f"radio_{idx}",
                horizontal=True
            )

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

        # Compute score from session_state (persistent & accurate)
        score = sum(1 for i in range(1, total_questions+1) if st.session_state.get(f"q{i}_is_correct") is True)
        st.markdown(f"**Your score: {score}/{total_questions}**")
        if score == total_questions and total_questions > 0:
            st.balloons()

        st.session_state.completed_sections.add('practice')
        update_progress()

    # --------------------- Toggles ---------------------
    if "toggle_states" not in st.session_state:
        st.session_state["toggle_states"] = {"recap":False,"funfact":False,"mindblower":False,"quicktip":False}

    col1, col2, col3, col4 = st.columns(4)
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

    if st.session_state["toggle_states"]["recap"]:
        st.markdown(f'<div class="lux-btn recap-btn">{section["recap"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["funfact"]:
        st.markdown(f'<div class="lux-btn funfact-btn">{section["funfact"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["mindblower"]:
        st.markdown(f'<div class="lux-btn mindblower-btn">{section["mindblower"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["quicktip"]:
        st.markdown(f'<div class="lux-btn funfact-btn">{section["quicktip"]}</div>', unsafe_allow_html=True)

    # --------------------- Persian Section ---------------------
    st.markdown('<div class="expandable-title">📝 Clarification in Persian</div>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        for line in section["farsi"]:
            st.markdown(f'<div class="farsi-line">{line}</div>', unsafe_allow_html=True)
        st.session_state.completed_sections.add('persian')
        update_progress()

    # --------------------- Feedback Section (Saves to CSV) ---------------------
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
