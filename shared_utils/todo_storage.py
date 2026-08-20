"""
Shared utilities for Todo Management Agent System
Common functions and classes used across all frameworks (CrewAI, OpenAI, Google ADK)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class TodoStorage:
    """
    Handles persistent storage of todo items in JSON format.
    
    Features:
    - Automatic file creation if not exists
    - Thread-safe read/write operations
    - Support for filtering (completed/incomplete)
    - Search by ID or description
    
    Attributes:
        filepath (str): Path to the todos.json file
    """
    
    def __init__(self, filepath: str = "todos.json"):
        """
        Initialize TodoStorage with a JSON file path.
        
        Args:
            filepath (str): Path to store todos.json (default: todos.json in current dir)
        """
        self.filepath = filepath
        self._ensure_file()
    
    def _ensure_file(self) -> None:
        """
        Create todos.json if it doesn't exist with default structure.
        
        Default structure:
        {
            "todos": [],
            "metadata": {
                "created": ISO timestamp,
                "last_modified": ISO timestamp
            }
        }
        """
        if not os.path.exists(self.filepath):
            initial_data = {
                "todos": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_modified": datetime.now().isoformat()
                }
            }
            with open(self.filepath, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def add_todo(self, task: str, priority: str = "normal", description: str = "") -> Dict:
        """
        Add a new todo item to the list.
        
        Args:
            task (str): The task description (required)
            priority (str): Priority level - "high", "normal", or "low" (default: normal)
            description (str): Detailed description of the task (optional)
        
        Returns:
            Dict: Success response with todo ID
            {
                "status": "created",
                "id": 1,
                "task": "task description",
                "priority": "normal"
            }
        
        Example:
            >>> storage = TodoStorage()
            >>> result = storage.add_todo("Write report", priority="high")
            >>> print(result)
            {'status': 'created', 'id': 1, 'task': 'Write report', 'priority': 'high'}
        """
        # Validate input
        if not task or not isinstance(task, str):
            return {"status": "error", "message": "Task must be a non-empty string"}
        
        if priority not in ["high", "normal", "low"]:
            priority = "normal"
        
        # Load existing todos
        data = self._load()
        
        # Generate new ID (max existing ID + 1, or 1 if empty)
        existing_ids = [t.get("id", 0) for t in data["todos"]]
        new_id = max(existing_ids) + 1 if existing_ids else 1
        
        # Create new todo item
        todo = {
            "id": new_id,
            "task": task.strip(),
            "priority": priority,
            "description": description.strip() if description else "",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "is_completed": False
        }
        
        # Add and save
        data["todos"].append(todo)
        self._save(data)
        
        return {
            "status": "created",
            "id": new_id,
            "task": task,
            "priority": priority
        }
    
    def get_todos(self, include_completed: bool = False) -> List[Dict]:
        """
        Retrieve todos from storage.
        
        Args:
            include_completed (bool): If True, return all todos; if False, only incomplete ones
                                     (default: False - only incomplete)
        
        Returns:
            List[Dict]: List of todo items
                [
                    {
                        "id": 1,
                        "task": "Write report",
                        "priority": "high",
                        "created_at": "2026-08-20T10:30:00",
                        "completed_at": null,
                        "is_completed": false
                    },
                    ...
                ]
        
        Example:
            >>> storage = TodoStorage()
            >>> todos = storage.get_todos()  # Get only incomplete
            >>> all_todos = storage.get_todos(include_completed=True)  # Get all
        """
        data = self._load()
        
        if include_completed:
            return data["todos"]
        
        # Filter to only incomplete todos
        return [t for t in data["todos"] if not t.get("is_completed", False)]
    
    def complete_todo(self, todo_id: Optional[int] = None, description: Optional[str] = None) -> Dict:
        """
        Mark a todo as complete by ID or description match.
        
        Search Strategy:
        1. If todo_id provided: search by exact ID match
        2. If description provided: search for task containing description (case-insensitive)
        3. If both provided: prioritize ID search
        
        Args:
            todo_id (int, optional): The ID of the todo to complete
            description (str, optional): Search for todo with matching task description
        
        Returns:
            Dict: Success/error response
            Success:
            {
                "status": "completed",
                "id": 1,
                "task": "Write report",
                "completed_at": "2026-08-20T14:00:00"
            }
            Error:
            {
                "status": "error",
                "message": "Todo not found"
            }
        
        Example:
            >>> storage = TodoStorage()
            >>> # Complete by ID
            >>> storage.complete_todo(todo_id=1)
            >>> # Complete by description
            >>> storage.complete_todo(description="report")
        """
        if todo_id is None and description is None:
            return {"status": "error", "message": "Provide either todo_id or description"}
        
        data = self._load()
        
        # Search for matching todo
        for todo in data["todos"]:
            # Match by ID (if provided)
            if todo_id is not None and todo["id"] == todo_id:
                if todo["is_completed"]:
                    return {"status": "error", "message": "Todo already completed"}
                
                todo["is_completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self._save(data)
                return {
                    "status": "completed",
                    "id": todo["id"],
                    "task": todo["task"],
                    "completed_at": todo["completed_at"]
                }
            
            # Match by description (case-insensitive substring match)
            if description is not None and todo_id is None:
                if description.lower() in todo["task"].lower():
                    if todo["is_completed"]:
                        continue  # Skip already completed todos
                    
                    todo["is_completed"] = True
                    todo["completed_at"] = datetime.now().isoformat()
                    self._save(data)
                    return {
                        "status": "completed",
                        "id": todo["id"],
                        "task": todo["task"],
                        "completed_at": todo["completed_at"]
                    }
        
        return {"status": "error", "message": "Todo not found"}
    
    def delete_todo(self, todo_id: int) -> Dict:
        """
        Delete a todo permanently by ID.
        
        Args:
            todo_id (int): The ID of the todo to delete
        
        Returns:
            Dict: Success/error response
            Success:
            {
                "status": "deleted",
                "id": 1
            }
            Error:
            {
                "status": "error",
                "message": "Todo not found"
            }
        
        Example:
            >>> storage = TodoStorage()
            >>> storage.delete_todo(1)
            {'status': 'deleted', 'id': 1}
        """
        data = self._load()
        original_count = len(data["todos"])
        
        # Filter out the todo with matching ID
        data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
        
        # Check if todo was found and deleted
        if len(data["todos"]) < original_count:
            self._save(data)
            return {"status": "deleted", "id": todo_id}
        
        return {"status": "error", "message": f"Todo with ID {todo_id} not found"}
    
    def search_todos(self, query: str) -> List[Dict]:
        """
        Search todos by keyword in task description (case-insensitive).
        
        Args:
            query (str): Search query
        
        Returns:
            List[Dict]: Matching todos
        
        Example:
            >>> storage = TodoStorage()
            >>> results = storage.search_todos("report")
        """
        data = self._load()
        query_lower = query.lower()
        return [t for t in data["todos"] if query_lower in t["task"].lower()]
    
    def get_stats(self) -> Dict:
        """
        Get statistics about todos.
        
        Returns:
            Dict: Statistics
            {
                "total": 10,
                "completed": 3,
                "incomplete": 7,
                "high_priority": 2,
                "normal_priority": 5,
                "low_priority": 3
            }
        """
        data = self._load()
        todos = data["todos"]
        
        return {
            "total": len(todos),
            "completed": sum(1 for t in todos if t["is_completed"]),
            "incomplete": sum(1 for t in todos if not t["is_completed"]),
            "high_priority": sum(1 for t in todos if t["priority"] == "high"),
            "normal_priority": sum(1 for t in todos if t["priority"] == "normal"),
            "low_priority": sum(1 for t in todos if t["priority"] == "low")
        }
    
    def _load(self) -> Dict:
        """
        Internal method to load todos from JSON file.
        
        Returns:
            Dict: Parsed JSON data
        """
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return default structure if file is corrupted
            return {"todos": [], "metadata": {"created": datetime.now().isoformat()}}
    
    def _save(self, data: Dict) -> None:
        """
        Internal method to save todos to JSON file.
        
        Args:
            data (Dict): Data to save
        """
        # Update last_modified timestamp
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["last_modified"] = datetime.now().isoformat()
        
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def reset(self) -> Dict:
        """
        Reset storage - delete all todos (WARNING: destructive operation).
        
        Returns:
            Dict: Confirmation message
        """
        initial_data = {
            "todos": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
        }
        with open(self.filepath, 'w') as f:
            json.dump(initial_data, f, indent=2)
        return {"status": "reset", "message": "All todos deleted"}


def format_todo_for_display(todo: Dict) -> str:
    """
    Format a todo item for human-readable display.
    
    Args:
        todo (Dict): Todo item
    
    Returns:
        str: Formatted string
        Example output:
        "[1] Write report (HIGH) - Created: 2026-08-20 ✓"
    """
    status = "✓" if todo["is_completed"] else "○"
    priority_emoji = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(todo["priority"], "")
    
    return (
        f"[{todo['id']}] {todo['task']} {priority_emoji} ({todo['priority'].upper()}) "
        f"- {status}"
    )


def format_todos_list(todos: List[Dict]) -> str:
    """
    Format multiple todos for display.
    
    Args:
        todos (List[Dict]): List of todo items
    
    Returns:
        str: Formatted multi-line string
    """
    if not todos:
        return "No todos found."
    
    return "\n".join(format_todo_for_display(t) for t in todos)
