# 🏥 Agentic AI Medical Consulting - Visual Flow Diagrams

## 🎯 **High-Level System Architecture (Mermaid)**

```mermaid
graph TB
    %% User Interface Layer
    subgraph "🌐 Frontend Layer (Port 8501)"
        UI[👤 Streamlit Interface]
        CHAT[💬 Chat Input]
        IMG[🖼️ Image Upload]
        VOICE[🎤 Voice Input]
        EMERGENCY[🚨 Emergency Button]
    end

    %% API Gateway Layer
    subgraph "🔗 API Gateway (Port 8000)"
        API[🌐 FastAPI Server]
        ENDPOINTS[📡 REST Endpoints]
        CORS[🛡️ CORS Middleware]
    end

    %% Agentic AI Layer
    subgraph "🤖 Agentic AI Orchestration"
        AGENT[🧠 Main Agent]
        GPT4[🎯 GPT-4o-mini Orchestrator]
        REACT[📋 ReAct Pattern]
        DECISION[🔍 Tool Selection Logic]
    end

    %% Tools Layer
    subgraph "🛠️ Specialized Tools"
        MEDICAL[🏥 Medical Specialist]
        IMAGE_TOOL[🖼️ Image Analysis]
        EMERGENCY_TOOL[🚨 Emergency Call]
        LOCATION[📍 Location Finder]
        MEDICATION[💊 Medication Info]
        VOICE_TOOL[🎤 Voice Transcription]
        APPOINTMENT[📅 Appointment Helper]
    end

    %% AI Models Layer
    subgraph "🧠 AI Models & Services"
        OLLAMA[🤖 Ollama Local Models]
        LLAVA[👁️ LLaVA 7B Vision]
        MEDGEMMA[🏥 MedGemma 7B Medical]
        OPENAI[🌐 OpenAI Services]
        WHISPER[🎤 Whisper Speech]
        TTS[🔊 Text-to-Speech]
        TWILIO[📞 Twilio Communication]
    end

    %% Data Flow
    UI --> API
    CHAT --> API
    IMG --> API
    VOICE --> API
    EMERGENCY --> API

    API --> AGENT
    AGENT --> GPT4
    GPT4 --> REACT
    REACT --> DECISION

    DECISION --> MEDICAL
    DECISION --> IMAGE_TOOL
    DECISION --> EMERGENCY_TOOL
    DECISION --> LOCATION
    DECISION --> MEDICATION
    DECISION --> VOICE_TOOL
    DECISION --> APPOINTMENT

    MEDICAL --> MEDGEMMA
    IMAGE_TOOL --> LLAVA
    EMERGENCY_TOOL --> TWILIO
    VOICE_TOOL --> WHISPER
    APPOINTMENT --> OPENAI

    %% Styling
    classDef frontend fill:#3b82f6,stroke:#1e40af,stroke-width:2px,color:#fff
    classDef api fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    classDef agent fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    classDef tools fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    classDef models fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff

    class UI,CHAT,IMG,VOICE,EMERGENCY frontend
    class API,ENDPOINTS,CORS api
    class AGENT,GPT4,REACT,DECISION agent
    class MEDICAL,IMAGE_TOOL,EMERGENCY_TOOL,LOCATION,MEDICATION,VOICE_TOOL,APPOINTMENT tools
    class OLLAMA,LLAVA,MEDGEMMA,OPENAI,WHISPER,TTS,TWILIO models
```

## 🔄 **Detailed Agent Decision Flow**

