"""
OpenAI Agents SDK Tool Definitions for Todo Management

This module defines all tools available to the OpenAI agent.
In OpenAI SDK, tools are decorated with @function_tool and must return strings.

Tools available:
- add_todo: Create a new todo item
- get_todos: Retrieve incomplete todos
- complete_todo: Mark todo as complete by ID or description
- delete_todo: Delete a todo by ID
- get_stats: Get todo statistics
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import shared_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai.lib._pydantic import to_strict_json_schema
from agents import function_tool
from shared_utils import TodoStorage

# Initialize storage - todos.json in same folder as this file
storage = TodoStorage(filepath=str(Path(__file__).parent / "todos.json"))


@function_tool
def add_todo(task: str, priority: str = "normal") -> str:
    """
    Add a new todo item to the list.
    
    Use this tool when the user wants to create a new task.
    
    Args:
        task (str): The task description (required)
        priority (str): Priority level: "high", "normal", or "low" (default: normal)
    
    Returns:
        str: JSON string with result containing the new todo ID and confirmation
        Example: {"status": "created", "id": 1, "task": "Write report", "priority": "high"}
    
    Example Usage:
        agent: add_todo("Complete project proposal", "high")
        user: "Add a high priority task: write report"
    """
    result = storage.add_todo(task, priority)
    return json.dumps(result)


@function_tool
def get_todos(include_completed: bool = False) -> str:
    """
    Retrieve todo items from storage.
    
    By default, returns only incomplete todos. Set include_completed=True to see all.
    
    Args:
        include_completed (bool): If True, return all todos; if False, only incomplete ones
                                 (default: False)
    
    Returns:
        str: JSON string with list of todo items with details
        Example:
        {
            "todos": [
                {
                    "id": 1,
                    "task": "Write report",
                    "priority": "high",
                    "created_at": "2026-08-20T10:30:00",
                    "is_completed": false
                }
            ]
        }
    
    Example Usage:
        agent: get_todos()  # Get incomplete todos
        user: "Show me my tasks"
    """
    todos = storage.get_todos(include_completed)
    return json.dumps({"todos": todos})


@function_tool
def complete_todo(todo_id: int = None, description: str = None) -> str:
    """
    Mark a todo item as complete.
    
    Can search by either todo_id OR description. The agent will choose the best approach.
    
    Args:
        todo_id (int, optional): The numeric ID of the todo (used if exact ID known)
        description (str, optional): Search for todo containing this text (case-insensitive)
    
    Returns:
        str: JSON string with confirmation of completion or error message
        Success: {"status": "completed", "id": 1, "task": "Write report", "completed_at": "..."}
        Error: {"status": "error", "message": "Todo not found"}
    
    Example Usage:
        agent: complete_todo(todo_id=1)           # Complete by ID
        agent: complete_todo(description="report") # Complete by text match
        user: "Mark the report writing task as done"
    """
    result = storage.complete_todo(todo_id, description)
    return json.dumps(result)


@function_tool
def delete_todo(todo_id: int) -> str:
    """
    Delete a todo item permanently.
    
    Use this when the user wants to remove a task from the list.
    
    Args:
        todo_id (int): The ID of the todo to delete (required)
    
    Returns:
        str: JSON string with confirmation of deletion or error message
        Success: {"status": "deleted", "id": 1}
        Error: {"status": "error", "message": "Todo not found"}
    
    Example Usage:
        agent: delete_todo(1)
        user: "Remove task number 1 from my list"
    """
    result = storage.delete_todo(todo_id)
    return json.dumps(result)


@function_tool
def get_stats() -> str:
    """
    Get statistics about todos.
    
    Provides a summary of how many todos are completed, pending, and their priorities.
    
    Returns:
        str: JSON string with statistics dictionary
        Example:
        {
            "total": 10,
            "completed": 3,
            "incomplete": 7,
            "high_priority": 2,
            "normal_priority": 5,
            "low_priority": 3
        }
    
    Example Usage:
        agent: get_stats()
        user: "Give me a summary of my tasks"
    """
    stats = storage.get_stats()
    return json.dumps(stats)
