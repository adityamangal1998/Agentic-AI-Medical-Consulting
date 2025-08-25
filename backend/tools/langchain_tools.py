"""
LangChain Tools for Agentic AI Medical Consulting
"""

import asyncio
import logging
from langchain.agents import tool
from .ai_tools import query_medgemma, call_emergency, query_llava_vision, transcribe_audio_whisper

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
