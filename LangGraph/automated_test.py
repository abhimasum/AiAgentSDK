"""
Automated Test Suite for LangGraph Todo Agent

This script tests all agent capabilities:
1. Add todos (default, high, low priority)
2. List todos
3. Complete todos (by description)
4. Delete todos
5. Get statistics

Run: uv run python automated_test.py
"""

import asyncio
from agent import TodoAgent
from shared_utils.todo_storage import TodoStorage
import os


async def test_agent():
    """Run comprehensive test suite"""
    
    # Clean up any existing todos
    if os.path.exists("todos.json"):
        os.remove("todos.json")
    
    print("=" * 60)
    print("🧪 LangGraph Todo Agent - Automated Test Suite")
    print("=" * 60)
    
    agent = TodoAgent()
    
    # Test 1: Add todo (default priority)
    print("\n[Test 1] Add todo with default priority")
    response = await agent.run("Add task: learn python")
    print(f"✓ Response: {response}")
    
    # Test 2: Add todo (high priority)
    print("\n[Test 2] Add todo with high priority")
    response = await agent.run("Add task: exercise with high priority")
    print(f"✓ Response: {response}")
    
    # Test 3: Add todo (low priority)
    print("\n[Test 3] Add todo with low priority")
    response = await agent.run("Add task: read book with low priority")
    print(f"✓ Response: {response}")
    
    # Test 4: List todos
    print("\n[Test 4] List all incomplete todos")
    response = await agent.run("Show my tasks")
    print(f"✓ Response: {response}")
    
    # Test 5: Complete todo by description
    print("\n[Test 5] Complete todo by description")
    response = await agent.run("Mark learn python as done")
    print(f"✓ Response: {response}")
    
    # Test 6: Get statistics
    print("\n[Test 6] Get todo statistics")
    response = await agent.run("How many tasks do I have?")
    print(f"✓ Response: {response}")
    
    # Test 7: Complete another todo
    print("\n[Test 7] Complete todo by partial match")
    response = await agent.run("Complete exercise")
    print(f"✓ Response: {response}")
    
    # Test 8: List todos again
    print("\n[Test 8] List remaining todos")
    response = await agent.run("What tasks are left?")
    print(f"✓ Response: {response}")
    
    # Test 9: Delete todo
    print("\n[Test 9] Delete a todo")
    response = await agent.run("Delete todo #3")
    print(f"✓ Response: {response}")
    
    # Test 10: Final statistics
    print("\n[Test 10] Final statistics")
    response = await agent.run("Show me the stats")
    print(f"✓ Response: {response}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    
    # Display final storage state
    print("\n📋 Final todos.json content:")
    storage = TodoStorage()
    todos = storage.get_todos(include_completed=True)
    for todo in todos:
        status = "✓" if todo["is_completed"] else "○"
        print(f"  {status} #{todo['id']}: {todo['task']} [{todo['priority']}]")


if __name__ == "__main__":
    asyncio.run(test_agent())
