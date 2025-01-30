import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        .stNumberInput > div > div > input {
            font-size: 1.5rem;
            height: 3rem;
        }
        .stats-container {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        h1 {
            color: #2c3e50;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