```mermaid
flowchart TD
    START([🚀 User Query Received]) --> PARSE[📋 Parse Input]
    PARSE --> IMAGE_CHECK{🖼️ Image Uploaded?}
    
    IMAGE_CHECK -->|Yes| IMAGE_FLOW[🔍 Image Analysis Flow]
    IMAGE_CHECK -->|No| TEXT_ANALYSIS[📝 Text Analysis]
    
    IMAGE_FLOW --> LLAVA_PROCESS[👁️ LLaVA 7B Processing]
    LLAVA_PROCESS --> PRESCRIPTION[💊 Extract Medicines]
    PRESCRIPTION --> COMBINE_RESULTS[🔄 Combine Results]
    
    TEXT_ANALYSIS --> EMERGENCY_CHECK{🚨 Emergency Keywords?}
    EMERGENCY_CHECK -->|Yes| EMERGENCY_FLOW[📞 Emergency Call]
    EMERGENCY_CHECK -->|No| INTENT_ANALYSIS[🎯 Analyze Intent]
    
    EMERGENCY_FLOW --> TWILIO_CALL[📱 Twilio Emergency Call]
    TWILIO_CALL --> COMBINE_RESULTS
    
    INTENT_ANALYSIS --> MEDICAL_CHECK{🏥 Medical Question?}
    MEDICAL_CHECK -->|Yes| MEDGEMMA_FLOW[🧠 MedGemma Consultation]
    MEDICAL_CHECK -->|No| OTHER_TOOLS[🛠️ Other Tools]
    
    MEDGEMMA_FLOW --> MEDICAL_RESPONSE[💬 Medical Guidance]
    MEDICAL_RESPONSE --> COMBINE_RESULTS
    
    OTHER_TOOLS --> LOCATION_TOOL[📍 Location Finder]
    OTHER_TOOLS --> MEDICATION_TOOL[💊 Medication Info]
    OTHER_TOOLS --> VOICE_TOOL[🎤 Voice Processing]
    OTHER_TOOLS --> APPOINTMENT_TOOL[📅 Appointment Helper]
    
    LOCATION_TOOL --> COMBINE_RESULTS
    MEDICATION_TOOL --> COMBINE_RESULTS
    VOICE_TOOL --> COMBINE_RESULTS
    APPOINTMENT_TOOL --> COMBINE_RESULTS
    
    COMBINE_RESULTS --> FINAL_RESPONSE[📤 Generate Final Response]
    FINAL_RESPONSE --> RETURN([✅ Return to User])
    
    %% Styling
    classDef startEnd fill:#22c55e,stroke:#16a34a,stroke-width:3px,color:#fff
    classDef decision fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    classDef process fill:#3b82f6,stroke:#2563eb,stroke-width:2px,color:#fff
    classDef model fill:#ef4444,stroke:#dc2626,stroke-width:2px,color:#fff
    
    class START,RETURN startEnd
    class IMAGE_CHECK,EMERGENCY_CHECK,MEDICAL_CHECK decision
    class PARSE,TEXT_ANALYSIS,INTENT_ANALYSIS,COMBINE_RESULTS,FINAL_RESPONSE process
    class LLAVA_PROCESS,MEDGEMMA_FLOW,TWILIO_CALL model
```

## 🏗️ **System Architecture Layers**

```mermaid
graph LR
    subgraph "Layer 1: User Interface"
        A1[👤 User]
        A2[🌐 Streamlit Frontend]
        A3[🎨 Dark Theme UI]
    end
    
    subgraph "Layer 2: API Gateway"
        B1[🔗 FastAPI Server]
        B2[🛡️ CORS & Security]
        B3[📝 Request Logging]
    end
    
    subgraph "Layer 3: AI Orchestration"
        C1[🤖 LangChain Agent]
        C2[🧠 GPT-4o-mini]
        C3[📋 ReAct Pattern]
    end
    
    subgraph "Layer 4: Specialized Tools"
        D1[🏥 Medical Tools]
        D2[🖼️ Vision Tools]
        D3[🚨 Emergency Tools]
        D4[📞 Communication Tools]
    end
    
    subgraph "Layer 5: AI Models"
        E1[🤖 Ollama Models]
        E2[🌐 OpenAI Models]
        E3[📞 Twilio Services]
    end
    
    A1 --> A2
    A2 --> A3
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> D1
    C3 --> D2
    C3 --> D3
    C3 --> D4
    D1 --> E1
    D2 --> E1
    D3 --> E3
    D4 --> E2
```

## 📊 **Tool Selection Matrix**

| User Input Type | Primary Tool | Secondary Tool | AI Model Used |
|----------------|--------------|----------------|---------------|
| 🖼️ **Image Upload** | `analyze_medical_image` | `ask_medical_specialist` | LLaVA 7B + MedGemma 7B |
| 🚨 **Emergency Keywords** | `emergency_call_tool` | `find_nearby_specialists` | Twilio API |
| 🏥 **Medical Questions** | `ask_medical_specialist` | - | MedGemma 7B |
| 📍 **Location Queries** | `find_nearby_specialists_by_location` | - | Google Maps API |
| 💊 **Medication Info** | `get_medication_information` | `ask_medical_specialist` | Drug Database + MedGemma |
| 🎤 **Voice Input** | `transcribe_voice_message` | `ask_medical_specialist` | Whisper + MedGemma |
| 📅 **Appointments** | `schedule_appointment_helper` | `find_nearby_specialists` | GPT-4o-mini |

## 🔍 **Agent Execution Timeline**

```mermaid
gantt
    title Agentic AI Processing Timeline
    dateFormat X
    axisFormat %s
    
    section Input Processing
    Parse Request     :0, 1
    Image Processing  :1, 3
    
    section AI Orchestration
    GPT-4o Decision   :3, 5
    Tool Selection    :5, 6
    
    section Tool Execution
    Model Inference   :6, 15
    Result Processing :15, 17
    
    section Response Generation
    Combine Results   :17, 19
    Format Response   :19, 20
    
    section Delivery
    Return to User    :20, 21
```

This comprehensive flow diagram shows exactly how your agentic AI medical consulting system processes user queries through intelligent tool selection and multiple AI models to provide comprehensive medical assistance!
