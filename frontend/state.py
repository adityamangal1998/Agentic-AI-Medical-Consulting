# state.py
# Handles Streamlit session state initialization and helpers
import streamlit as st

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'audio_response' not in st.session_state:
        st.session_state.audio_response = None
