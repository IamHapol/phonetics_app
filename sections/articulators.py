import streamlit as st
import random
from gtts import gTTS
from io import BytesIO
import time

st.set_page_config(page_title="Articulators App", layout="wide")

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

# --------------------- Text to Speech with Error Handling ---------------------
@st.cache_data(show_spinner=False)
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Text-to-speech service unavailable: {str(e)}")
        return None

# --------------------- Render Function ---------------------
def render():
    # --------------------- Custom CSS ---------------------
    st.markdown("""
    <style>
    /* Section Headings */
    .section-heading { 
        font-size: 1.3rem !important; 
        font-weight: 800 !important; 
        margin-bottom: 0.5rem !important; 
        color: #2c3e50 !important; 
    }

    /* Expandable Title */
    .expandable-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1C39BB;
        margin: 1rem 0 0.5rem 0;
        padding: 0.5rem;
        background-color: #f0f8ff;
        border-radius: 8px;
        border-left: 4px solid #1C39BB;
    }

    /* Hover Text */
    .hover-text { 
        font-weight: 700 !important; 
        color: #34495e !important; 
        transition: all 0.3s ease !important;
    }
    .hover-text:hover { 
        color: #2980b9 !important; 
    }

    /* Phonetic Symbols */
    .phonetic { 
        color: #16a085 !important; 
        font-weight: 700 !important; 
        font-size: 1.1rem !important; 
    }

    /* Farsi Lines */
    .farsi-line { 
        background-color: #007acc !important; 
        color: white !important; 
        padding: 8px 15px !important; 
        border-left: 4px solid #004b8d !important; 
        margin-bottom: 5px !important; 
        border-radius: 6px !important; 
        font-size: 1.1rem !important; 
        font-weight: bold !important; 
        transition: color 0.3s ease !important;
    }
    .farsi-line:hover { 
        color: black !important; 
    }

    /* Universal Button Style */
    .lux-btn { 
        display: inline-block; 
        font-weight: 700 !important; 
        border-radius: 12px !important; 
        padding: 10px 20px !important; 
        border: none !important; 
        color: white !important; 
        margin: 6px 4px !important; 
        transition: all 0.3s ease !important; 
        cursor: pointer; 
        position: relative; 
        overflow: hidden; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .lux-btn:hover { 
        transform: translateY(-3px) !important; 
        box-shadow: 0 8px 14px rgba(0,0,0,0.25) !important; 
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

    /* Specific Colors */
    .answer-btn { background: linear-gradient(90deg, #9b59b6, #8e44ad) !important; }
    .check-btn { background: linear-gradient(90deg, #27ae60, #2ecc71) !important; }
    .recap-btn { background: linear-gradient(90deg, #87ceeb, #ffffff) !important; color:#1e3c72 !important; }
    .funfact-btn { background: linear-gradient(90deg, #fff176, #f1c40f) !important; color:#7d6608 !important; }
    .mindblower-btn { background: linear-gradient(90deg, #8e44ad, #9b59b6) !important; }

    /* Card for Practice Options */
    .option-card { 
        background: linear-gradient(135deg, #6a11cb, #2575fc); 
        color: white !important; 
        font-weight: bold !important;
        padding: 12px 20px; 
        border-radius: 14px; 
        text-align: center; 
        margin: 5px 0; 
        cursor: pointer; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .option-card:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 6px 12px rgba(0,0,0,0.2); 
    }

    /* General App Styling */
    body {
        background: linear-gradient(135deg, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
        transition: background 2s ease-in-out;
    }

    /* Container cards */
    .card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        padding: 25px;
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    }

    /* Section dividers */
    .divider {
        height: 3px;
        border-radius: 2px;
        background: linear-gradient(to right, #7B68EE, #87CEEB, #FFD700, #FF69B4, #32CD32);
        margin: 25px 0;
        box-shadow: 0 0 8px rgba(0,0,0,0.1);
    }

    /* Headings */
    h2, h3 {
        color: #1C39BB; /* Persian blue */
        text-align: center;
        font-weight: 700;
        transition: color 0.3s ease;
    }
    h2:hover, h3:hover {
        color: #4169E1;
    }

    /* Buttons shared - Updated for bold light text */
    .stButton > button {
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 0.7em 1.2em;
        font-size: 1em;
        font-weight: 700 !important;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        background: linear-gradient(90deg, #1C39BB, #4169E1) !important;
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
        box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    }

    /* Fade-in animation for revealed text */
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    /* IPA Table Styling - Black with white text */
    .ipa-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        background-color: black !important;
        color: white !important;
    }
    .ipa-table th, .ipa-table td {
        border: 1px solid white;
        padding: 8px;
        text-align: left;
        color: white !important;
        background-color: black !important;
    }
    .ipa-table th {
        font-weight: bold;
        background-color: #333 !important;
    }
    .ipa-table tr:nth-child(even) {
        background-color: #222 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------- Section Data ---------------------
    section = {
        "summary": "First things first, your lungs push air up, the larynx gives it voice, and then your tongue, lips, teeth, soft/hard palates, and more jump in to shape it. These are your articulators—your speech crew!",
        "examples": [
            ("top", "[tɔp]"),
            ("kick", "[kɪk]"),
            ("bat", "[bæt]"),
            ("fun", "[fʌn]"),
            ("think", "[θɪŋk]"),
            ("go", "[gəʊ]"),
            ("hat", "[hæt]")
        ],
        "important_qs": [
            "Why do we call [k] and [g] 'velars'?",
            "If the velum never lowered, how would nasals change?"
        ],
        "important_answers": [
            "Because they're produced by the back of the tongue contacting the velum.",
            "If velum always stayed raised, nasal sounds wouldn't be possible—they'd all be oral!"
        ],
        "practice": [
            {"question":"Which one is a velar consonant?","options":["[t]","[k]","[m]"],"answer":"[k]"},
            {"question":"Which part separates oral and nasal cavities?","options":["alveolar ridge","pharynx","teeth"],"answer":"pharynx"}
        ],
        "recap": "Your lungs, larynx, and articulators team up to turn air into speech.",
        "farsi": [
            "درود دوستان. این بخش اعضای اصلی تولید صدا را معرفی کرد.",
            "گلو هوا را می‌فرستد، و اجزای مختلف دهان شکلش می‌دهند.",
            "مثلاً [t] با تماس زبان به ridge تولید می‌شود.",
            "یا [k] با تماس زبان به نرم‌کام.",
            "یاد گرفتیم oral و nasal از هم جدا هستند.",
            "بدون بالابردن velum، nasal نمی‌بود."
        ],
        "funfact": "The tongue is the most flexible articulator and can produce sounds at every place of articulation in the mouth!",
        "mindblower": "🤯 Did You Know?\nThe English 'th' sounds (/θ/ and /ð/) are among the rarest sounds in world languages, occurring in only 7% of them!"
    }

    st.title("🗣️ Articulators above the larynx")

    # --------------------- IPA Chart ---------------------
    st.markdown('<div class="expandable-title">📊 IPA Chart (Reference)</div>', unsafe_allow_html=True)
    with st.expander("", expanded=False):
        st.markdown("""
        <table class="ipa-table">
          <tr>
            <th>Place</th>
            <th>Examples</th>
            <th>English Words</th>
          </tr>
          <tr>
            <td>Bilabial</td>
            <td>[p], [b], [m]</td>
            <td><em>pat</em>, <em>bat</em>, <em>mat</em></td>
          </tr>
          <tr>
            <td>Labiodental</td>
            <td>[f], [v]</td>
            <td><em>fan</em>, <em>van</em></td>
          </tr>
          <tr>
            <td>Dental</td>
            <td>[θ], [ð]</td>
            <td><em>think</em>, <em>this</em></td>
          </tr>
          <tr>
            <td>Alveolar</td>
            <td>[t], [d], [s], [z]</td>
            <td><em>top</em>, <em>dog</em>, <em>sun</em>, <em>zoo</em></td>
          </tr>
          <tr>
            <td>Post-alveolar</td>
            <td>[ʃ], [ʒ], [tʃ], [dʒ]</td>
            <td><em>ship</em>, <em>judge</em></td>
          </tr>
          <tr>
            <td>Palatal</td>
            <td>[j]</td>
            <td><em>yes</em></td>
          </tr>
          <tr>
            <td>Velar</td>
            <td>[k], [g], [ŋ]</td>
            <td><em>go</em>, <em>cat</em>, <em>sing</em></td>
          </tr>
          <tr>
            <td>Glottal</td>
            <td>[h], [ʔ]</td>
            <td><em>hat</em>, <em>uh-oh</em></td>
          </tr>
        </table>
        """, unsafe_allow_html=True)

    # --------------------- Summary ---------------------
    st.markdown('<div class="expandable-title">1. Simple Summary</div>', unsafe_allow_html=True)
    with st.expander("", expanded=True):
        st.markdown(f'<div class="hover-text">{section["summary"]}</div>', unsafe_allow_html=True)

    # --------------------- Examples ---------------------
    st.markdown('<div class="expandable-title">2. Examples</div>', unsafe_allow_html=True)
    with st.expander(""):
        for word, ipa in section["examples"]:
            col1, col2, col3 = st.columns([3,3,4])
            col1.markdown(f"**{word}**")
            
            # Try to get audio, but handle if it fails
            audio_bytes = text_to_speech(word)
            if audio_bytes:
                col2.audio(audio_bytes, format='audio/mp3')
            else:
                col2.warning("Audio unavailable")
                
            col3.markdown(f'<span class="phonetic">{ipa}</span>', unsafe_allow_html=True)

    # --------------------- Important Questions ---------------------
    st.markdown('<div class="expandable-title">3. Prof. Badakhshan\'s Questions</div>', unsafe_allow_html=True)
    if "show_answers" not in st.session_state:
        st.session_state["show_answers"] = [False]*len(section["important_answers"])
    with st.expander(""):
        for i, q in enumerate(section["important_qs"]):
            st.markdown(f"**Q{i+1}. {q}**", unsafe_allow_html=True)
            if st.button(f"Show Answer {i+1}", key=f"answer_{i}"):
                st.session_state["show_answers"][i] = not st.session_state["show_answers"][i]
            if st.session_state["show_answers"][i]:
                st.markdown(f'<div class="lux-btn answer-btn">{section["important_answers"][i]}</div>', unsafe_allow_html=True)

    # --------------------- Practice ---------------------
    st.markdown('<div class="expandable-title">4. Practice</div>', unsafe_allow_html=True)
    with st.expander(""):
        for idx, p in enumerate(section["practice"],1):
            st.write(f"**Q{idx}. {p['question']}**")
            if f"selected_{idx}" not in st.session_state:
                st.session_state[f"selected_{idx}"] = None
            cols = st.columns(len(p['options']))
            for i, option in enumerate(p['options']):
                if cols[i].button(option, key=f"opt_{idx}_{i}", help="Select this answer"):
                    st.session_state[f"selected_{idx}"] = option
            if st.session_state[f"selected_{idx}"]:
                selected = st.session_state[f"selected_{idx}"]
                if st.button(f"Check Q{idx}", key=f"check_{idx}"):
                    if selected == p['answer']:
                        st.success("✅ Correct!")
                        st.info(random.choice(ENCOURAGEMENTS_CORRECT))
                    else:
                        st.error("❌ Incorrect.")
                        st.warning(random.choice(ENCOURAGEMENTS_WRONG))

    # --------------------- Toggles ---------------------
    if "toggle_states" not in st.session_state:
        st.session_state["toggle_states"] = {"recap":False,"funfact":False,"mindblower":False}

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚡ Quick Recap", key="recap_btn"):
            st.session_state["toggle_states"]["recap"] = not st.session_state["toggle_states"]["recap"]
    with col2:
        if st.button("🌟 Fun Fact", key="funfact_btn"):
            st.session_state["toggle_states"]["funfact"] = not st.session_state["toggle_states"]["funfact"]

    if st.session_state["toggle_states"]["recap"]:
        st.markdown(f'<div class="lux-btn recap-btn">{section["recap"]}</div>', unsafe_allow_html=True)
    if st.session_state["toggle_states"]["funfact"]:
        st.markdown(f'<div class="lux-btn funfact-btn">{section["funfact"]}</div>', unsafe_allow_html=True)

    # --------------------- Persian Section ---------------------
    st.markdown('<div class="expandable-title">Clarification in Persian</div>', unsafe_allow_html=True)
    with st.expander(""):
        for line in section["farsi"]:
            st.markdown(f'<div class="farsi-line">{line}</div>', unsafe_allow_html=True)

    # --------------------- Mind Blower ---------------------
    if st.button("🧠 Mind Blower", key="mindblower_btn"):
        st.session_state["toggle_states"]["mindblower"] = not st.session_state["toggle_states"]["mindblower"]
    if st.session_state["toggle_states"]["mindblower"]:
        st.markdown(f'<div class="lux-btn mindblower-btn">{section["mindblower"]}</div>', unsafe_allow_html=True)

# --------------------- Main ---------------------
def show():
    render()
if __name__ == "__main__":
    render()