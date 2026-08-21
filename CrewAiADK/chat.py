"""
CrewAI Todo Manager - Interactive Chat Interface
UPDATED: Latest CrewAI patterns
Run: uv run python chat.py
"""
import os
import warnings
import logging

# Disable verbose logging for speed
warnings.filterwarnings('ignore')
logging.getLogger().setLevel(logging.ERROR)
os.environ['CREWAI_VERBOSE'] = '0'

from agent import process_user_input_async

async def chat():
    """Interactive chat loop with CrewAI todo manager."""
    print("\n" + "=" * 60)
    print("Todo Manager - CrewAI + Ollama (FREE)")
    print("=" * 60)
    print("✨ Using Ollama Qwen 2.5 (better function calling)")
    print("💡 Make sure you have qwen2.5: ollama pull qwen2.5\n")
    print("💡 TIP: Be explicit with commands for best results!\n")
    print("Examples:")
    print("  ✅ add task learn Python")
    print("  ✅ add buy groceries high priority")
    print("  ✅ show all tasks")
    print("  ✅ complete task 1")
    print("  ✅ show statistics")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("\nGoodbye!\n")
                break
            
            # Process with CrewAI async
            response = await process_user_input_async(user_input)
            print(f"\nAgent: {response}\n")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            print("Continuing chat...\n")
            # Continue chat even after errors

if __name__ == "__main__":
    import asyncio
    asyncio.run(chat())
