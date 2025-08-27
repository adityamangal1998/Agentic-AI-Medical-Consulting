# api.py
# Handles all backend API calls
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

def send_chat_request(message, image_data=None):
    try:
        payload = {
            "message": message,
            "has_image": image_data is not None,
            "image_data": image_data
        }
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.post(f"{API_BASE_URL}/chat", json=payload, headers=headers, timeout=75)
        if response.status_code == 403:
            st.error("❌ Access denied. Please check if the backend is running on http://localhost:8000")
            return None
        elif response.status_code == 404:
            st.error("❌ Backend not found. Please start the backend server.")
            return None
        elif response.status_code != 200:
            st.error(f"❌ Backend error: {response.status_code} - {response.text}")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Please ensure it's running at http://localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out after 75 seconds. The AI agent is processing your request, please try again or simplify your question.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def transcribe_audio(audio_bytes):
    try:
        files = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}
        response = requests.post(f"{API_BASE_URL}/voice", files=files, timeout=45)
        if response.status_code == 403:
            st.error("❌ Access denied for voice transcription")
            return None
        elif response.status_code != 200:
            st.error(f"❌ Transcription error: {response.status_code}")
            return None
        response.raise_for_status()
        return response.json()["text"]
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend for transcription")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error transcribing audio: {e}")
        return None

def get_tts_audio(text):
    try:
        payload = {"text": text}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/tts", json=payload, headers=headers, timeout=45)
        if response.status_code == 403:
            st.error("❌ Access denied for text-to-speech")
            return None
        elif response.status_code != 200:
            st.error(f"❌ TTS error: {response.status_code}")
            return None
        response.raise_for_status()
        return response.content
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend for TTS")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error generating audio: {e}")
        return None

def trigger_emergency_call(message=None):
    try:
        payload = {"message": message} if message else {}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/emergency-call", json=payload, headers=headers, timeout=30)
        if response.status_code == 403:
            st.error("❌ Access denied for emergency call")
            return None
        elif response.status_code != 200:
            st.error(f"❌ Emergency call error: {response.status_code}")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend for emergency call")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error making emergency call: {e}")
        return None

def check_backend_status():
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=3)
        return response.status_code == 200
    except:
        return False
