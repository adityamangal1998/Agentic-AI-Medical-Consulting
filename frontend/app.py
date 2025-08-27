import streamlit as st
from styles import CUSTOM_CSS
from state import initialize_session_state
from api import check_backend_status
from ui import render_sidebar, render_chat_area

def setup_page():
    """Configure Streamlit page settings and styling"""
    st.set_page_config(
        page_title="AI Medical Consulting",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Inject custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def show_header():
    """Display application header"""
    st.title("🏥 AI Medical Consulting")
    st.markdown("Get medical insights powered by AI. *Always consult healthcare professionals for proper diagnosis.*")

def check_backend_connection():
    """Check backend status and show appropriate message"""
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

def main():
    """Main application function"""
    # Setup
    setup_page()
    initialize_session_state()
    
    # Header
    show_header()
    
    # Check backend connection
    check_backend_connection()
    
    # Render UI components
    uploaded_file = render_sidebar()
    render_chat_area()

if __name__ == "__main__":
    main()
