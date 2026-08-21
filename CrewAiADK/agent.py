"""
CrewAI Todo Manager Agent with Ollama Support
UPDATED: Using Ollama (free, local) - No API key needed!
Uses CrewAI 1.15+ with local Ollama models
"""
import json
import os
import sys

# Add parent directory to path for shared_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from shared_utils.todo_storage import TodoStorage

# Initialize storage
storage = TodoStorage()

# Initialize LLM using CrewAI's LLM wrapper with Ollama
# Trying llama3.2 which is more stable and reliable for function calling
llm = LLM(
    model="ollama/llama3.2",  # Llama 3.2 (2GB, proven reliable)
    base_url="http://localhost:11434"  # Ollama endpoint
)

# Define tools using @tool decorator (CrewAI 1.15+ requires this)
@tool("Add Todo Task")
def add_todo(task: str, priority: str = "medium") -> str:
    """Add a new todo task with specified priority (low, medium, or high)."""
    todo_id = storage.add_todo(task, priority=priority)
    return f"✓ Added task #{todo_id}: {task} (priority: {priority})"

@tool("Get All Todos")
def get_todos(include_completed: bool = False) -> str:
    """Get all todo tasks. By default shows only incomplete tasks."""
    todos = storage.get_todos(include_completed=include_completed)
    if not todos:
        return "📋 No incomplete tasks found"
    result = "📋 Your incomplete tasks:\n"
    for todo in todos:
        if not todo.get("is_completed", False):
            status = "○"
            result += f"\n{status} #{todo['id']}: {todo['task']} [{todo.get('priority', 'medium')}]"
    return result

@tool("Complete Todo Task")
def complete_todo(todo_ids: str) -> str:
    """Mark one or multiple todo tasks as complete.
    
    Examples:
    - "1" → Completes task #1
    - "1,2,3" → Completes tasks #1, #2, #3
    - "1, 2, 3" → Completes tasks #1, #2, #3 (spaces work too)
    """
    # Parse comma-separated IDs
    ids = [int(id.strip()) for id in str(todo_ids).split(',')]
    results = []
    
    for todo_id in ids:
        success = storage.complete_todo(todo_id)
        if success:
            results.append(f"✓ Task #{todo_id} marked as complete!")
        else:
            results.append(f"✗ Task #{todo_id} not found")
    
    return "\n".join(results)

@tool("Delete Todo Task")
def delete_todo(todo_ids: str) -> str:
    """Delete one or multiple todo tasks.
    
    Examples:
    - "1" → Deletes task #1
    - "1,2,3" → Deletes tasks #1, #2, #3
    """
    # Parse comma-separated IDs
    ids = [int(id.strip()) for id in str(todo_ids).split(',')]
    results = []
    
    for todo_id in ids:
        success = storage.delete_todo(todo_id)
        if success:
            results.append(f"✓ Task #{todo_id} deleted!")
        else:
            results.append(f"✗ Task #{todo_id} not found")
    
    return "\n".join(results)

@tool("Get Todo Statistics")
def get_stats() -> str:
    """Get statistics about all todo tasks including counts and priorities."""
    s = storage.get_stats()
    return f"📊 Total: {s['total']}, Done: {s['completed']}, Pending: {s['incomplete']}, High: {s.get('high_priority', 0)}, Normal: {s.get('normal_priority', 0)}, Low: {s.get('low_priority', 0)}"

# Removed complete_all_tasks() - Use "complete task 1,2,3..." instead for multiple tasks

# Create the Todo Manager Agent with 5 core tools
todo_agent = Agent(
    role="Todo Manager",
    goal="Help users manage their todo tasks efficiently",
    backstory="""You are a helpful todo assistant. You have 5 tools:
1. add_todo(task, priority) - Add new task
2. get_todos() - Show only incomplete tasks  
3. complete_todo(todo_ids) - Complete one or multiple tasks (e.g., "1" or "1,2,3")
4. delete_todo(todo_ids) - Delete one or multiple tasks (e.g., "1,2")
5. get_stats() - Show task statistics

Usage examples:
- "add task learn python" → add_todo(task="learn python", priority="medium")
- "add task exercise high priority" → add_todo(task="exercise", priority="high")
- "list tasks" → get_todos()
- "complete task 1" → complete_todo("1")
- "complete task 1,2,3" → complete_todo("1,2,3")
- "delete task 2" → delete_todo("2")
- "show stats" → get_stats()

Always call exactly ONE tool. Extract task names and IDs from user input.""",
    llm=llm,
    tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats],
    verbose=False,
    allow_delegation=False
)

def process_user_input(user_input: str) -> str:
    """Process user input and return agent response."""
    task = Task(
        description=f"""User input: "{user_input}"

Identify the action and call the appropriate tool:
- "add" → add_todo()
- "complete task" → complete_todo()
- "delete task" → delete_todo()
- "list" or "show" → get_todos()
- "stats" → get_stats()

Extract parameters (task name, priority, task IDs) from user input and call tool.""",
        agent=todo_agent,
        expected_output="Tool result"
    )
    
    crew = Crew(
        agents=[todo_agent],
        tasks=[task],
        verbose=False
    )
    
    result = crew.kickoff()
    return str(result)

async def process_user_input_async(user_input: str) -> str:
    """Process user input asynchronously and return agent response."""
    task = Task(
        description=f"""User input: "{user_input}"

Identify the action and call the appropriate tool:
- "add" → add_todo()
- "complete task" → complete_todo()
- "delete task" → delete_todo()
- "list" or "show" → get_todos()
- "stats" → get_stats()

Extract parameters (task name, priority, task IDs) from user input and call tool.""",
        agent=todo_agent,
        expected_output="Tool result"
    )
    
    crew = Crew(
        agents=[todo_agent],
        tasks=[task],
        verbose=False
    )
    
    result = await crew.kickoff_async()
    return str(result)
