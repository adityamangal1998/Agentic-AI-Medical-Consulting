"""
Agentic AI Medical Consulting Agent using LangChain and OpenAI
"""

import os
import logging
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
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


# Test function for development
async def test_agent():
    """Test the agent with sample queries"""
    test_queries = [
        "I have a severe headache and feel nauseous. What could be wrong?",
        "I'm having chest pains and trouble breathing. This is an emergency!",
        "Can you help me find a cardiologist in New York?",
        "What are the side effects of ibuprofen?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: {query}")
        result = await process_medical_query(query)
        print(f"🤖 Tool Used: {result['tool_used']}")
        print(f"📝 Response: {result['response'][:200]}...")
        print("-" * 50)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent())

# Agent initialization complete
print("🎉 [AGENTIC AI] Medical Consulting Agent fully initialized and ready!")
print("🛠️ [TOOLS] Available: Medical Specialist, Emergency Call, Specialist Finder, Image Analysis, Voice Transcription, Medication Info, Appointment Helper")
print("🧠 [ORCHESTRATOR] OpenAI GPT-4o-mini ready for intelligent tool selection")
print("=" * 80)
logger.info("🎉 INITIALIZATION: Agentic AI Medical Consulting Agent fully ready for queries")
