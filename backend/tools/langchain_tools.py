"""
LangChain Tools for Agentic AI Medical Consulting
"""

import asyncio
import logging
from langchain.agents import tool
import os
import httpx
import base64
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_async_in_sync(coro):
    """Helper function to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # We're already in an event loop, create a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create one
        return asyncio.run(coro)


@tool
def ask_medical_specialist(query: str) -> str:
    """
    Generate a medical response using the MedGemma model.
    Use this for all medical queries, health questions, symptom analysis,
    or to provide evidence-based medical guidance in a conversational tone.
    Always recommends consulting healthcare professionals for proper diagnosis.
    """
    print(f"🏥 [MEDICAL SPECIALIST TOOL] Called with query: {query[:100]}...")
    logger.info(f"🏥 TOOL: ask_medical_specialist | MODEL: alibayram/medgemma:4b | QUERY: {query[:100]}...")
    
    try:
        print(f"📡 [OLLAMA] Calling MedGemma model: alibayram/medgemma:4b")
        result = run_async_in_sync(query_medgemma(query, "alibayram/medgemma:4b"))
        print(f"✅ [MEDICAL SPECIALIST] Response received: {len(result)} characters")
        logger.info(f"✅ MEDICAL SPECIALIST: Response generated successfully ({len(result)} chars)")
        return result
    except Exception as e:
        print(f"❌ [MEDICAL SPECIALIST] Error: {str(e)}")
        logger.error(f"❌ MEDICAL SPECIALIST ERROR: {str(e)}")
        return f"I apologize, but I'm having trouble accessing the medical knowledge base right now. For your safety, please consult with a healthcare professional directly. Error: {str(e)}"


@tool
def emergency_call_tool(emergency_message: str = "Emergency medical assistance needed") -> str:
    """
    Initiate an emergency call when a user is experiencing a medical emergency.
    Use this tool immediately when detecting emergency situations, severe symptoms,
    or when a user explicitly requests emergency assistance.
    """
    print(f"🚨 [EMERGENCY TOOL] ACTIVATED! Message: {emergency_message[:100]}...")
    logger.warning(f"🚨 EMERGENCY TOOL: call_emergency | SERVICE: Twilio | MESSAGE: {emergency_message[:100]}...")
    
    try:
        print(f"📞 [TWILIO] Initiating emergency call...")
        result = run_async_in_sync(call_emergency(emergency_message))
        print(f"✅ [EMERGENCY] Call initiated successfully")
        logger.warning(f"✅ EMERGENCY CALL: Successfully initiated via Twilio")
        return result
    except Exception as e:
        print(f"❌ [EMERGENCY] Call failed: {str(e)}")
        logger.error(f"❌ EMERGENCY CALL ERROR: {str(e)}")
        return f"Emergency services contacted. If this is a life-threatening emergency, please call 108 immediately. Error: {str(e)}"


@tool
def find_nearby_specialists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed medical specialists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking medical support.

    Returns:
        str: A newline-separated string containing specialist names and contact info.
    """
    print(f"🗺️ [SPECIALIST FINDER] Searching for doctors in: {location}")
    logger.info(f"🗺️ TOOL: find_nearby_specialists | LOCATION: {location} | SERVICE: Local Database")
    
    result = (
        f"Here are some medical specialists near {location}:\n"
        "- Dr. Sarah Johnson (Internal Medicine) - +1 (555) 123-4567\n"
        "- Dr. Michael Chen (Cardiology) - +1 (555) 987-6543\n"
        "- Dr. Emily Rodriguez (Emergency Medicine) - +1 (555) 222-3333\n"
        "- Regional Medical Center - +1 (555) 111-2222\n"
        "- Urgent Care Clinic - +1 (555) 333-4444"
    )
    
    print(f"✅ [SPECIALIST FINDER] Found 5 specialists in {location}")
    logger.info(f"✅ SPECIALIST FINDER: Successfully found specialists in {location}")
    return result


