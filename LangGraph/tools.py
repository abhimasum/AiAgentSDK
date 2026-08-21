"""
LangGraph Tool Definitions

This module defines tools (functions) that the LangGraph agent can call.
Tools are the agent's way of interacting with the external world.

LangGraph Tool Pattern:
1. Define regular Python functions
2. Use type hints (LangGraph extracts these for schemas)
3. Write detailed docstrings (LLM reads these to understand tool purpose)
4. Return structured data (dictionaries or strings)

How LangGraph Binds Tools:
- tools are passed to the LLM via .bind_tools(tools)
- LLM receives tool schemas (name, description, parameters)
- LLM decides which tool to call based on user input
- LangGraph routes tool calls back to these functions
"""

from typing import Optional
from todo_storage import TodoStorage


def add_todo(task: str, priority: str = "normal", description: str = "") -> dict:
    """Add a new todo item to the list.
    
    Use this tool when the user wants to add a new task, create a todo, or remember something to do.
    
    Args:
        task: Brief description of the task (required)
        priority: Priority level - must be 'low', 'normal', or 'high' (default: normal)
        description: Optional extended description or notes
    """
    storage = TodoStorage()
    result = storage.add_todo(task, priority, description)
    return result


def get_todos(include_completed: bool = False) -> list:
    """Retrieve all todos from the list.
    
    Use this tool when the user wants to see their tasks, list todos, view what's on their list, or check what they need to do.
    
    Args:
        include_completed: If True, shows all todos including completed ones. If False, shows only incomplete todos (default)
    """
    storage = TodoStorage()
    result = storage.get_todos(include_completed)
    return result


def complete_todo(todo_id: Optional[int] = None, description: Optional[str] = None) -> dict:
    """Mark a todo as complete.
    
    Use this tool when the user wants to mark a task as done, complete a todo, or check off an item.
    You can complete by exact ID (todo_id=5) or by description search (description='report' finds first todo containing 'report').
    
    Args:
        todo_id: Exact ID of the todo to complete
        description: Search string to match in task description (case-insensitive substring match)
    """
    storage = TodoStorage()
    result = storage.complete_todo(todo_id, description)
    return result


def delete_todo(todo_id: int) -> dict:
    """Permanently delete a todo from the list.
    
    Use this tool when the user wants to remove a task, delete a todo, or get rid of an item.
    
    Args:
        todo_id: ID of the todo to delete (required)
    """
    storage = TodoStorage()
    result = storage.delete_todo(todo_id)
    return result


def get_todo_stats() -> dict:
    """Get statistics about todos including counts by status and priority.
    
    Use this tool when the user wants to see todo statistics, get an overview, or check how many tasks they have.
    """
    storage = TodoStorage()
    result = storage.get_stats()
    return result


# Export all tools as a list for easy binding
TOOLS = [add_todo, get_todos, complete_todo, delete_todo, get_todo_stats]
