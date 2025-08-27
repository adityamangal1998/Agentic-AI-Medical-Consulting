# ui.py
# UI layout and widget components
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from components import display_chat_message
from api import trigger_emergency_call, transcribe_audio
from ui_handlers import process_message
def render_sidebar():
    """Render the sidebar with all controls"""
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Emergency section
        render_emergency_section()
        
        # Image upload section
        uploaded_file = render_image_upload_section()
        
        # Voice input section
        render_voice_input_section()
        
        # Settings section
        render_settings_section()
        
    return uploaded_file

def render_emergency_section():
    """Render emergency call section"""
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

def render_image_upload_section():
    """Render image upload section"""
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
    
    return uploaded_file

def render_voice_input_section():
    """Render voice input section"""
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
                    process_message(transcription)
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_settings_section():
    """Render settings section"""
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.markdown("**⚙️ Settings**")
    auto_tts = st.checkbox("Auto-play AI responses", value=False)
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.audio_response = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    return auto_tts

def render_chat_area():
    """Render the main chat area"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        render_chat_history()
        
        # Chat input form
        render_chat_input_form()
    
    with col2:
        # Audio playback area
        render_audio_playback()

def render_chat_history():
    """Render chat history"""
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            display_chat_message(chat["message"], chat.get("is_user", False))
            
            # Show source indicator for AI responses
            if not chat.get("is_user", False) and "source" in chat:
                render_source_caption(chat["source"])

def render_source_caption(source):
    """Render source caption for AI responses"""
    if source == "medgemma":
        st.caption("🧬 Powered by Gemma 7B (Medical Text Analysis)")
    elif source == "llava+medgemma":
        st.caption("👁️ Powered by LLaVA 7B + Gemma 7B (Image + Medical Analysis)")
    elif source == "openai":
        st.caption("🤖 Powered by OpenAI GPT-4o-mini")
    elif source == "emergency":
        st.caption("🚨 Emergency System")

def render_chat_input_form():
    """Render chat input form"""
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

def render_audio_playback():
    """Render audio playback area"""
    if st.session_state.audio_response:
        st.markdown("**🔊 AI Response Audio**")
        st.audio(st.session_state.audio_response, format="audio/mp3")
        
        if st.button("Clear Audio"):
            st.session_state.audio_response = None
            st.rerun()
