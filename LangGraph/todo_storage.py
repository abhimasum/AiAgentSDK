"""
Todo Storage Layer for LangGraph Agent

This module provides persistent JSON-based storage for todo items.
Storage is folder-specific, with each folder maintaining its own todos.json file.

Key Features:
- JSON persistence (human-readable, easy to backup)
- Auto-incremental IDs
- Priority levels (low, normal, high)
- Timestamp tracking (created_at, completed_at)
- Flexible search (by ID or task description)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class TodoStorage:
    """
    Manages persistent storage of todo items in JSON format.
    
    Design Principles:
    1. **File per Folder**: Each folder gets its own todos.json
    2. **Auto-create**: Creates file on first use if missing
    3. **Transaction Safety**: Read → Modify → Write pattern
    4. **Type Safety**: Returns structured dictionaries
    
    Storage Schema:
    {
        "todos": [
            {
                "id": 1,
                "task": "Task description",
                "priority": "high|normal|low",
                "created_at": "2026-08-21T10:00:00",
                "completed_at": null,
                "is_completed": false,
                "description": "Optional extended description"
            }
        ]
    }
    """
    
    def __init__(self, filepath: str = "todos.json"):
        """
        Initialize storage with specified JSON file.
        
        Args:
            filepath: Path to JSON storage file (default: "todos.json")
        """
        self.filepath = filepath
        self._ensure_file()
    
    def _ensure_file(self):
        """Create todos.json with empty structure if it doesn't exist"""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({"todos": []}, f, indent=2)
    
    def _load(self) -> Dict:
        """Load all data from JSON file"""
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def _save(self, data: Dict):
        """Save data to JSON file with pretty formatting"""
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_todo(self, task: str, priority: str = "normal", description: str = "") -> Dict:
        """
        Add a new todo item to storage.
        
        Args:
            task: Brief task description
            priority: Priority level (low/normal/high)
            description: Optional extended description
            
        Returns:
            Dictionary with id, status, task, and priority
        """
        data = self._load()
        
        # Generate next available ID
        new_id = max([t["id"] for t in data["todos"]], default=0) + 1
        
        todo = {
            "id": new_id,
            "task": task,
            "priority": priority.lower(),
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "is_completed": False,
            "description": description
        }
        
        data["todos"].append(todo)
        self._save(data)
        
        return {
            "id": new_id,
            "status": "created",
            "task": task,
            "priority": priority
        }
    
    def get_todos(self, include_completed: bool = False) -> List[Dict]:
        """
        Retrieve todos, optionally filtering completed ones.
        
        Args:
            include_completed: If True, returns all todos; if False, only incomplete
            
        Returns:
            List of todo dictionaries
        """
        data = self._load()
        
        if include_completed:
            return data["todos"]
        
        return [t for t in data["todos"] if not t["is_completed"]]
    
    def complete_todo(self, todo_id: Optional[int] = None, description: Optional[str] = None) -> Dict:
        """
        Mark a todo as complete by ID or description match.
        
        Args:
            todo_id: Exact ID of todo to complete
            description: Search string to match in task description
            
        Returns:
            Dictionary with status, id, and task
        """
        data = self._load()
        
        # Search for matching todo
        for todo in data["todos"]:
            # Match by ID (exact) or description (substring, case-insensitive)
            if (todo_id is not None and todo["id"] == todo_id) or \
               (description is not None and todo_id is None and 
                description.lower() in todo["task"].lower()):
                
                if todo["is_completed"]:
                    return {
                        "status": "already_completed",
                        "id": todo["id"],
                        "task": todo["task"]
                    }
                
                todo["is_completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self._save(data)
                
                return {
                    "status": "completed",
                    "id": todo["id"],
                    "task": todo["task"]
                }
        
        return {
            "status": "error",
            "message": f"Todo not found (id={todo_id}, description={description})"
        }
    
    def delete_todo(self, todo_id: int) -> Dict:
        """
        Permanently delete a todo by ID.
        
        Args:
            todo_id: ID of todo to delete
            
        Returns:
            Dictionary with status and id
        """
        data = self._load()
        original_count = len(data["todos"])
        
        # Filter out the todo with matching ID
        data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
        
        if len(data["todos"]) < original_count:
            self._save(data)
            return {"status": "deleted", "id": todo_id}
        
        return {
            "status": "error",
            "message": f"Todo with ID {todo_id} not found"
        }
    
    def get_stats(self) -> Dict:
        """
        Get statistics about todos.
        
        Returns:
            Dictionary with counts by status and priority
        """
        data = self._load()
        todos = data["todos"]
        
        completed = sum(1 for t in todos if t["is_completed"])
        incomplete = len(todos) - completed
        
        high_priority = sum(1 for t in todos if t["priority"] == "high" and not t["is_completed"])
        normal_priority = sum(1 for t in todos if t["priority"] == "normal" and not t["is_completed"])
        low_priority = sum(1 for t in todos if t["priority"] == "low" and not t["is_completed"])
        
        return {
            "total": len(todos),
            "completed": completed,
            "incomplete": incomplete,
            "high_priority": high_priority,
            "normal_priority": normal_priority,
            "low_priority": low_priority
        }
