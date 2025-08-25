# 🏥 Agentic AI Medical Consulting System - Complete Flow Diagram

## 🗂️ **System Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🏥 AGENTIC AI MEDICAL CONSULTING SYSTEM                  │
│                                Version 2.0.0                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

🌐 FRONTEND LAYER (Streamlit - Port 8501)
┌─────────────────────────────────────────────────────────────────────────────────┐
│  👤 USER INTERFACE (Dark Theme)                                                │
│  ┌─────────────────┬─────────────────┬─────────────────┬─────────────────────┐  │
│  │   💬 Chat       │   🖼️ Image     │   🎤 Voice      │   🚨 Emergency      │  │
│  │   Interface     │   Upload        │   Input         │   Button            │  │
│  │                 │                 │                 │                     │  │
│  │ • Text input    │ • Prescription  │ • Mic recorder  │ • Instant Twilio    │  │
│  │ • Chat history  │ • Medical scans │ • Audio upload  │ • Emergency call    │  │
│  │ • Auto-play AI  │ • Drag & drop   │ • TTS playback  │ • Critical alerts   │  │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────────┘  │
│                                    ⬇️                                          │
│                            HTTP POST /chat                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ⬇️
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🔗 API GATEWAY LAYER (FastAPI - Port 8000)                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                    🌐 FASTAPI SERVER                                    │  │
│  │  Endpoints:                                                             │  │
│  │  • POST /chat          - Main agentic AI endpoint                      │  │
│  │  • POST /emergency     - Direct emergency calls                        │  │
│  │  • POST /voice         - Voice transcription                           │  │
│  │  • POST /tts           - Text-to-speech                                │  │
│  │  • GET /docs           - API documentation                             │  │
│  │                                                                         │  │
│  │  🛡️ Middleware: CORS, Request logging, Error handling                  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                    ⬇️                                          │
│                       Process medical query with image data                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ⬇️
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🤖 AGENTIC AI ORCHESTRATION LAYER                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                   🧠 MAIN AGENT (agent.py)                             │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │  │
│  │  │  🎯 OPENAI GPT-4O-MINI ORCHESTRATOR                              │  │  │
│  │  │  • Model: gpt-4o-mini                                             │  │  │
│  │  │  • Temperature: 0.2 (consistent responses)                        │  │  │
│  │  │  • Max iterations: 10                                             │  │  │
│  │  │  • Timeout: 60 seconds                                            │  │  │
│  │  │  • Pattern: ReAct (Reasoning + Acting)                            │  │  │
│  │  └───────────────────────────────────────────────────────────────────┘  │  │
│  │                                ⬇️                                          │  │
│  │  📋 INTELLIGENT TOOL SELECTION & REASONING                                 │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐      │  │
│  │  │  Decision Logic:                                                │      │  │
│  │  │  • Image uploaded? → analyze_medical_image                      │      │  │
│  │  │  • Emergency keywords? → emergency_call_tool                   │      │  │
│  │  │  • Location needed? → find_nearby_specialists_by_location       │      │  │
│  │  │  • Medication info? → get_medication_information                │      │  │
│  │  │  • Voice message? → transcribe_voice_message                    │      │  │
│  │  │  • General medical? → ask_medical_specialist                    │      │  │
│  │  │  • Appointment help? → schedule_appointment_helper              │      │  │
│  │  └─────────────────────────────────────────────────────────────────┘      │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ⬇️
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🛠️ SPECIALIZED TOOLS LAYER (langchain_tools.py)                              │
│                                                                                 │
│  ┌─────────────────┬─────────────────┬─────────────────┬─────────────────────┐  │
│  │ 🏥 MEDICAL      │ 🖼️ IMAGE       │ 🚨 EMERGENCY   │ 📍 LOCATION         │  │
│  │ SPECIALIST      │ ANALYSIS        │ CALL            │ FINDER              │  │
│  │                 │                 │                 │                     │  │
│  │ • MedGemma 7B   │ • LLaVA 7B     │ • Twilio API    │ • Geolocation       │  │
│  │ • Medical Q&A   │ • Prescription  │ • Voice calls   │ • Specialist search │  │
│  │ • Symptom help  │ • X-ray analysis│ • SMS alerts    │ • Hospital finder   │  │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────────┘  │
│                                                                                 │
│  ┌─────────────────┬─────────────────┬─────────────────┬─────────────────────┐  │
│  │ 💊 MEDICATION   │ 🎤 VOICE        │ 📅 APPOINTMENT  │ 🔧 SYSTEM           │  │
│  │ INFORMATION     │ TRANSCRIPTION   │ HELPER          │ UTILITIES           │  │
│  │                 │                 │                 │                     │  │
│  │ • Drug database │ • Whisper API   │ • Scheduling    │ • Error handling    │  │
│  │ • Interactions  │ • Audio to text │ • Availability  │ • Logging system    │  │
│  │ • Dosage info   │ • Multi-format  │ • Reminders     │ • Async operations  │  │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ⬇️
┌─────────────────────────────────────────────────────────────────────────────────┐
│  🧠 AI MODELS & EXTERNAL SERVICES LAYER                                        │
│                                                                                 │
│  ┌─────────────────┬─────────────────┬─────────────────┬─────────────────────┐  │
│  │ 🤖 OLLAMA       │ 🌐 OPENAI       │ 📞 TWILIO       │ 🗺️ LOCATION         │  │
│  │ LOCAL MODELS    │ CLOUD MODELS    │ COMMUNICATION   │ SERVICES            │  │
│  │                 │                 │                 │                     │  │
│  │ • LLaVA 7B      │ • GPT-4o-mini   │ • Voice calls   │ • Google Maps API   │  │
│  │   (Vision)      │   (Orchestrator)│ • SMS messaging │ • Address lookup   │  │
│  │ • MedGemma 7B   │ • Whisper       │ • Emergency     │ • Distance calc     │  │
│  │   (Medical)     │   (Speech)      │   contacts      │ • Route planning    │  │
│  │                 │ • TTS           │                 │                     │  │
│  │ Port: 11434     │ • Text-to-Speech│                 │                     │  │
│  └─────────────────┴─────────────────┴─────────────────┴─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 **Complete Data Flow Sequence**

