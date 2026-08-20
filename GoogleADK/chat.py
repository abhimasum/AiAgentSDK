"""
Simple CLI Chat with Google ADK Todo Manager
Just run: uv run python chat.py
"""
import asyncio
import warnings
import logging
import os

# Disable verbose logging for faster performance
warnings.filterwarnings('ignore')  # Suppress UserWarnings
logging.getLogger().setLevel(logging.ERROR)  # Only show errors
os.environ['LITELLM_LOG'] = 'ERROR'  # Disable LiteLLM info logs

from agent import root_agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService

async def chat():
    print("\n" + "=" * 60)
    print("Todo Manager - Chat Interface")
    print("=" * 60)
    print("Ask me anything about your todos!")
    print("Examples:")
    print("  - can you give me all todo list")
    print("  - add a task to buy groceries")
    print("  - mark task 1 as complete")
    print("  - give me statistics")
    print("\nType 'quit' or press Ctrl+C to exit\n")
    
    # Create runner with required services
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="TodoManager",
        session_service=session_service
    )
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q', 'bye', 'goodbye']:
                print("\nGoodbye!\n")
                break
            
            # Run the agent with run_debug (awaitable) - quiet mode for speed
            events = await runner.run_debug(user_input, quiet=True, verbose=False)
            
            # Extract the final text response from events
            # Events structure: function_call -> function_response -> final text
            final_response = None
            for event in events:
                if hasattr(event, 'content') and event.content:
                    # Check if this event has parts with text
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            # Look for text responses (not function calls/responses)
                            if hasattr(part, 'text') and part.text:
                                final_response = part.text.strip()
            
            if final_response:
                print(f"\nAgent: {final_response}\n")
            else:
                print("\nAgent: Done.\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except EOFError:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    asyncio.run(chat())
