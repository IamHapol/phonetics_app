# utils/css.py
import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    /* Main container background */
    .main {
        background: linear-gradient(135deg, #eef1f5 0%, #e3e7ee 100%);
    }

    /* App-level background */
    .stApp {
        background: linear-gradient(135deg, #f2f4f8 0%, #e6e9ef 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2b2f38;
    }

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

    /* Buttons */
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
    .mindblower-btn { background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%) !important; color: black !important; }
    .help-from-e-btn { background: linear-gradient(135deg, #FFD700 0%, #FFC200 100%) !important; color: black !important; }

    /* Card container */
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

    </style>
    """, unsafe_allow_html=True)
