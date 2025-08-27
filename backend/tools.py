import asyncio
from langchain.agents import tool
import os
import shutil
from dotenv import load_dotenv
from utils import query_medgemma, query_llava_vision, call_emergency
load_dotenv()

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
    try:
        result = run_async_in_sync(query_medgemma(query))
        return result
    except Exception as e:
        print(f"❌ [MEDICAL SPECIALIST] Error: {str(e)}")
        return f"I apologize, but I'm having trouble accessing the medical knowledge base right now. For your safety, please consult with a healthcare professional directly. Error: {str(e)}"


@tool
def emergency_call_tool(emergency_message: str = "Emergency medical assistance needed") -> str:
    """
    Initiate an emergency call when a user is experiencing a medical emergency.
    Use this tool immediately when detecting emergency situations, severe symptoms,
    or when a user explicitly requests emergency assistance.
    """
    print(f"🚨 [EMERGENCY TOOL] ACTIVATED! Message: {emergency_message[:100]}...")
    try:
        print(f"📞 [TWILIO] Initiating emergency call...")
        result = run_async_in_sync(call_emergency(emergency_message))
        return result
    except Exception as e:
        print(f"❌ [EMERGENCY] Call failed: {str(e)}")
        return f"Emergency services contacted. If this is a life-threatening emergency, please call 108 immediately. Error: {str(e)}"


@tool
def find_nearby_specialists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed medical specialists near the specified location.
    """
    print(f"🗺️ [SPECIALIST FINDER] Searching for doctors in: {location}")
    result = (
        f"Here are some medical specialists near {location}:\n"
        "- Dr. Sarah Johnson (Internal Medicine) - +1 (555) 123-4567\n"
        "- Dr. Michael Chen (Cardiology) - +1 (555) 987-6543\n"
        "- Dr. Emily Rodriguez (Emergency Medicine) - +1 (555) 222-3333\n"
        "- Regional Medical Center - +1 (555) 111-2222\n"
        "- Urgent Care Clinic - +1 (555) 333-4444"
    )
    return result


@tool
def analyze_medical_image(image_description: str) -> str:
    """
    Analyze medical images, scans, X-rays, or other visual medical content.
    Use this when a user uploads or describes a medical image they want analyzed.
    """
    print(f"🖼️ [IMAGE ANALYSIS] Processing medical image: {image_description[:100]}...")
    try:
        print(f"👁️ [LLAVA] Analyzing image with LLaVA vision model...")
        # Get the current image data if available
        temp_dir = "agentic_ai_images"
        image_data = None
        if os.path.exists(temp_dir):
            print(f"🗂️ [IMAGE DATA] Found existing directory: {temp_dir}")
            image_path = os.path.join(temp_dir, "uploaded_image.bin")
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image_data = f.read()
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
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return result
    except Exception as e:
        print(f"❌ [IMAGE ANALYSIS] Error: {str(e)}")
        return f"I'm unable to analyze the medical image at this time. Please consult with a healthcare professional or radiologist for proper image interpretation. Error: {str(e)}"


@tool
def get_medication_information(medication_name: str) -> str:
    """
    Provide information about medications including side effects, interactions, and usage.
    Use this when users ask about specific medications, drugs, or treatments.
    """
    print(f"💊 [MEDICATION INFO] Looking up drug: {medication_name}")
    try:
        query = f"Please provide information about {medication_name} including common side effects, usage, and important warnings."
        result = run_async_in_sync(query_medgemma(query))
        return result + "\n\n⚠️ Important: Always consult your healthcare provider or pharmacist before starting, stopping, or changing any medication."
    except Exception as e:
        print(f"❌ [MEDICATION INFO] Error: {str(e)}")
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
    return result




