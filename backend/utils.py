import os
import httpx
import base64
from twilio.rest import Client
from openai import OpenAI

async def query_medgemma(query: str) -> str:
    """
    Query MedGemma model via Ollama for medical analysis
    """
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        medgemma_model = os.getenv("MEDGEMMA_MODEL", "gemma:7b")
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": medgemma_model,
                "prompt": f"As a medical AI assistant, please analyze the following query and provide helpful medical information. Remember to always recommend consulting with healthcare professionals for proper diagnosis and treatment.\n\nQuery: {query}",
                "stream": False
            }
            
            response = await client.post(
                f"{base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Unable to process medical query.")
            else:
                return f"Error connecting to MedGemma service (Status: {response.status_code}). Please try again later."
                
    except Exception as e:
        return f"Error connecting to MedGemma: {str(e)}. Please consult a healthcare professional."


async def query_llava_vision(query: str, image_data: bytes = None) -> str:
    """
    Query LLaVA model for image analysis
    """
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        llava_model = os.getenv("LLAVA_MODEL", "llava:7b")
        
        if image_data is None:
            return "No image data provided for analysis. Please upload an image and try again."
        
        # Convert image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "model": llava_model,
                "prompt": f"""As a medical AI assistant analyzing a medical prescription or medical image, please:

                1. Carefully examine the image and describe what you see in detail
                2. If this is a prescription, list all medicines, dosages, frequency, and instructions you can identify
                3. If this is a medical scan/report, describe the findings and any notable features
                4. Provide clear, organized information about what is visible in the image
                5. Always emphasize that this is for informational purposes only
                6. Recommend consulting healthcare professionals for proper medical advice

                User's question: {query}

                Please provide a comprehensive analysis of what you can see in this medical image.""",
                "images": [image_b64],
                "stream": False
            }
            
            response = await client.post(
                f"{base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Unable to process medical image.")
            else:
                return f"Error connecting to LLaVA vision service (Status: {response.status_code}). Please try again later."
                
    except Exception as e:
        return f"Error processing medical image: {str(e)}. Please consult a healthcare professional for proper image analysis."


def call_emergency(message: str = "Emergency medical assistance needed. Please call back immediately.") -> str:
    """
    Make emergency call using Twilio
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_FROM_NUMBER")
        to_number = os.getenv("EMERGENCY_CONTACT")
        
        if not all([account_sid, auth_token, from_number, to_number]):
            return "Emergency call configuration missing. Please contact emergency services directly."
        
        client = Client(account_sid, auth_token)
        
        twiml_message = f"""
        <Response>
            <Say voice="alice">
                {message}
            </Say>
            <Say voice="alice">
                This is an automated emergency call from the AI Medical Consulting system. 
                Please contact the user immediately for medical assistance.
            </Say>
        </Response>
        """
        
        call = client.calls.create(
            twiml=twiml_message,
            to=to_number,
            from_=from_number
        )
        return f"Emergency call initiated successfully. Call SID: {call.sid}"
        
    except Exception as e:
        return f"Failed to make emergency call: {str(e)}. Please contact emergency services directly."


def transcribe_audio_whisper(audio_bytes: bytes) -> str:
    """
    Transcribe audio using OpenAI Whisper
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Create file-like object
        import io
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text
        
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"


def generate_speech_tts(text: str) -> bytes:
    """
    Generate speech using OpenAI TTS
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        return response.content
        
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")
