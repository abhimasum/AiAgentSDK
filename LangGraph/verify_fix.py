"""
Simple verification test for LangGraph agent anti-hallucination fix
"""

import asyncio
import os
from agent import TodoAgent
from shared_utils.todo_storage import TodoStorage


async def verify_agent():
    """Verify agent behavior with clean storage"""
    
    # Clean up
    if os.path.exists("todos.json"):
        os.remove("todos.json")
    
    print("=" * 70)
    print("🧪 LangGraph Anti-Hallucination Verification")
    print("=" * 70)
    
    agent = TodoAgent()
    
    # Test 1: List when empty
    print("\n[Test 1] Ask for tasks when storage is empty")
    print("User: List my tasks")
    response = await agent.run("List my tasks")
    print(f"Agent: {response}")
    
    # Verify storage is actually empty
    storage = TodoStorage()
    todos = storage.get_todos()
    print(f"✓ Actual storage has {len(todos)} tasks")
    
    # Test 2: Add a real task
    print("\n[Test 2] Add a real task")
    print("User: Add task: buy milk")
    response = await agent.run("Add task: buy milk")
    print(f"Agent: {response}")
    
    # Verify it was added
    todos = storage.get_todos()
    print(f"✓ Actual storage now has {len(todos)} tasks")
    if todos:
        print(f"  - Task 1: {todos[0]['task']}")
    
    # Test 3: List existing tasks
    print("\n[Test 3] List existing tasks")
    print("User: What tasks do I have?")
    response = await agent.run("What tasks do I have?")
    print(f"Agent: {response}")
    
    # Test 4: Try to complete non-existent task
    print("\n[Test 4] Try to complete non-existent task")
    print("User: Complete task: write report")
    response = await agent.run("Complete task: write report")
    print(f"Agent: {response}")
    
    # Test 5: Complete actual task
    print("\n[Test 5] Complete actual task")
    print("User: Complete buy milk")
    response = await agent.run("Complete buy milk")
    print(f"Agent: {response}")
    
    # Verify completion
    todos = storage.get_todos()
    completed = storage.get_todos(include_completed=True)
    print(f"✓ Incomplete: {len(todos)}, Total: {len(completed)}")
    
    # Test 6: Add another task and list all
    print("\n[Test 6] Add task and list all")
    print("User: Add task: clean house")
    response = await agent.run("Add task: clean house")
    print(f"Agent: {response}")
    
    print("User: Show all my tasks including completed")
    response = await agent.run("Show all my tasks including completed")
    print(f"Agent: {response}")
    
    # Final verification
    all_todos = storage.get_todos(include_completed=True)
    print(f"\n✓ Final verification: {len(all_todos)} tasks in storage")
    for todo in all_todos:
        status = "✓" if todo["is_completed"] else "○"
        print(f"  {status} #{todo['id']}: {todo['task']}")
    
    print("\n" + "=" * 70)
    print("✅ Verification complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(verify_agent())
