# 🏥 AI Medical Consulting

A full-stack AI-powered medical consulting application with voice interaction, image analysis, and emergency calling capabilities.

## 🌟 Features

### Frontend (Streamlit)
- **Interactive Chat Interface**: Clean, responsive chat bubbles with user/AI distinction
- **Voice Input**: Record voice messages using microphone (via `streamlit-mic-recorder`)
- **Audio Playback**: Listen to AI responses with text-to-speech
- **Medical Image Upload**: Upload and analyze medical scans, X-rays, reports, etc.
- **Emergency Calling**: One-click emergency contact via Twilio integration

### Backend (FastAPI)
- **Intelligent Routing**: Automatically routes queries to appropriate AI models
- **Multi-Modal AI**:
  - **OpenAI GPT-4o-mini** for general conversations
  - **LLaVA 7B (via Ollama)** for medical image analysis and vision tasks
  - **Gemma 7B (via Ollama)** for medical text reasoning and consultation
  - **OpenAI Whisper** for speech-to-text
  - **OpenAI TTS** for text-to-speech
- **Emergency Services**: Twilio integration for emergency calls
- **RESTful API**: Clean, documented endpoints for all functionality

### AI Agent Logic
- **Medical Keywords Detection**: Automatically routes medical queries to Gemma 7B
- **Image Analysis**: Uses LLaVA 7B for medical image interpretation, enhanced with Gemma 7B for medical context
- **Emergency Detection**: Triggers emergency calls when urgent language is detected
- **Fallback Handling**: Graceful degradation when services are unavailable

## 📁 Project Structure

```
project/
├── backend/
│   ├── main.py                 # FastAPI application with all endpoints
│   ├── tools/
│   │   ├── __init__.py        # Package initialization
│   │   ├── medgemma.py        # MedGemma/Ollama integration
│   │   └── twilio_call.py     # Twilio emergency calling
│   └── requirements.txt       # Backend dependencies
├── frontend/
│   └── app.py                 # Streamlit chat interface
├── .env                       # Environment variables (not in repo)
├── .env.example              # Environment variables template
├── requirements.txt          # All project dependencies
└── README.md                # This file
```

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running (for MedGemma)
3. **OpenAI API key**
4. **Twilio account** (for emergency calling)

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd Agentic-AI-Medical-Consulting

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
notepad .env  # Windows
# nano .env   # macOS/Linux
```

Required environment variables:
```env
# OpenAI Configuration
OPENAI_API_KEY="your_openai_api_key_here"

# Ollama Configuration - Dual Model Setup
OLLAMA_BASE_URL="http://localhost:11434"
MEDGEMMA_MODEL="gemma:7b"          # Medical text analysis
LLAVA_MODEL="llava:7b"             # Image analysis

# Twilio Configuration
TWILIO_ACCOUNT_SID="your_twilio_account_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_FROM_NUMBER="+1234567890"  # your Twilio number
EMERGENCY_CONTACT="+1234567890"   # emergency contact number
```

### 3. Setup Ollama Models

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull required models
ollama pull llava:7b      # For image analysis
ollama pull gemma:7b      # For medical text analysis

# Verify installation
ollama list
```

### 4. Setup Twilio (Optional)

1. Create a [Twilio account](https://www.twilio.com/try-twilio)
2. Get a Twilio phone number
3. Find your Account SID and Auth Token in the Twilio Console
4. Update the `.env` file with your Twilio credentials

## 🏃‍♂️ Running the Application

### Start Backend (Terminal 1)
```bash
# Navigate to backend directory
cd backend

# Start FastAPI server (uvicorn now built-in)
python main.py
```

**Alternative methods:**
```bash
# Using uvicorn directly (if preferred)
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Using the launcher script
python run_server.py
```

The backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)
```bash
# Navigate to frontend directory
cd frontend

# Start Streamlit app
streamlit run app.py
```

The frontend will be available at: `http://localhost:8501`

## 🔧 API Endpoints

### Backend Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/chat` | POST | Main chat endpoint with AI routing |
| `/voice` | POST | Speech-to-text transcription |
| `/tts` | POST | Text-to-speech conversion |
| `/emergency-call` | POST | Trigger emergency call |

### Example API Usage

```python
import requests

# Chat with AI
response = requests.post("http://localhost:8000/chat", json={
    "message": "I have a headache and fever",
    "has_image": False
})

# Upload and analyze medical image
with open("xray.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()
    
response = requests.post("http://localhost:8000/chat", json={
    "message": "Please analyze this X-ray",
    "has_image": True,
    "image_data": image_data
})
```

## 🤖 AI Model Routing

The system intelligently routes queries based on content:

### LLaVA 7B (Medical Image Analysis)
- **Triggers**: Any uploaded image (medical scans, reports, etc.)
- **Capabilities**: Advanced vision analysis, medical image interpretation
- **Enhanced**: Combined with Gemma 7B for medical context

### Gemma 7B (Medical Text Analysis)
- **Triggers**: Medical keywords (symptom, pain, scan, diagnosis, etc.)
- **Capabilities**: Medical reasoning, symptom analysis, treatment suggestions
- **Model**: Runs locally via Ollama

### OpenAI GPT-4o-mini (General AI)
- **Triggers**: General conversations, non-medical queries
- **Capabilities**: General knowledge, casual conversation
- **Model**: OpenAI API

### Emergency System
- **Triggers**: Keywords like "emergency", "call doctor", "help", "urgent"
- **Action**: Automatically places call via Twilio with pre-recorded message

## 🔒 Security Considerations

- **Environment Variables**: Keep `.env` file secure and never commit to version control
- **API Keys**: Rotate API keys regularly
- **CORS**: Configure CORS properly for production deployment
- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Consider implementing rate limiting for production

## 🚨 Emergency Features

### Automatic Emergency Detection
The system monitors chat messages for emergency keywords and can:
1. Automatically trigger emergency calls
2. Send pre-configured messages to emergency contacts
3. Provide immediate response with emergency guidance

### Manual Emergency Trigger
Users can manually trigger emergency calls via:
- Emergency button in chat interface
- Typing "emergency" in chat
- Using the dedicated emergency form submission

## 🛠️ Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   ollama list
   
   # Start Ollama service
   ollama serve
   ```

2. **OpenAI API Errors**
   - Verify API key is correct in `.env`
   - Check API quota and billing status

3. **Twilio Call Failures**
   - Verify phone numbers are in E.164 format (+1234567890)
   - Check Twilio account balance
   - Ensure from number is verified

4. **Frontend Connection Issues**
   - Ensure backend is running on port 8000
   - Check CORS configuration
   - Verify network connectivity

### Logs and Debugging

```bash
# Backend logs
uvicorn main:app --reload --log-level debug

# Check Ollama logs
ollama logs

# Streamlit logs
streamlit run app.py --logger.level debug
```

## 📝 Development

### Adding New Features

1. **New AI Models**: Add integration in `backend/tools/`
2. **New Endpoints**: Extend `backend/main.py`
3. **Frontend Components**: Modify `frontend/app.py`
4. **Routing Logic**: Update keyword detection in `backend/main.py`

### Testing

```bash
# Test backend endpoints
python -m pytest backend/tests/

# Test Twilio integration
python backend/tools/twilio_call.py

# Test MedGemma connection
python backend/tools/medgemma.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support, please:
1. Check this README and troubleshooting section
2. Review the API documentation at `http://localhost:8000/docs`
3. Open an issue on GitHub

---

**⚠️ Medical Disclaimer**: This application is for educational and informational purposes only. Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment. Do not use this application for emergency medical situations - call your local emergency services directly.
