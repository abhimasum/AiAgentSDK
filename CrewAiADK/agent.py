"""
CrewAI Todo Manager Agent with Ollama Support
UPDATED: Using Ollama (free, local) - No API key needed!
Uses CrewAI 1.15+ with local Ollama models
"""
import json
import os
import sys
import re

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
    role="Todo Assistant",
    goal="Help users manage their todo tasks by calling the appropriate tools",
    backstory="""You are a todo assistant that helps users manage tasks.

When users give commands:
- Extract task names from "add task [name]" or "add [name]"
- Extract task IDs from numbers in the command
- Extract priority from "high priority", "low priority" (default: medium)
- Call the appropriate tool with correct parameters
- Return only the tool's result, no extra text

Available tools and when to use them:
- add_todo: When user wants to add/create a task
- get_todos: When user wants to list/show tasks
- complete_todo: When user wants to complete/finish/mark done
- delete_todo: When user wants to delete/remove a task
- get_stats: When user wants statistics/summary

Just call the tool and return its result.""",
    llm=llm,
    tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats],
    verbose=False,
    allow_delegation=False
)

# Manual tool execution helper
def execute_tool_from_result(result_str: str) -> str:
    """
    Parse CrewAI result and manually execute tools if needed.
    CrewAI sometimes returns tool call JSON instead of executing, so we handle it.
    """
    result_str = str(result_str).strip()
    
    # Try to find JSON tool call pattern (handles empty parameters too)
    tool_call_match = re.search(r'\{"name":\s*"([^"]+)"[^}]*"parameters":\s*(\{[^}]*\})', result_str)
    
    if tool_call_match:
        tool_name = tool_call_match.group(1)
        try:
            params_str = tool_call_match.group(2)
            params = json.loads(params_str) if params_str.strip() != '{}' else {}
        except:
            params = {}
        
        # Execute tools directly (not via .func())
        try:
            if "add_todo" in tool_name.lower():
                task = params.get("task", "")
                priority = params.get("priority", "medium")
                result = storage.add_todo(task, priority=priority)
                # Extract ID from result dict
                if isinstance(result, dict) and result.get("status") == "created":
                    todo_id = result.get("id")
                    return f"✓ Added task #{todo_id}: {task} (priority: {priority})"
                else:
                    return f"Error: {result.get('message', 'Failed to add task')}"
            
            elif "get_todos" in tool_name.lower() or "get_all_todos" in tool_name.lower():
                include_completed = params.get("include_completed", False)
                if isinstance(include_completed, str):
                    include_completed = include_completed.lower() == "true"
                todos = storage.get_todos(include_completed=include_completed)
                if not todos:
                    return "📋 No incomplete tasks found"
                result = "📋 Your incomplete tasks:\n"
                for todo in todos:
                    if not todo.get("is_completed", False):
                        result += f"\n○ #{todo['id']}: {todo['task']} [{todo.get('priority', 'medium')}]"
                return result
            
            elif "complete_todo" in tool_name.lower():
                todo_ids = params.get("todo_ids", params.get("ids", ""))
                ids = [int(id.strip()) for id in str(todo_ids).split(',')]
                results = []
                for todo_id in ids:
                    success = storage.complete_todo(todo_id)
                    if success:
                        results.append(f"✓ Task #{todo_id} marked as complete!")
                    else:
                        results.append(f"✗ Task #{todo_id} not found")
                return "\n".join(results)
            
            elif "delete_todo" in tool_name.lower():
                todo_ids = params.get("todo_ids", params.get("ids", ""))
                ids = [int(id.strip()) for id in str(todo_ids).split(',')]
                results = []
                for todo_id in ids:
                    success = storage.delete_todo(todo_id)
                    if success:
                        results.append(f"✓ Task #{todo_id} deleted!")
                    else:
                        results.append(f"✗ Task #{todo_id} not found")
                return "\n".join(results)
            
            elif "get_stats" in tool_name.lower() or "statistics" in tool_name.lower():
                s = storage.get_stats()
                return f"📊 Total: {s['total']}, Done: {s['completed']}, Pending: {s['incomplete']}, High: {s.get('high_priority', 0)}, Normal: {s.get('normal_priority', 0)}, Low: {s.get('low_priority', 0)}"
            
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    # If no tool call pattern found, return original result
    return result_str

def process_user_input(user_input: str) -> str:
    """Process user input and return agent response."""
    task = Task(
        description=f"""Identify the tool to call for: "{user_input}"

Return ONLY a JSON tool call in this exact format:
{{"name": "tool_name", "parameters": {{...}}}}

Tool mappings:
- add task → {{"name": "add_todo", "parameters": {{"task": "...", "priority": "medium"}}}}
- list → {{"name": "get_todos", "parameters": {{"include_completed": false}}}}
- complete → {{"name": "complete_todo", "parameters": {{"todo_ids": "1"}}}}
- delete → {{"name": "delete_todo", "parameters": {{"todo_ids": "1"}}}}
- stats → {{"name": "get_stats", "parameters": {{}}}}

Return ONLY the JSON, nothing else.""",
        agent=todo_agent,
        expected_output="JSON tool call"
    )
    
    crew = Crew(
        agents=[todo_agent],
        tasks=[task],
        verbose=False
    )
    
    result = crew.kickoff()
    return execute_tool_from_result(str(result))

async def process_user_input_async(user_input: str) -> str:
    """Process user input asynchronously and return agent response."""
    task = Task(
        description=f"""Identify the tool to call for: "{user_input}"

Return ONLY a JSON tool call in this exact format:
{{"name": "tool_name", "parameters": {{...}}}}

Tool mappings:
- add task → {{"name": "add_todo", "parameters": {{"task": "...", "priority": "medium"}}}}
- list → {{"name": "get_todos", "parameters": {{"include_completed": false}}}}
- complete → {{"name": "complete_todo", "parameters": {{"todo_ids": "1"}}}}
- delete → {{"name": "delete_todo", "parameters": {{"todo_ids": "1"}}}}
- stats → {{"name": "get_stats", "parameters": {{}}}}

Return ONLY the JSON, nothing else.""",
        agent=todo_agent,
        expected_output="JSON tool call"
    )
    
    crew = Crew(
        agents=[todo_agent],
        tasks=[task],
        verbose=False
    )
    
    result = await crew.kickoff_async()
    return execute_tool_from_result(str(result))