### 1. 👤 **User Interaction**
```
User Input → Streamlit Frontend
├── Text Message
├── Image Upload (Prescription/Scan)
├── Voice Recording
└── Emergency Button
```

### 2. 🌐 **API Request Processing**
```
Frontend → FastAPI Backend
├── POST /chat (main endpoint)
├── Image data (base64 encoded)
├── Has_image flag
└── User message text
```

### 3. 🤖 **Agentic AI Decision Making**
```
FastAPI → Main Agent (agent.py)
├── Store image data globally
├── Initialize OpenAI GPT-4o-mini
├── Create ReAct agent with tools
├── Execute with max 10 iterations
└── 60-second timeout protection
```

### 4. 🧠 **Intelligent Tool Selection**
```
GPT-4o-mini Orchestrator → Tool Decision
├── Analyze user intent
├── Check for image upload
├── Detect emergency keywords
├── Determine appropriate tool(s)
└── Execute selected tool(s)
```

### 5. 🛠️ **Tool Execution Examples**

#### 🖼️ **Image Analysis Flow**
```
analyze_medical_image Tool
├── Access global image data
├── Convert to base64
├── Send to LLaVA 7B (Ollama)
├── Extract prescription details
└── Return medicine information
```

#### 🏥 **Medical Consultation Flow**
```
ask_medical_specialist Tool
├── Receive medical query
├── Send to MedGemma 7B (Ollama)
├── Generate evidence-based response
├── Add disclaimer
└── Return medical guidance
```

#### 🚨 **Emergency Flow**
```
emergency_call_tool Tool
├── Detect emergency keywords
├── Extract user location
├── Call Twilio API
├── Initiate voice call
└── Send SMS alert
```

### 6. 📊 **Response Generation**
```
Tool Response → Agent Orchestrator
├── Combine tool outputs
├── Generate final response
├── Format for user
└── Return to FastAPI
```

### 7. 🎯 **User Response Delivery**
```
FastAPI → Streamlit Frontend
├── Display chat response
├── Show tool usage info
├── Play TTS audio (optional)
└── Update chat history
```

## 🎛️ **System Configuration**

### 🔧 **Agent Settings**
- **Max Iterations**: 10 (increased from 3)
- **Timeout**: 60 seconds
- **Error Handling**: Graceful fallbacks
- **Logging**: Comprehensive console output

### 🎨 **Frontend Features**
- **Dark Theme**: Custom CSS for better UX
- **Responsive Design**: Works on all devices
- **Real-time Chat**: Instant message display
- **Multi-modal Input**: Text, voice, image support

### 🔐 **Security & Performance**
- **CORS Protection**: Cross-origin request handling
- **Environment Variables**: Secure API key management
- **Async Operations**: Non-blocking request processing
- **Error Boundaries**: Graceful error handling

## 📈 **Monitoring & Logging**

### 📋 **Comprehensive Logging**
```
🤖 [AGENT] - Agent decisions and orchestration
🛠️ [TOOL] - Individual tool executions
🔍 [VISION] - LLaVA image analysis
🏥 [MEDICAL] - MedGemma consultations
📞 [EMERGENCY] - Twilio call operations
📡 [API] - FastAPI request/response cycles
🖼️ [IMAGE] - Image processing steps
⏰ [TIMEOUT] - Timeout and error handling
```

This complete flow diagram shows how your agentic AI system intelligently routes user queries through the appropriate AI models and tools to provide comprehensive medical assistance!
