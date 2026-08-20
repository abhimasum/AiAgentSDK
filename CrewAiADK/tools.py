"""
CrewAI Tool Definitions for Todo Management

This module defines all tools available to the CrewAI agent.
Each tool is a function that the agent can autonomously call based on user intent.

Tools available:
- add_todo: Create a new todo item
- get_todos: Retrieve incomplete todos
- complete_todo: Mark todo as complete by ID or description
- delete_todo: Delete a todo by ID
- get_stats: Get todo statistics
"""

import sys
from pathlib import Path

# Add parent directory to path to import shared_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai_tools import tool
from shared_utils import TodoStorage

# Initialize storage - todos.json in same folder as this file
storage = TodoStorage(filepath=str(Path(__file__).parent / "todos.json"))


@tool
def add_todo(task: str, priority: str = "normal") -> dict:
    """
    Add a new todo item to the list.
    
    Use this tool when the user wants to create a new task.
    
    Args:
        task (str): The task description (required)
        priority (str): Priority level: "high", "normal", or "low" (default: normal)
    
    Returns:
        dict: Result containing the new todo ID and confirmation
        Example: {"status": "created", "id": 1, "task": "Write report", "priority": "high"}
    
    Example Usage:
        agent: add_todo("Complete project proposal", "high")
        user: "Add a high priority task: write report"
    """
    return storage.add_todo(task, priority)


@tool
def get_todos(include_completed: bool = False) -> list:
    """
    Retrieve todo items from storage.
    
    By default, returns only incomplete todos. Set include_completed=True to see all.
    
    Args:
        include_completed (bool): If True, return all todos; if False, only incomplete ones
                                 (default: False)
    
    Returns:
        list: List of todo items with details
        Example:
        [
            {
                "id": 1,
                "task": "Write report",
                "priority": "high",
                "created_at": "2026-08-20T10:30:00",
                "is_completed": false
            },
            {
                "id": 2,
                "task": "Review code",
                "priority": "normal",
                "created_at": "2026-08-20T11:00:00",
                "is_completed": false
            }
        ]
    
    Example Usage:
        agent: get_todos()  # Get incomplete todos
        user: "Show me my tasks"
    """
    return storage.get_todos(include_completed)


@tool
def complete_todo(todo_id: int = None, description: str = None) -> dict:
    """
    Mark a todo item as complete.
    
    Can search by either todo_id OR description. The agent will choose the best approach.
    
    Args:
        todo_id (int, optional): The numeric ID of the todo (used if exact ID known)
        description (str, optional): Search for todo containing this text (case-insensitive)
    
    Returns:
        dict: Confirmation of completion or error message
        Success: {"status": "completed", "id": 1, "task": "Write report", "completed_at": "..."}
        Error: {"status": "error", "message": "Todo not found"}
    
    Example Usage:
        agent: complete_todo(todo_id=1)           # Complete by ID
        agent: complete_todo(description="report") # Complete by text match
        user: "Mark the report writing task as done"
    """
    return storage.complete_todo(todo_id, description)


@tool
def delete_todo(todo_id: int) -> dict:
    """
    Delete a todo item permanently.
    
    Use this when the user wants to remove a task from the list.
    
    Args:
        todo_id (int): The ID of the todo to delete (required)
    
    Returns:
        dict: Confirmation of deletion or error message
        Success: {"status": "deleted", "id": 1}
        Error: {"status": "error", "message": "Todo not found"}
    
    Example Usage:
        agent: delete_todo(1)
        user: "Remove task number 1 from my list"
    """
    return storage.delete_todo(todo_id)


@tool
def get_stats() -> dict:
    """
    Get statistics about todos.
    
    Provides a summary of how many todos are completed, pending, and their priorities.
    
    Returns:
        dict: Statistics dictionary
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
    return storage.get_stats()
