"""
OpenAI Todo Manager - Interactive Chat Interface with Ollama
UPDATED: Using Ollama (free, local) - No API key needed!
Run: uv run python chat.py
"""
import os
import warnings
import logging
import json

# Disable verbose logging for speed
warnings.filterwarnings('ignore')
logging.getLogger().setLevel(logging.ERROR)

from agent import client, TOOLS, FUNCTION_MAP, process_tool_call

async def chat():
    """Interactive chat loop with todo manager."""
    print("\n" + "=" * 60)
    print("Todo Manager - OpenAI SDK + Ollama (FREE)")
    print("=" * 60)
    print("✨ Using Ollama Llama 3.2 (local, no API key needed!)")
    print("\nAsk me anything about your todos!")
    print("Examples:")
    print("  - show me all my tasks")
    print("  - add a task to learn Python")
    print("  - mark task 1 as complete")
    print("  - give me statistics")
    print("\nType 'quit' to exit\n")
    
    conversation_history = []
    system_message = """You are a helpful todo assistant. When users ask about their tasks:
    
1. Use the available tools to manage todos
2. ALWAYS call the appropriate function to get real data
3. Format responses clearly and helpfully
4. When listing tasks, show all results from get_todos()
5. Be direct and concise

Available tools: add_todo, get_todos, complete_todo, delete_todo, get_stats"""
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("\nGoodbye!\n")
                break
            
            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Call Ollama via OpenAI-compatible API (SDK v3.3+)
            response = client.chat.completions.create(
                model="llama3.2",  # Using Ollama's Llama 3.2 model (2GB, fast)
                messages=[{"role": "system", "content": system_message}] + conversation_history,
                tools=TOOLS,
                tool_choice="auto"
            )
            
            # Process response
            assistant_message = response.choices[0].message
            
            # Handle tool calls
            if assistant_message.tool_calls:
                conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Process each tool call
                for tool_call in assistant_message.tool_calls:
                    try:
                        # Safely parse arguments
                        tool_args = json.loads(tool_call.function.arguments)
                        tool_result = process_tool_call(
                            tool_call.function.name,
                            tool_args
                        )
                    except json.JSONDecodeError as e:
                        tool_result = json.dumps({"error": f"Invalid JSON arguments: {str(e)}"})
                    
                    conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                
                # Get final response after tool calls
                final_response = client.chat.completions.create(
                    model="llama3.2",  # Using Ollama's Llama 3.2
                    messages=[{"role": "system", "content": system_message}] + conversation_history,
                    tools=TOOLS,
                    tool_choice="none"  # Don't call tools again
                )
                
                final_message = final_response.choices[0].message.content
                print(f"\nAgent: {final_message}\n")
                
                conversation_history.append({
                    "role": "assistant",
                    "content": final_message
                })
            else:
                # Direct response without tools
                response_text = assistant_message.content or "I'm not sure how to help with that."
                print(f"\nAgent: {response_text}\n")
                
                conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            # Continue chat even after errors

if __name__ == "__main__":
    import asyncio
    asyncio.run(chat())
