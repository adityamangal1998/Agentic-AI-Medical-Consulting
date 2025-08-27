# ui_handlers.py
# Event handlers and business logic for UI interactions
import streamlit as st
from PIL import Image
import io
import base64
from api import send_chat_request, get_tts_audio

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
    with st.spinner("🤖 AI is analyzing your medical question... This may take up to 60 seconds."):
        response = send_chat_request(message, image_data)
        
        if response:
            ai_message = response["response"]
            source = response.get("source", "unknown")
            
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
        else:
            # Add error message to chat if no response received
            st.session_state.chat_history.append({
                "message": "Sorry, I couldn't process your request. Please try again or contact a healthcare professional if this is urgent.",
                "is_user": False,
                "source": "error"
            })
