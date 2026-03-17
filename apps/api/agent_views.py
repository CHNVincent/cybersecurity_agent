from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from typing import Dict, Any
import json
import uuid

# Import core modules (these would normally be referenced in the real app)
from apps.agent.brain.base import BaseLLM
from apps.agent.brain.ali_bailian import AliBailianLLM
from apps.agent.planning.planner import Planner
from apps.agent.tooluse.skill_manager import SkillManager
from apps.agent.memory.long_term import LongTermMemory, ShortTermMemory
from apps.agent.mcp.mcp_server import MCPServer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def agent_chat(request):
    """
    Endpoint for chatting with the cybersecurity agent
    Expected payload: {
        'message': 'user message content',
        'conversation_id': 'optional existing conv id',
        'files': 'optional file uploads for security analysis'
    }
    """
    message = request.data.get("message", "")
    conversation_id = request.data.get("conversation_id") or str(uuid.uuid4())
    uploaded_files = request.FILES.getlist("files", [])

    # Initialize core agent components
    # Note: In the actual project, this initialization will happen in the main agent class
    # For the demo purpose, we're loading a config directly:
    model_configs = BaseLLM.load_model_config()

    if not model_configs:
        return Response(
            {"error": "No model configurations found"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Select first model from config (in real implementation would be more sophisticated)
    model_config = model_configs[0]

    try:
        # Create LLM instance based on config
        llm = BaseLLM.create_llm_instance(model_config)

        # Initialize the short term memory (conversation context memory)
        short_term_mem = ShortTermMemory(capacity=20)
        short_term_mem.set_conversation_id(conversation_id)

        # Load conversation history from long term memory if exists
        long_term_mem = LongTermMemory()

        # If existing conversation, load context
        if conversation_id:
            # In a real scenario, we'd load from DB by conversation_id
            pass

        # Add user message to short-term memory
        user_msg = {"role": "user", "content": message}
        short_term_mem.add_message(user_msg)

        # Get recent messages as context
        conversation_context = short_term_mem.get_recent_messages()

        # Process the response through the agent pipeline
        # For now, we'll simulate a response using the LLM directly
        response_data = llm.chat(conversation_context)

        # Extract response content
        assistant_reply = (
            response_data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "I encountered an issue processing your request.")
        )

        # Add assistant response to memory
        assistant_msg = {"role": "assistant", "content": assistant_reply}
        short_term_mem.add_message(assistant_msg)

        # If files were uploaded, we might trigger code audit skills
        processed_files = []
        for uploaded_file in uploaded_files:
            # Save file to media directory
            file_path = default_storage.save(
                f"uploads/{uploaded_file.name}", ContentFile(uploaded_file.read())
            )
            processed_files.append(file_path)

        # For file analysis, we would trigger skills here
        if (
            processed_files
            and "audit" in message.lower()
            or "analyze" in message.lower()
        ):
            # This is where we'd trigger the code audit skill
            skill_manager = SkillManager()
            for file_path in processed_files:
                try:
                    # Try to execute the code audit skill with the uploaded file
                    result = skill_manager.execute_skill(
                        "code_audit", file_path=file_path
                    )
                    # Add this to our response as needed
                except Exception:
                    # Skill may not exist yet - that's expected during setup
                    pass

        return Response(
            {
                "response": assistant_reply,
                "conversation_id": conversation_id,
                "processed_files": processed_files,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error processing request: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_installed_skills(request):
    """
    Endpoint to list all installed skills
    """
    try:
        skill_manager = SkillManager()
        available_skills = skill_manager.list_available_skills()
        return Response({"skills": available_skills})
    except Exception as e:
        return Response(
            {"error": f"Error listing skills: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# These functions would typically be in a separate core agent class, but are defined here for the endpoints:
def initialize_agent():
    """
    Initialize the agent with its full capabilities: brain, planning, tool use, memory, MCP
    """
    # Load configurations
    model_configs = BaseLLM.load_model_config()
    model_config = model_configs[0] if model_configs else None

    if model_config:
        # Create LLM instance
        llm = BaseLLM.create_llm_instance(model_config)

        # Initialize components
        planner = Planner(llm)
        skill_manager = SkillManager()
        short_term_memory = ShortTermMemory()
        long_term_memory = LongTermMemory()
        mcp_server = MCPServer(skill_manager=skill_manager)

        return {
            "llm": llm,
            "planner": planner,
            "skill_manager": skill_manager,
            "short_term_memory": short_term_memory,
            "long_term_memory": long_term_memory,
            "mcp_server": mcp_server,
        }
    else:
        raise Exception("No suitable model configuration found")
