"""
OpenAI Agent Configuration

This module defines configuration for the OpenAI Agents SDK.
Unlike CrewAI which uses YAML, OpenAI SDK uses Python configuration.

Configuration includes:
- Agent name and instructions
- Tool configuration
- LLM settings
"""

# Agent Configuration
AGENT_CONFIG = {
    "name": "TodoManager",
    "instructions": """You are a helpful and efficient Todo Manager assistant. Your role is to help users 
manage their tasks through a todo list application.

Your core responsibilities:
1. Add new todos - when users want to create tasks
2. View todos - when users ask to see their tasks
3. Complete todos - when users want to mark tasks as done
4. Delete todos - when users want to remove tasks
5. Provide statistics - when users want task summaries

Always:
- Be clear and friendly in your responses
- Confirm actions with specific details (ID, task name, priority)
- Use emojis for visual clarity (✅, 📋, 🔄, ❌)
- Search by task description if user doesn't provide ID
- Ask for clarification if the request is ambiguous

Example interactions:
- User: "Add a high priority task: write quarterly report"
  Response: "✅ Added 'write quarterly report' (HIGH priority) - ID: 1"
  
- User: "Show me my tasks"
  Response: "📋 You have 3 incomplete tasks:
           [1] write quarterly report (HIGH)
           [2] review code (NORMAL)
           [3] deploy app (LOW)"
           
- User: "Complete the report task"
  Response: "✅ Marked 'write quarterly report' as complete"
""",
}

# LLM Configuration
LLM_CONFIG = {
    # OpenAI models available:
    # - "gpt-4-turbo" - Most capable, higher cost
    # - "gpt-4" - Strong reasoning, higher cost
    # - "gpt-4-turbo-preview" - Latest preview model
    # - "gpt-3.5-turbo" - Fast, lower cost
    # 
    # For Ollama integration, use local LLM endpoint
    "model": "gpt-3.5-turbo",
    
    # Temperature controls randomness
    # 0.0 = deterministic (good for todos)
    # 1.0 = very random
    "temperature": 0.3,
    
    # Maximum tokens to generate per response
    "max_tokens": 1000,
}

# OpenAI API Configuration
OPENAI_CONFIG = {
    # Set OPENAI_API_KEY environment variable or pass in Agent creation
    "api_key": None,  # Will use environment variable OPENAI_API_KEY
    
    # For Ollama integration, use this endpoint:
    # "base_url": "http://localhost:11434/v1",
    
    "timeout": 30,  # Timeout for API requests in seconds
}

# Tool Configuration
TOOL_CONFIG = {
    # Maximum number of tool calls per response
    "max_tool_calls": 3,
    
    # Whether to use parallel tool execution
    "parallel_execution": True,
    
    # Timeout for tool execution
    "tool_timeout": 10,
}

# Agent behavior tuning
AGENT_BEHAVIOR = {
    # Maximum retries for failed tool calls
    "max_retries": 2,
    
    # Whether to explain reasoning
    "explain_reasoning": True,
    
    # Verbosity level: "quiet", "normal", "verbose"
    "verbosity": "normal",
}


def get_agent_instructions() -> str:
    """Get the agent instructions for initialization"""
    return AGENT_CONFIG["instructions"]


def get_model_name() -> str:
    """Get the LLM model name"""
    return LLM_CONFIG["model"]


def get_temperature() -> float:
    """Get the temperature setting"""
    return LLM_CONFIG["temperature"]


# Example configuration for using Ollama instead of OpenAI
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434/v1",  # Ollama endpoint
    "model": "mistral",                        # Model to use
    "api_key": "ollama",                       # Required but not used
    "temperature": 0.3,
}
