"""
OpenAI Todo Manager Agent with Ollama Support
Uses OpenAI SDK v3.3+ patterns with Ollama (free, local LLM)
UPDATED: Configured for Ollama - No API key needed!
"""
import json
import os
import sys

# Add parent directory to path for shared_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from shared_utils.todo_storage import TodoStorage

# Initialize storage
storage = TodoStorage()

# Initialize OpenAI client for Ollama (free, local)
# Uses Ollama's OpenAI-compatible API endpoint
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible endpoint
    api_key="ollama",  # Dummy key required by SDK, not used by Ollama
)

# Define todo management functions
def add_todo(task: str, priority: str = "medium") -> str:
    """Add a new todo task."""
    todo_id = storage.add_todo(task, priority=priority)
    return json.dumps({"success": True, "message": f"✓ Added task #{todo_id}: {task} (priority: {priority})"})

def get_todos(include_completed: bool = False) -> str:
    """Get all todo tasks."""
    todos = storage.get_todos(include_completed=include_completed)
    if not todos:
        return json.dumps({"tasks": [], "message": "📋 No tasks found"})
    
    tasks = []
    for todo in todos:
        status = "✓" if todo.get("is_completed") else "○"
        tasks.append({
            "id": todo['id'],
            "task": todo['task'],
            "priority": todo.get('priority', 'medium'),
            "is_completed": todo.get("is_completed", False),
            "status_symbol": status
        })
    return json.dumps({"tasks": tasks, "count": len(tasks)})

def complete_todo(todo_id: int) -> str:
    """Mark a todo task as complete."""
    success = storage.complete_todo(todo_id)
    return json.dumps({"success": success, "message": f"✓ Task #{todo_id} marked as complete!" if success else f"✗ Task #{todo_id} not found"})

def delete_todo(todo_id: int) -> str:
    """Delete a todo task."""
    success = storage.delete_todo(todo_id)
    return json.dumps({"success": success, "message": f"✓ Task #{todo_id} deleted!" if success else f"✗ Task #{todo_id} not found"})

def get_stats() -> str:
    """Get todo statistics."""
    s = storage.get_stats()
    return json.dumps({
        "total": s['total'],
        "completed": s['completed'],
        "incomplete": s['incomplete'],
        "high_priority": s.get('high_priority', 0),
        "normal_priority": s.get('normal_priority', 0),
        "low_priority": s.get('low_priority', 0)
    })

# Define tools for OpenAI function calling (SDK v3.3+)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "Add a new todo task to the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task description to add"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level (default: medium)"
                    }
                },
                "required": ["task"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_todos",
            "description": "Get all todo tasks from storage",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_completed": {
                        "type": "boolean",
                        "description": "Include completed tasks in results (default: false)"
                    }
                },
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "Mark a specific todo task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete"
                    }
                },
                "required": ["todo_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "Delete a specific todo task",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["todo_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stats",
            "description": "Get statistics about all todo tasks",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    }
]

# Function map for execution
FUNCTION_MAP = {
    "add_todo": add_todo,
    "get_todos": get_todos,
    "complete_todo": complete_todo,
    "delete_todo": delete_todo,
    "get_stats": get_stats
}

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result."""
    if tool_name in FUNCTION_MAP:
        func = FUNCTION_MAP[tool_name]
        try:
            return func(**tool_input)
        except TypeError as e:
            return json.dumps({"error": f"Invalid arguments for {tool_name}: {str(e)}"})
    return json.dumps({"error": f"Unknown tool: {tool_name}"})
