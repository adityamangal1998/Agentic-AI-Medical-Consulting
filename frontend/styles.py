# styles.py
# Contains the custom CSS for Streamlit dark theme and UI tweaks

CUSTOM_CSS = '''
<style>
    /* Force dark theme styles */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
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
    .stFileUploader > div {
        background-color: #262730 !important;
        border: 2px dashed #464954 !important;
        border-radius: 10px !important;
    }
    .stFileUploader label {
        color: #fafafa !important;
    }
    .stButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    .stButton > button:hover {
        background-color: #464954 !important;
        border-color: #70798a !important;
    }
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
    .emergency-button {
        background-color: #ef4444 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
    }
    .sidebar-info {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #374151;
    }
    .css-1d391kg {
        background-color: #0e1117 !important;
    }
    .css-18e3th9 {
        background-color: #0e1117 !important;
    }
    .css-10trblm {
        color: #fafafa !important;
    }
    .css-1xarl3l {
        background-color: #262730 !important;
        border: 1px solid #464954 !important;
    }
    .stCheckbox > label {
        color: #fafafa !important;
    }
    .stDownloadButton > button {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    .stAlert {
        background-color: #262730 !important;
        color: #fafafa !important;
        border: 1px solid #464954 !important;
    }
    .stCode {
        background-color: #1e1e1e !important;
        color: #fafafa !important;
    }
    .stDataFrame {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    .stMarkdown {
        color: #fafafa !important;
    }
    .streamlit-expanderHeader {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    .streamlit-expanderContent {
        background-color: #262730 !important;
        border: 1px solid #464954 !important;
    }
</style>
'''
