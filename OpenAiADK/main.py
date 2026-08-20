"""
OpenAI Agents SDK Todo Manager

This module implements a Todo Management Agent using the OpenAI Agents SDK.
The agent understands user requests and uses available tools to manage todos.

Key Differences from CrewAI:
- Simpler, more direct orchestration
- Tool-based composition (agents as tools)
- No task definitions needed
- Easier to understand for simple workflows

LLM Integration:
- Can use OpenAI models (gpt-4, gpt-3.5-turbo)
- Can use Ollama for local inference
- Set OPENAI_API_KEY environment variable for OpenAI
"""

import os
import json
from pathlib import Path

# Import from OpenAI Agents SDK
from agents import Agent, Runner
from agents.extensions.visualization import draw_graph

# Import configuration
from config import get_agent_instructions, get_model_name, get_temperature, OPENAI_CONFIG

# Import tools
from tools import add_todo, get_todos, complete_todo, delete_todo, get_stats


def create_todo_agent() -> Agent:
    """
    Create the Todo Manager Agent for OpenAI SDK.
    
    Architecture:
    - Agent: Single AI agent with name and instructions
    - Tools: List of functions the agent can call
    - Model: Which LLM to use
    - No task layer needed (simpler than CrewAI)
    
    Returns:
        Agent: Configured agent with all tools
    
    Example:
        agent = create_todo_agent()
        result = await Runner.run(agent, "Add task: write report")
    """
    
    # Create agent with tools
    agent = Agent(
        name="TodoManager",                          # Agent name
        instructions=get_agent_instructions(),       # System prompt
        model=get_model_name(),                      # LLM model
        tools=[                                      # Available tools
            add_todo,
            get_todos,
            complete_todo,
            delete_todo,
            get_stats
        ],
        # Optional: Set temperature for more/less determinism
        model_settings={
            "temperature": get_temperature(),
            "max_tokens": 1000,
        }
    )
    
    return agent


def format_response(response: str) -> str:
    """
    Format agent response for better readability.
    
    Args:
        response (str): Raw response from agent
    
    Returns:
        str: Formatted response with better structure
    """
    # Try to parse as JSON for structured responses
    try:
        data = json.loads(response)
        if isinstance(data, dict):
            # Format JSON response nicely
            return json.dumps(data, indent=2)
    except (json.JSONDecodeError, TypeError):
        # Not JSON, return as is
        pass
    
    return response


def main():
    """
    Main entry point for OpenAI Todo Agent.
    
    This function:
    1. Creates the agent
    2. Handles user input in a loop
    3. Runs agent with user requests
    4. Displays results
    
    Prerequisites:
    - OPENAI_API_KEY environment variable set
      OR
    - Ollama running on localhost:11434 with appropriate config
    
    Example Interactions:
    - "Add a task: write quarterly report"
    - "Show me my incomplete tasks"
    - "Mark the report task as done"
    - "How many tasks do I have?"
    - "Delete task 1"
    """
    
    # Display welcome message
    print("=" * 70)
    print("🤖 OpenAI Agents SDK Todo Manager")
    print("=" * 70)
    print("\nWelcome! I'm your AI-powered todo assistant.")
    print("\nWhat I can do:")
    print("  📝 Add tasks:       'Add a high priority task: write report'")
    print("  📋 List tasks:      'Show my incomplete tasks'")
    print("  ✅ Complete tasks:  'Mark the report as done' or 'Complete task 1'")
    print("  🔍 Search:          'Find tasks about project'")
    print("  📊 Get stats:       'How many tasks do I have?'")
    print("  🗑️  Delete tasks:    'Remove task 1'")
    print("\nType 'quit' to exit, 'help' for more commands.")
    print("=" * 70)
    
    try:
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            print("\n⚠️  WARNING: OPENAI_API_KEY not set")
            print("If using OpenAI: set the environment variable first")
            print("If using Ollama: make sure it's running on localhost:11434\n")
        
        # Create the agent
        print("\n🔄 Initializing agent...")
        agent = create_todo_agent()
        print("✅ Agent ready!\n")
        
        # Main interaction loop
        while True:
            try:
                # Get user input
                user_input = input("\n📝 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ["quit", "exit", "bye", "q"]:
                    print("\n👋 Goodbye! Your todos have been saved.")
                    break
                
                if user_input.lower() in ["help", "h", "?"]:
                    print("\n📚 Available Commands:")
                    print("  - Add task: 'Add task: <description> with <priority> priority'")
                    print("  - List: 'Show my tasks' or 'What's on my list?'")
                    print("  - Complete: 'Complete task <id>' or 'Mark <description> as done'")
                    print("  - Delete: 'Delete task <id>'")
                    print("  - Stats: 'Summary' or 'How many tasks?'")
                    continue
                
                if not user_input:
                    print("Please enter a command or type 'help' for options.")
                    continue
                
                # Run the agent with user input
                print("\n🔄 Processing...\n")
                
                # Runner.run is the main way to execute an agent
                # It handles the full orchestration
                result = Runner.run(agent, user_input)
                
                # Display response
                print(f"🤖 Agent: {result.final_output}")
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.")
    
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {str(e)}")
        print("\nMake sure:")
        print("1. OPENAI_API_KEY is set (for OpenAI models)")
        print("2. OR Ollama is running (ollama serve)")
    
    except ImportError as e:
        print(f"\n❌ Import Error: {str(e)}")
        print("\nMake sure to install dependencies:")
        print("  pip install -r requirements.txt")
        print("  OR")
        print("  uv sync")
    
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
