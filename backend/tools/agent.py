"""
Agentic AI Medical Consulting Agent using LangChain and OpenAI
"""

import os
import logging
import httpx
import base64
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from twilio.rest import Client
from openai import OpenAI
from .langchain_tools import (
    ask_medical_specialist,
    emergency_call_tool,
    find_nearby_specialists_by_location,
    analyze_medical_image,
    transcribe_voice_message,
    get_medication_information,
    schedule_appointment_helper
)

load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 [AGENTIC AI] Initializing Medical Consulting Agent...")
logger.info("🤖 AGENT: Initializing Agentic AI Medical Consulting System")

# Initialize tools
tools = [
    ask_medical_specialist,
    emergency_call_tool,
    find_nearby_specialists_by_location,
    analyze_medical_image,
    transcribe_voice_message,
    get_medication_information,
    schedule_appointment_helper
]

print(f"🛠️ [TOOLS] Loaded {len(tools)} specialized medical tools")
logger.info(f"🛠️ TOOLS: Successfully loaded {len(tools)} medical tools: {[tool.name for tool in tools]}")

# Initialize the OpenAI LLM
print("🧠 [LLM] Initializing OpenAI GPT-4o-mini for orchestration...")
logger.info("🧠 LLM: Initializing ChatOpenAI with model gpt-4o-mini")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)

print("✅ [LLM] OpenAI model initialized successfully")
logger.info("✅ LLM: ChatOpenAI model ready for orchestration")

# Create a simple prompt for the agent
print("📋 [PROMPT] Creating ReAct agent prompt template...")
template = """You are an AI medical consulting assistant with access to specialized medical tools.

You have access to the following tools:
{tools}

Tool names: {tool_names}

IMPORTANT GUIDELINES:
- If the user mentions uploading an image, prescription, medical scan, or asks about "medicines in this image", ALWAYS use the analyze_medical_image tool
- For emergency situations (chest pain, breathing problems, severe symptoms), use emergency_call_tool
- For finding doctors/specialists in a location, use find_nearby_specialists_by_location
- For medication questions, use get_medication_information
- For appointment help, use schedule_appointment_helper
- For general medical questions, use ask_medical_specialist

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
print("✅ [PROMPT] ReAct prompt template created")
logger.info("✅ PROMPT: ReAct template configured for medical agent")

# Create the agent
print("🔧 [AGENT] Creating ReAct agent with LangChain...")
agent = create_react_agent(llm, tools, prompt)
print("✅ [AGENT] ReAct agent created successfully")
logger.info("✅ AGENT: ReAct agent created with OpenAI LLM and medical tools")

# Create the agent executor
print("⚙️ [EXECUTOR] Setting up agent executor...")
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False, 
    handle_parsing_errors=True,
    max_iterations=10
)
print("✅ [EXECUTOR] Agent executor ready (max_iterations=10)")
logger.info("✅ EXECUTOR: AgentExecutor configured with error handling")

# Global variable to store current image data for tools
_current_image_data = None

async def process_medical_query(user_input: str, has_image: bool = False, image_context: str = None, image_data: bytes = None) -> dict:
    """
    Process a medical query using the agentic AI system
    
    Args:
        user_input (str): The user's question or message
        has_image (bool): Whether an image was uploaded
        image_context (str): Context about the uploaded image
        image_data (bytes): The actual image data for analysis
    
    Returns:
        dict: Response containing the AI's answer, tools used, and metadata
    """
    print(f"\n🚀 [QUERY START] Processing: '{user_input[:100]}...'")
    logger.info(f"🚀 QUERY: Starting processing for user input: {user_input[:100]}...")
    
    # Store image data globally for tools to access
    if has_image and image_data:
        import tempfile
        import base64
        
        # Store image data in a way tools can access it
        global _current_image_data
        _current_image_data = image_data
        print(f"🖼️ [IMAGE DATA] Stored {len(image_data)} bytes for analysis")
        logger.info(f"🖼️ IMAGE: Stored image data ({len(image_data)} bytes) for tool access")
    
    try:
        # Modify input if image is present
        original_input = user_input
        if has_image and image_context:
            user_input = f"{user_input} [Image uploaded: {image_context}]"
            print(f"🖼️ [IMAGE CONTEXT] Added image context to query")
            logger.info(f"🖼️ IMAGE: Added image context to user query")
        
        print(f"🧠 [AGENT EXECUTION] Invoking ReAct agent with LangChain...")
        logger.info(f"🧠 AGENT: Starting ReAct agent execution with input: {user_input[:100]}...")
        
        # Execute the agent with timeout protection
        import concurrent.futures
        import asyncio
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                # Set timeout to 60 seconds to prevent hanging
                result = await asyncio.wait_for(
                    loop.run_in_executor(
                        executor, 
                        lambda: agent_executor.invoke({"input": user_input})
                    ),
                    timeout=60.0
                )
            except asyncio.TimeoutError:
                print(f"⏰ [TIMEOUT] Agent execution exceeded 60 second limit")
                logger.warning(f"⏰ TIMEOUT: Agent execution timed out after 60 seconds")
                return {
                    "response": "I apologize, but your query is taking longer than expected to process. Please try asking a more specific question or break down your request into smaller parts.",
                    "tool_used": "timeout_handler",
                    "all_tools_used": ["timeout_handler"],
                    "source": "timeout_handler",
                    "has_emergency": False
                }
        
        print(f"✅ [AGENT COMPLETE] Agent execution finished successfully")
        logger.info(f"✅ AGENT: Execution completed successfully")
        
        # Extract information from the result
        response = result.get("output", "I'm here to help with your medical questions.")
        print(f"📝 [RESPONSE] Generated response: {len(response)} characters")
        
        # Check if emergency was detected (basic keyword check)
        emergency_keywords = ["emergency", "urgent", "severe", "critical", "help", "pain", "bleeding", "cant breathe", "chest pain"]
        has_emergency = any(keyword in original_input.lower() for keyword in emergency_keywords)
        
        if has_emergency:
            print(f"🚨 [EMERGENCY DETECTED] Emergency keywords found in query!")
            logger.warning(f"🚨 EMERGENCY: Emergency keywords detected in user input")
        
        final_result = {
            "response": response,
            "tool_used": "agentic_ai",
            "all_tools_used": ["medical_agent"],
            "source": "agentic_ai",
            "has_emergency": has_emergency
        }
        
        print(f"🎯 [QUERY END] Successfully processed query")
        logger.info(f"🎯 QUERY: Successfully completed processing")
        return final_result
        
    except Exception as e:
        print(f"❌ [ERROR] Agent execution failed: {str(e)}")
        logger.error(f"❌ ERROR: Agent execution failed: {str(e)}")
        return {
            "response": f"I apologize, but I encountered an issue processing your request: {str(e)}. Please try rephrasing your question or contact a healthcare professional directly if this is urgent.",
            "tool_used": "error",
            "all_tools_used": [],
            "source": "error",
            "has_emergency": False
        }


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


def transcribe_audio_whisper(audio_bytes: bytes) -> str:
    """
    Transcribe audio using OpenAI Whisper
    """
    try:
        from openai import OpenAI
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
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        
        return response.content
        
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")


