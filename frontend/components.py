# components.py
# UI components for Streamlit app
import streamlit as st

def display_chat_message(message, is_user=False):
    """Display a chat message with styling"""
    avatar = "👤" if is_user else "🤖"
    with st.container():
        col1, col2 = st.columns([1, 10])
        with col1:
            st.markdown(f"<div style='text-align: center; font-size: 24px; padding: 10px;'>{avatar}</div>", unsafe_allow_html=True)
        with col2:
            if is_user:
                st.markdown(f"""
                <div style=\"background-color: #007bff; \
                            color: white; \
                            padding: 10px 15px; \
                            border-radius: 15px; \
                            margin: 5px 0;\
                            max-width: 80%;\">
                    {message}
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.container():
                    st.markdown(f"""
                    <div style=\"background-color: #f1f3f4; \
                                padding: 15px; \
                                border-radius: 15px; \
                                margin: 5px 0;\
                                max-width: 95%;\">
                    """, unsafe_allow_html=True)
                    st.markdown(message)
                    st.markdown("</div>", unsafe_allow_html=True)
