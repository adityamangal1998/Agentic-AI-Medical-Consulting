import io
import base64
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv
from PIL import Image
from utils import call_emergency, transcribe_audio_whisper, generate_speech_tts
from agents import process_medical_query
# Load environment variables
load_dotenv()

app = FastAPI(title="Agentic AI Medical Consulting API", version="2.0.0")
# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],  # Allow Streamlit
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    has_image: bool = False
    image_data: Optional[str] = None  # base64 encoded image

class ChatResponse(BaseModel):
    response: str
    source: str  # "agentic_ai"
    tool_used: Optional[str] = None
    has_emergency: bool = False

class TTSRequest(BaseModel):
    text: str

class EmergencyRequest(BaseModel):
    message: Optional[str] = "Emergency medical assistance needed. Please call back immediately."

@app.get("/")
async def root():
    return {"message": "Agentic AI Medical Consulting API is running", "version": "2.0.0", "agent": "LangChain + OpenAI"}



@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint using Agentic AI with LangChain tools"""
    try:
        # Prepare image context if available
        image_context = None
        image_bytes = None
        if request.has_image and request.image_data:
            print(f"🖼️ [IMAGE PROCESSING] Processing uploaded image...")
            try:
                # Decode and validate image
                image_bytes = base64.b64decode(request.image_data)
                image = Image.open(io.BytesIO(image_bytes))
                image_context = f"Medical image uploaded - Format: {image.format}, Size: {image.size}"
            except Exception as e:
                image_context = f"Image processing error: {str(e)}"
                print(f"❌ [IMAGE] Processing failed: {str(e)}")
        # Process query using agentic AI
        result = await process_medical_query(
            user_input=request.message,
            has_image=request.has_image,
            image_context=image_context,
            image_data=image_bytes
        )
        return ChatResponse(
            response=result["response"],
            source=result["source"],
            tool_used=result.get("tool_used"),
            has_emergency=result.get("has_emergency", False)
        )
            
    except Exception as e:
        print(f"❌ [CHAT] Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/voice")
async def transcribe_voice(audio_file: UploadFile = File(...)):
    """Transcribe voice input using OpenAI Whisper"""
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Transcribe using helper function
        transcript_text = transcribe_audio_whisper(audio_data)
        
        return {"text": transcript_text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech using OpenAI TTS"""
    try:
        audio_data = generate_speech_tts(request.text)
        
        return Response(
            content=audio_data,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

@app.post("/emergency-call")
async def emergency_call(request: EmergencyRequest):
    """Trigger emergency call using Twilio"""
    try:
        result = call_emergency(request.message)
        return {"status": "success", "message": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making emergency call: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
