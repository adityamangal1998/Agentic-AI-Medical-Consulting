"""
Streamlit Frontend for AI Medical Consulting
Features: Chat interface, voice input, audio playback, image upload
"""

import streamlit as st
import requests
import base64
import io
from PIL import Image
import tempfile
import os
from streamlit_mic_recorder import mic_recorder

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration with dark theme
st.set_page_config(
    page_title="AI Medical Consulting",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme compatibility
st.markdown("""
<style>
    /* Force dark theme styles */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Fix white input boxes for dark theme */
    .stTextInput > div > div > input {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #262730 !important;
        border: 2px dashed #464954 !important;
        border-radius: 10px !important;
    }
    
    .stFileUploader label {
        color: #fafafa !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    .stButton > button:hover {
        background-color: #464954 !important;
        border-color: #70798a !important;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #1e3a8a;
        flex-direction: row-reverse;
    }
    .chat-message.bot {
        background-color: #374151;
    }
    .chat-message .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 1rem;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .chat-message .message {
        flex-grow: 1;
        padding: 0 1rem;
        color: #fafafa;
    }
    
    /* Emergency button */
    .emergency-button {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }
    
    /* Sidebar styling */
    .sidebar-info {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #374151;
    }
    
    /* Fix sidebar background */
    .css-1d391kg {
        background-color: #0e1117 !important;
    }
    
    /* Fix main content area */
    .css-18e3th9 {
        background-color: #0e1117 !important;
    }
    
    /* Fix headers and text */
    .css-10trblm {
        color: #fafafa !important;
    }
    
    /* Fix metric containers */
    .css-1xarl3l {
        background-color: #262730 !important;
        border: 1px solid #464954 !important;
    }
    
    /* Fix checkbox and radio button containers */
    .stCheckbox > label {
        color: #fafafa !important;
    }
    
    /* Fix download button */
    .stDownloadButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    /* Fix success/error/warning messages */
    .stAlert {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    
    /* Fix code blocks */
    .stCode {
        background-color: #1e1e1e !important;
        color: #fafafa !important;
    }
    
    /* Fix table styling */
    .stDataFrame {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    
    /* Ensure all text is visible */
    .stMarkdown {
        color: #fafafa !important;
    }
    
    /* Fix expander styling */
    .streamlit-expanderHeader {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    
    .streamlit-expanderContent {
        background-color: #262730 !important;
        border: 1px solid #464954 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None
    if 'audio_response' not in st.session_state:
        st.session_state.audio_response = None

def display_chat_message(message, is_user=False):
    """Display a chat message with styling"""
    role = "user" if is_user else "bot"
    avatar = "👤" if is_user else "🤖"
    
    with st.container():
        st.markdown(f"""
        <div class="chat-message {role}">
            <div class="avatar">{avatar}</div>
            <div class="message">{message}</div>
        </div>
        """, unsafe_allow_html=True)

def send_chat_request(message, image_data=None):
    """Send chat request to backend"""
    try:
        payload = {
            "message": message,
            "has_image": image_data is not None,
            "image_data": image_data
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat", 
            json=payload, 
            headers=headers,
            timeout=30
        )
        
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
        st.error("❌ Request timed out. The backend may be overloaded.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None

def transcribe_audio(audio_bytes):
    """Send audio to backend for transcription"""
    try:
        files = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}
        response = requests.post(f"{API_BASE_URL}/voice", files=files, timeout=30)
        
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
    """Get TTS audio from backend"""
    try:
        payload = {"text": text}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{API_BASE_URL}/tts", json=payload, headers=headers, timeout=30)
        
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
    """Trigger emergency call via backend"""
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
    """Check if backend is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("🏥 AI Medical Consulting")
    st.markdown("Get medical insights powered by AI. *Always consult healthcare professionals for proper diagnosis.*")
    
    # Check backend connection
    if not check_backend_status():
        st.error("❌ **Backend Connection Failed**")
        st.markdown("""
        **Please ensure the backend is running:**
        1. Open a terminal and navigate to the backend folder
        2. Run: `python main.py`
        3. The backend should be accessible at http://localhost:8000
        """)
        st.stop()
    else:
        st.success("✅ Backend connected successfully")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Emergency call button
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("**🚨 Emergency**")
        if st.button("Call Emergency Contact", key="emergency_btn", help="Trigger emergency call via Twilio"):
            with st.spinner("Making emergency call..."):
                result = trigger_emergency_call()
                if result:
                    st.success("Emergency call initiated!")
                    st.session_state.chat_history.append({
                        "message": "Emergency call was initiated successfully.",
                        "is_user": False,
                        "source": "emergency"
                    })
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Image upload
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("**📸 Medical Image**")
        uploaded_file = st.file_uploader(
            "Upload medical scan/report",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            help="Upload X-rays, MRI scans, lab reports, etc."
        )
        
        if uploaded_file:
            st.session_state.uploaded_image = uploaded_file
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("Image ready for analysis!")
        
        if st.button("Clear Image"):
            st.session_state.uploaded_image = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Voice input
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("**🎤 Voice Input**")
        audio_data = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            use_container_width=True,
            key="mic_recorder"
        )
        
        if audio_data:
            st.audio(audio_data['bytes'], format="audio/wav")
            if st.button("Send Voice Message"):
                with st.spinner("Transcribing..."):
                    transcription = transcribe_audio(audio_data['bytes'])
                    if transcription:
                        st.session_state.chat_history.append({
                            "message": f"🎤 {transcription}",
                            "is_user": True
                        })
                        # Process the transcribed message
                        process_message(transcription)
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Settings
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.markdown("**⚙️ Settings**")
        auto_tts = st.checkbox("Auto-play AI responses", value=False)
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.audio_response = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for chat in st.session_state.chat_history:
                display_chat_message(chat["message"], chat.get("is_user", False))
                
                # Show source indicator for AI responses
                if not chat.get("is_user", False) and "source" in chat:
                    source = chat["source"]
                    if source == "medgemma":
                        st.caption("🧬 Powered by Gemma 7B (Medical Text Analysis)")
                    elif source == "llava+medgemma":
                        st.caption("👁️ Powered by LLaVA 7B + Gemma 7B (Image + Medical Analysis)")
                    elif source == "openai":
                        st.caption("🤖 Powered by OpenAI GPT-4o-mini")
                    elif source == "emergency":
                        st.caption("🚨 Emergency System")
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Type your message...",
                height=100,
                placeholder="Ask about symptoms, upload medical images, or type 'emergency' for urgent help",
                key="chat_input"
            )
            
            col_send, col_emergency = st.columns([3, 1])
            with col_send:
                submit_button = st.form_submit_button("Send Message", use_container_width=True)
            with col_emergency:
                emergency_button = st.form_submit_button("🚨 Emergency", use_container_width=True)
            
            if submit_button and user_input:
                process_message(user_input)
                st.rerun()
                
            if emergency_button:
                emergency_msg = user_input if user_input else "Emergency medical assistance needed"
                with st.spinner("Making emergency call..."):
                    result = trigger_emergency_call(emergency_msg)
                    if result:
                        st.session_state.chat_history.append({
                            "message": f"🚨 Emergency call initiated: {emergency_msg}",
                            "is_user": True
                        })
                        st.session_state.chat_history.append({
                            "message": "Emergency call was successfully initiated. Help is on the way!",
                            "is_user": False,
                            "source": "emergency"
                        })
                        st.rerun()
    
    with col2:
        # Audio playback area
        if st.session_state.audio_response:
            st.markdown("**🔊 AI Response Audio**")
            st.audio(st.session_state.audio_response, format="audio/mp3")
            
            if st.button("Clear Audio"):
                st.session_state.audio_response = None
                st.rerun()

def process_message(message):
    """Process user message and get AI response"""
    # Add user message to chat history
    st.session_state.chat_history.append({
        "message": message,
        "is_user": True
    })
    
    # Prepare image data if available
    image_data = None
    if st.session_state.uploaded_image:
        image = Image.open(st.session_state.uploaded_image)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode()
    
    # Get AI response
    with st.spinner("Getting AI response..."):
        response = send_chat_request(message, image_data)
        
        if response:
            ai_message = response["response"]
            source = response["source"]
            
            # Add AI response to chat history
            st.session_state.chat_history.append({
                "message": ai_message,
                "is_user": False,
                "source": source
            })
            
            # Generate TTS audio for AI response
            audio_data = get_tts_audio(ai_message)
            if audio_data:
                st.session_state.audio_response = audio_data

if __name__ == "__main__":
    main()
