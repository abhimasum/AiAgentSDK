"""
Simple test to verify tool execution
"""

import asyncio
import os
from agent import TodoAgent
from todo_storage import TodoStorage


async def simple_test():
    """Simple focused test"""
    
    # Clean up
    if os.path.exists("todos.json"):
        os.remove("todos.json")
    
    print("=" * 70)
    print("🧪 Simple LangGraph Test with Mistral")
    print("=" * 70)
    
    agent = TodoAgent()
    storage = TodoStorage()
    
    # Test 1: Add a task
    print("\n[Test 1] Add task: buy milk")
    response = await agent.run("Add task: buy milk")
    print(f"Agent response:\n{response}\n")
    
    # Check storage directly
    todos = storage.get_todos()
    print(f"Storage check: {len(todos)} tasks")
    if todos:
        for todo in todos:
            print(f"  - #{todo['id']}: {todo['task']}")
    else:
        print("  ⚠️ Storage is EMPTY (tool didn't execute!)")
    
    # Test 2: List tasks
    print("\n[Test 2] List tasks")
    response = await agent.run("List my tasks")
    print(f"Agent response:\n{response}\n")
    
    # Final check
    print("\n" + "=" * 70)
    print(f"Final storage: {len(storage.get_todos(include_completed=True))} total tasks")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(simple_test())
