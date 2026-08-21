"""
LangGraph Tool Definitions

This module defines tools (functions) that the LangGraph agent can call.
Tools are the agent's way of interacting with the external world.

LangGraph Tool Pattern:
1. Define regular Python functions
2. Use type hints (LangGraph extracts these for schemas)
3. Write detailed docstrings (LLM reads these to understand tool purpose)
4. Return FORMATTED STRINGS (easier for small LLMs to parse than complex dicts)

How LangGraph Binds Tools:
- tools are passed to the LLM via .bind_tools(tools)
- LLM receives tool schemas (name, description, parameters)
- LLM decides which tool to call based on user input
- LangGraph routes tool calls back to these functions
"""

from typing import Optional
from shared_utils.todo_storage import TodoStorage


def add_todo(task: str, priority: str = "normal", description: str = "") -> str:
    """Add a NEW todo item. Use this ONLY when user wants to ADD or CREATE a new task.
    
    Use keywords: 'add', 'create', 'new task'. DO NOT use if user says 'complete', 'done', or 'finish'.
    
    Args:
        task: Brief description of the task (required)
        priority: Priority level - must be 'low', 'normal', or 'high' (default: normal)
        description: Optional extended description or notes
    """
    storage = TodoStorage()
    result = storage.add_todo(task, priority, description)
    # Return formatted string for LLM
    return f"✅ Added task #{result['id']}: {result['task']} (priority: {result['priority']})"


def get_todos(include_completed: bool = False) -> str:
    """Retrieve all todos from the list. ALWAYS call this to see tasks - do NOT make up task data.
    
    When user asks questions like: 'show tasks', 'list todos', 'what tasks do I have', call this tool FIRST before answering.
    
    Args:
        include_completed: If True, shows all todos including completed ones. If False, shows only incomplete todos (default)
    """
    storage = TodoStorage()
    todos = storage.get_todos(include_completed)
    
    # Format as human-readable string
    if not todos:
        return "📋 You have NO tasks."
    
    lines = [f"📋 You have {len(todos)} task(s):"]
    for todo in todos:
        status = "✅" if todo['is_completed'] else "○"
        priority_icon = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(todo['priority'], "○")
        lines.append(f"  {status} #{todo['id']}: {todo['task']} {priority_icon}")
    
    return "\n".join(lines)


def complete_todo(todo_id: Optional[int] = None, description: Optional[str] = None) -> str:
    """Mark an EXISTING todo as complete. Use this when user says 'complete', 'done', 'finish', or 'mark as done'.
    
    DO NOT call add_todo if user says 'complete'. Call complete_todo instead.
    Examples: 'complete buy milk', 'mark task 1 as done', 'finish the report task'
    
    Args:
        todo_id: Exact ID of the todo to complete
        description: Search string to match in task description (case-insensitive substring match)
    """
    storage = TodoStorage()
    result = storage.complete_todo(todo_id, description)
    
    # Format response
    if result['status'] == 'completed':
        return f"✅ Completed task #{result['id']}: {result['task']}"
    elif result['status'] == 'already_completed':
        return f"ℹ️ Task #{result['id']}: {result['task']} was already completed"
    else:
        return f"❌ Error: {result['message']}"


def delete_todo(todo_id: int) -> str:
    """Permanently delete a todo from the list.
    
    Use this tool when the user wants to remove a task, delete a todo, or get rid of an item.
    
    Args:
        todo_id: ID of the todo to delete (required)
    """
    storage = TodoStorage()
    result = storage.delete_todo(todo_id)
    
    if result['status'] == 'deleted':
        return f"🗑️ Deleted task #{result['id']}"
    else:
        return f"❌ Error: {result['message']}"


def get_todo_stats() -> str:
    """Get statistics about todos including counts by status and priority.
    
    Use this tool when the user wants to see todo statistics, get an overview, or check how many tasks they have.
    """
    storage = TodoStorage()
    stats = storage.get_stats()
    
    return f"""📊 Todo Statistics:
  • Total: {stats['total']} tasks
  • Completed: {stats['completed']}
  • Incomplete: {stats['incomplete']}
  • High priority: {stats['high_priority']}
  • Normal priority: {stats['normal_priority']}
  • Low priority: {stats['low_priority']}"""


# Export all tools as a list for easy binding
TOOLS = [add_todo, get_todos, complete_todo, delete_todo, get_todo_stats]
