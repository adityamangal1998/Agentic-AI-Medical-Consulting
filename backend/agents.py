import os
import shutil
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from config import agent_template
from tools import (
    ask_medical_specialist,
    emergency_call_tool,
    find_nearby_specialists_by_location,
    analyze_medical_image,
    get_medication_information,
    schedule_appointment_helper
)

load_dotenv()

# Initialize tools
tools = [
    ask_medical_specialist,
    emergency_call_tool,
    find_nearby_specialists_by_location,
    analyze_medical_image,
    get_medication_information,
    schedule_appointment_helper
]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY")
)


prompt = PromptTemplate.from_template(agent_template)
agent = create_react_agent(llm, tools, prompt)
print("✅ [AGENT] ReAct agent created successfully")


agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False, 
    handle_parsing_errors=True,
    max_iterations=10
)


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
    
    # Store image data globally for tools to access
    if has_image and image_data:
        # Store image data in a way tools can access it
        # Save the image data to a temporary file and store the path for tools to access
        temp_dir = "agentic_ai_images"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        else:
            os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, f"uploaded_image.bin")
        with open(image_path, "wb") as f:
            f.write(image_data)
        print(f"🖼️ [IMAGE DATA] Stored {len(image_data)} bytes for analysis")
    try:
        # Modify input if image is present
        original_input = user_input
        if has_image and image_context:
            user_input = f"{user_input} [Image uploaded: {image_context}]"

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
                    timeout=90
                )
            except asyncio.TimeoutError:
                return {
                    "response": "I apologize, but your query is taking longer than expected to process. Please try asking a more specific question or break down your request into smaller parts.",
                    "tool_used": "timeout_handler",
                    "all_tools_used": ["timeout_handler"],
                    "source": "timeout_handler",
                    "has_emergency": False
                }
        
        # Extract information from the result
        response = result.get("output", "I'm here to help with your medical questions.")
        print(f"📝 [RESPONSE] Generated response: {len(response)} characters")
        # Check if emergency was detected (basic keyword check)
        emergency_keywords = ["emergency", "urgent", "severe", "critical", "help", "pain", "bleeding", "cant breathe", "chest pain"]
        has_emergency = any(keyword in original_input.lower() for keyword in emergency_keywords)
        
        if has_emergency:
            print(f"🚨 [EMERGENCY DETECTED] Emergency keywords found in query!")
        final_result = {
            "response": response,
            "tool_used": "agentic_ai",
            "all_tools_used": ["medical_agent"],
            "source": "agentic_ai",
            "has_emergency": has_emergency
        }
        return final_result
        
    except Exception as e:
        print(f"❌ [ERROR] Agent execution failed: {str(e)}")
        return {
            "response": f"I apologize, but I encountered an issue processing your request: {str(e)}. Please try rephrasing your question or contact a healthcare professional directly if this is urgent.",
            "tool_used": "error",
            "all_tools_used": [],
            "source": "error",
            "has_emergency": False
        }
