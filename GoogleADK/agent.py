"""
Google ADK Todo Manager - All-in-One
Run: adk web agent.py (or: adk run agent.py "your query")
Uses Ollama locally - No API key needed!
Make sure Ollama is running: ollama serve
"""
import sys
from pathlib import Path

# Add shared_utils to path
sys.path.append(str(Path(__file__).parent.parent))
from shared_utils.todo_storage import TodoStorage

# Storage
storage = TodoStorage(filepath=str(Path(__file__).parent / "todos.json"))

# Tools - Plain Python functions
def add_todo(task: str, priority: str = "medium") -> str:
    """Add a new todo task."""
    todo_id = storage.add_todo(task, priority=priority)
    return f"✓ Added task #{todo_id}: {task} (priority: {priority})"

def get_todos(include_completed: bool = False) -> str:
    """Get all todos."""
    todos = storage.get_todos(include_completed=include_completed)
    if not todos:
        return "No tasks found."
    result = f"📋 {len(todos)} tasks:\n"
    for t in todos:
        status = "✓" if t["is_completed"] else "○"
        result += f"{status} #{t['id']}: {t['task']} [{t['priority']}]\n"
    return result

def complete_todo(todo_id: int) -> str:
    """Mark a todo as complete."""
    return f"✓ Task #{todo_id} complete!" if storage.complete_todo(todo_id) else f"✗ Task #{todo_id} not found."

def delete_todo(todo_id: int) -> str:
    """Delete a todo."""
    return f"✓ Deleted task #{todo_id}" if storage.delete_todo(todo_id) else f"✗ Task #{todo_id} not found."

def get_stats() -> str:
    """Get todo statistics."""
    s = storage.get_stats()
    return f"📊 Total: {s['total']}, Done: {s['completed']}, Pending: {s['incomplete']}, High: {s.get('high_priority', 0)}, Normal: {s.get('normal_priority', 0)}, Low: {s.get('low_priority', 0)}"

# Agent Definition
from google.adk import Agent

root_agent = Agent(
    name="TodoManager",
    model="ollama_chat/llama3.2",  # Recommended: llama3.2 (fast), qwen2.5 (more accurate but slower)
    instruction="""You are a helpful todo assistant. When users ask about their tasks, USE THE TOOLS to get real data.
    
IMPORTANT: Always call the appropriate tool functions to get actual data:
    - When asked to show/list tasks: call get_todos() to fetch from storage
    - When asked to add a task: call add_todo() with the task details
    - When asked about statistics: call get_stats() to get real numbers
    - When asked to complete a task: call complete_todo() with the task ID
    - When asked to delete a task: call delete_todo() with the task ID
    
    Do NOT just explain what the tools do - actually use them to help the user!""",
    tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats],
)