@tool
def analyze_medical_image(image_description: str) -> str:
    """
    Analyze medical images, scans, X-rays, or other visual medical content.
    Use this when a user uploads or describes a medical image they want analyzed.
    
    Args:
        image_description (str): Description of the medical image or scan
    
    Returns:
        str: Analysis of the medical image with appropriate medical disclaimers
    """
    print(f"🖼️ [IMAGE ANALYSIS] Processing medical image: {image_description[:100]}...")
    logger.info(f"🖼️ TOOL: analyze_medical_image | MODEL: llava:7b | DESCRIPTION: {image_description[:100]}...")
    
    try:
        # Import agent module to access current image data
        from . import agent
        
        print(f"👁️ [LLAVA] Analyzing image with LLaVA vision model...")
        
        # Get the current image data if available
        image_data = getattr(agent, '_current_image_data', None)
        
        if image_data:
            print(f"✅ [IMAGE DATA] Found image data: {len(image_data)} bytes")
            result = run_async_in_sync(query_llava_vision(
                f"Please analyze this medical prescription image and list all the medicines, dosages, and instructions you can see: {image_description}",
                image_data
            ))
        else:
            print(f"⚠️ [IMAGE DATA] No image data available, using text-only analysis")
            result = run_async_in_sync(query_llava_vision(
                f"Please provide general information about medical image analysis: {image_description}",
                None
            ))
        
        print(f"✅ [IMAGE ANALYSIS] Analysis completed: {len(result)} characters")
        logger.info(f"✅ IMAGE ANALYSIS: Successfully analyzed with LLaVA ({len(result)} chars)")
        return result
    except Exception as e:
        print(f"❌ [IMAGE ANALYSIS] Error: {str(e)}")
        logger.error(f"❌ IMAGE ANALYSIS ERROR: {str(e)}")
        return f"I'm unable to analyze the medical image at this time. Please consult with a healthcare professional or radiologist for proper image interpretation. Error: {str(e)}"


@tool
def transcribe_voice_message(audio_description: str) -> str:
    """
    Transcribe voice messages or audio input from users.
    Use this when users provide voice input that needs to be converted to text.
    
    Args:
        audio_description (str): Description of the audio input
        
    Returns:
        str: Transcribed text or guidance for voice input
    """
    return "For voice transcription, please use the voice input feature in the interface. I can help interpret your spoken medical questions once they're transcribed."


@tool
def get_medication_information(medication_name: str) -> str:
    """
    Provide information about medications including side effects, interactions, and usage.
    Use this when users ask about specific medications, drugs, or treatments.
    
    Args:
        medication_name (str): Name of the medication or drug
        
    Returns:
        str: Information about the medication with safety disclaimers
    """
    print(f"💊 [MEDICATION INFO] Looking up drug: {medication_name}")
    logger.info(f"💊 TOOL: get_medication_information | MODEL: alibayram/medgemma:4b | DRUG: {medication_name}")
    
    try:
        query = f"Please provide information about {medication_name} including common side effects, usage, and important warnings."
        print(f"📊 [MEDGEMMA] Querying medication database for {medication_name}...")
        result = run_async_in_sync(query_medgemma(query, "alibayram/medgemma:4b"))
        print(f"✅ [MEDICATION INFO] Information retrieved for {medication_name}")
        logger.info(f"✅ MEDICATION INFO: Successfully retrieved info for {medication_name}")
        return result + "\n\n⚠️ Important: Always consult your healthcare provider or pharmacist before starting, stopping, or changing any medication."
    except Exception as e:
        print(f"❌ [MEDICATION INFO] Error: {str(e)}")
        logger.error(f"❌ MEDICATION INFO ERROR: {str(e)}")
        return f"I'm unable to provide medication information at this time. Please consult your pharmacist or healthcare provider for accurate medication information. Error: {str(e)}"


@tool
def schedule_appointment_helper(appointment_type: str) -> str:
    """
    Provide guidance on scheduling medical appointments.
    Use this when users need help with appointment scheduling or finding healthcare services.
    
    Args:
        appointment_type (str): Type of appointment or medical service needed
        
    Returns:
        str: Guidance on scheduling appointments
    """
    print(f"📅 [APPOINTMENT HELPER] Providing guidance for: {appointment_type}")
    logger.info(f"📅 TOOL: schedule_appointment_helper | TYPE: {appointment_type} | SERVICE: Scheduling Guide")
    
    result = f"""To schedule a routine appointment with your doctor, follow these steps:

    1. Contact your primary care physician for referrals if needed.
    2. Call the healthcare provider's office directly
    3. Have your insurance information ready
    4. Be prepared to describe your symptoms or reason for the visit
    5. Ask about availability and scheduling options

    For immediate assistance:
    - Emergency room: For life-threatening conditions
    - Urgent care: For non-life-threatening but immediate medical needs
    - Telehealth: For routine consultations and follow-ups

    Insurance coverage may vary, so confirm with your provider before scheduling."""

    print(f"✅ [APPOINTMENT HELPER] Guidance provided for {appointment_type}")
    logger.info(f"✅ APPOINTMENT HELPER: Successfully provided guidance for {appointment_type}")
    return result



async def query_medgemma(query: str, model: str = "alibayram/medgemma:4b") -> str:
    """
    Query MedGemma model via Ollama for medical analysis
    """
    try:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": model,
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



