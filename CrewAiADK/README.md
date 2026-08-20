# CrewAI Todo Manager - Complete Setup Guide

**Framework:** CrewAI  
**LLM:** Ollama (Local)  
**Complexity:** Intermediate  
**Time to Setup:** 15-20 minutes  

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Running the Agent](#running-the-agent)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [Understanding the Code](#understanding-the-code)

---

## Overview

This is a **Todo Management Agent** built with **CrewAI**, a multi-agent orchestration framework. The agent:

✅ Understands natural language commands  
✅ Manages todo items (add, complete, retrieve, delete)  
✅ Stores todos persistently in JSON  
✅ Uses **Ollama** for local, private LLM inference  
✅ Provides a conversational interface  

### Example Interactions

```
You: Add a high priority task: write quarterly report
Agent: ✅ Added task 'write quarterly report' (HIGH) - ID: 1

You: Show my tasks
Agent: 📋 You have 1 incomplete task:
       [1] write quarterly report (HIGH)

You: Mark the report as done
Agent: ✅ Completed 'write quarterly report'

You: Give me a summary
Agent: 📊 Stats: 1 total, 1 completed, 0 pending
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│          User Input (Natural Language)       │
│     "Add task: Write report with high       │
│      priority"                               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │   CrewAI Agent     │
        │  - Parse intent    │
        │  - Choose tool     │
        │  - Execute action  │
        └────────┬───────────┘
                 │
        ┌────────┴──────────┐
        │                   │
        ▼                   ▼
    ┌─────────┐      ┌──────────────┐
    │ Ollama  │      │ Tools Layer  │
    │ LLM     │      │  - add_todo()
    │Mistral  │      │  - get_todos()
    │         │      │  - complete_todo()
    └─────────┘      │  - delete_todo()
                     │  - get_stats()
                     └────────┬──────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  JSON Storage   │
                     │  (todos.json)   │
                     └─────────────────┘
```

### File Structure

```
CrewAiADK/
├── main.py              # Entry point - run this to start
├── todo_manager.py      # Agent definition (TodoManagerCrew class)
├── tools.py             # Tool definitions (add_todo, etc.)
├── config.yaml          # Agent and task configuration
├── pyproject.toml       # UV package management
├── requirements.txt     # Pip package management
├── README.md            # This file
└── todos.json           # Generated at runtime - stores todo data
```

---

## Prerequisites

### Required Software

- **Python 3.10+** - Check with: `python --version`
- **Ollama** - Download from [https://ollama.ai](https://ollama.ai)
- **Git** (optional) - For version control

### Verify Installation

```bash
# Check Python
python --version          # Should be 3.10 or higher

# Check Ollama installation
ollama --version         # Should show version number
```

---

## Installation

### Step 1: Install Ollama

1. Visit [https://ollama.ai](https://ollama.ai)
2. Download for your OS (Windows, Mac, Linux)
3. Install by running the installer
4. Verify: `ollama --version`

### Step 2: Pull a Language Model

Ollama requires a language model. We recommend **Mistral** for this todo application (small, fast, good reasoning):

```bash
ollama pull mistral
```

Other options:
- `ollama pull llama2` - Larger, more capable
- `ollama pull neural-chat` - Lightweight, conversational

### Step 3: Clone/Setup Project (First Time Only)

```bash
# Navigate to the CrewAiADK folder
cd CrewAiADK
```

### Step 4: Install Dependencies

**Option A: Using UV (Recommended - Faster, Modern)**

```bash
# Install uv if you don't have it
pip install uv

# Sync dependencies
uv sync

# Run the agent
uv run main.py
```

**Option B: Using Pip + Virtual Environment (Traditional)**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py
```

---

## Running the Agent

### Step 1: Start Ollama

Ollama must be running for the agent to work. Open a terminal and run:

```bash
ollama serve
```

You should see:
```
Listening on 127.0.0.1:11434
```

Leave this terminal open while using the agent.

### Step 2: Run the Agent (Different Terminal)

```bash
# If using uv:
uv run main.py

# If using pip:
python main.py
```

### Step 3: Interact with the Agent

```
============================================================
🤖 CrewAI Todo Manager Agent
============================================================

Welcome! I can help you manage your todos.
Commands examples:
  - Add a task: 'Add task: write report with high priority'
  - Show tasks: 'Show my incomplete tasks'
  - Complete task: 'Mark report as done' or 'Complete task 1'
  - Get stats: 'How many tasks do I have?'
  - Delete task: 'Remove task 1'

Type 'quit' to exit.
============================================================

📝 You: Add task: write quarterly report with high priority

🔄 Processing your request...

🤖 Agent: ✅ Added task 'write quarterly report' (HIGH priority) - ID: 1

📝 You: show my tasks

🔄 Processing your request...

🤖 Agent: 📋 Your incomplete tasks:
1. [HIGH] write quarterly report - ID: 1

📝 You: quit

👋 Goodbye! Your todos have been saved.
```

---

## Testing

### Manual Testing Scenarios

**Test 1: Add a Todo**
```
Input:  "Add a high priority task: review code"
Expected: Task created with ID, high priority confirmed
```

**Test 2: List Todos**
```
Input:  "Show all my tasks"
Expected: Lists all incomplete todos with IDs and priorities
```

**Test 3: Complete by Description**
```
Input:  "Mark the code review as done"
Expected: Task marked complete, timestamp recorded
```

**Test 4: Complete by ID**
```
Input:  "Mark task 1 as complete"
Expected: Task with ID 1 marked done
```

**Test 5: Get Statistics**
```
Input:  "How many tasks do I have total?"
Expected: Shows summary (total, completed, incomplete, by priority)
```

**Test 6: Delete a Todo**
```
Input:  "Delete task 2"
Expected: Task removed, confirmation shown
```

### Automated Testing (Python)

Create `test_agent.py`:

```python
#!/usr/bin/env python
"""Quick test of the todo agent"""

import json
from pathlib import Path
from tools import add_todo, get_todos, complete_todo, delete_todo, get_stats

def test_workflow():
    """Test basic todo workflow"""
    
    print("Testing Todo Agent Workflow\n")
    
    # Test 1: Add todos
    print("1. Adding todos...")
    r1 = add_todo("Write report", priority="high")
    print(f"   {r1}")
    
    r2 = add_todo("Review code", priority="normal")
    print(f"   {r2}")
    
    # Test 2: Get todos
    print("\n2. Getting todos...")
    todos = get_todos()
    for t in todos:
        print(f"   [{t['id']}] {t['task']} ({t['priority']})")
    
    # Test 3: Complete a todo
    print("\n3. Completing a todo...")
    r3 = complete_todo(todo_id=1)
    print(f"   {r3}")
    
    # Test 4: Get stats
    print("\n4. Getting stats...")
    stats = get_stats()
    print(f"   Total: {stats['total']}, Completed: {stats['completed']}, Incomplete: {stats['incomplete']}")
    
    # Test 5: Delete
    print("\n5. Deleting a todo...")
    r4 = delete_todo(2)
    print(f"   {r4}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_workflow()
```

Run with:
```bash
python test_agent.py
```

---

## Troubleshooting

### Issue: "Cannot connect to Ollama"

**Symptom:**
```
❌ ERROR: Cannot connect to Ollama!
```

**Solution:**
1. Check if Ollama is running: `ollama serve` in a separate terminal
2. Verify Ollama is accessible: `curl http://localhost:11434/api/tags`
3. Check firewall settings allow localhost:11434

### Issue: "Model not found"

**Symptom:**
```
Error: mistral model not found
```

**Solution:**
```bash
# Pull the mistral model
ollama pull mistral

# Verify it was installed
ollama list
```

### Issue: "Command not found: uv"

**Symptom:**
```
command not found: uv
```

**Solution:**
```bash
# Install uv globally
pip install uv

# Or use pip instead
python -m pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'crewai'"

**Symptom:**
```
ModuleNotFoundError: No module named 'crewai'
```

**Solution:**
1. Make sure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.10+)

### Issue: "Permission Denied" on Mac/Linux

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Make script executable
chmod +x main.py

# Run with python explicitly
python main.py
```

### Issue: Slow Agent Responses

**Cause:** Model is processing (normal for first run)  
**Solution:** Wait longer or use lighter model

```bash
ollama pull neural-chat  # Smaller, faster model
```

Then edit `main.py` and change:
```python
self.llm = OllamaLLM(model="neural-chat", ...)
```

---

## Understanding the Code

### Main Components

#### 1. **tools.py** - Tool Definitions

Tools are functions the agent can call. Each tool has:
- Type hints (parameter schema)
- Docstring (description for agent)
- Implementation (uses TodoStorage)

```python
@tool
def add_todo(task: str, priority: str = "normal") -> dict:
    """Add a new todo item - the agent reads this description"""
    return storage.add_todo(task, priority)
```

#### 2. **config.yaml** - Agent Personality

Defines agent role, goal, and backstory:

```yaml
todo_manager_agent:
  role: "Todo Manager Agent"
  goal: "Efficiently manage and organize user's todo items"
  backstory: "You are an intelligent todo management assistant..."
  model: "ollama/mistral"
  temperature: 0.3  # Lower = more deterministic
```

#### 3. **todo_manager.py** - Agent Definition

Defines agent and task using CrewBase:

```python
class TodoManagerCrew(CrewBase):
    @agent
    def todo_manager_agent(self) -> Agent:
        # Create agent with tools
        return Agent(
            config=self.agents_config["todo_manager_agent"],
            tools=[add_todo, get_todos, complete_todo, ...],
            llm=self.llm
        )
    
    @task
    def manage_todos_task(self) -> Task:
        # Create task
        return Task(config=self.tasks_config["manage_todos_task"])
    
    @crew
    def crew(self) -> Crew:
        # Orchestrate everything
        return Crew(agents=self.agents, tasks=self.tasks)
```

#### 4. **main.py** - Entry Point

Handles user interaction loop:

```python
def main():
    crew_instance = TodoManagerCrew()
    
    while True:
        user_input = input("\n📝 You: ")
        result = crew_instance.crew().kickoff(
            inputs={"user_request": user_input}
        )
        print(f"\n🤖 Agent: {result}")
```

### Agent Loop Explained

When you send a request to the agent:

1. **Perception**: Agent reads your request
2. **Reasoning**: LLM decides which tool to use
3. **Action**: Tool is executed with parameters
4. **Observation**: Result is received
5. **Response**: Agent formulates response to you
6. **Persistence**: Change is saved to todos.json

---

## Advanced Configuration

### Change the LLM Model

Edit `config.yaml`:
```yaml
model: "ollama/llama2"  # Change to llama2
```

Or edit `main.py`:
```python
self.llm = OllamaLLM(
    model="neural-chat",  # Different model
    temperature=0.5       # More creative
)
```

### Adjust Agent Behavior

Modify `config.yaml` agent backstory:
```yaml
backstory: >
  You are a strict, no-nonsense todo assistant who 
  speaks very formally and always confirms actions 
  with specific timestamps.
```

### Add Custom Tools

1. Add a new function in `tools.py`
2. Decorate with `@tool`
3. Add to agent's tools list in `todo_manager.py`

Example:
```python
@tool
def list_by_priority(priority: str) -> list:
    """Get todos by priority level"""
    return [t for t in storage.get_todos() if t["priority"] == priority]
```

---

## Project Structure Explanation

| File | Purpose | Editing Needed? |
|------|---------|-----------------|
| `main.py` | Entry point, user loop | Rarely - for UI changes |
| `todo_manager.py` | Agent definition, orchestration | Rarely - for LLM changes |
| `tools.py` | Tool definitions | Sometimes - to add new tools |
| `config.yaml` | Agent personality, settings | Often - to tune agent behavior |
| `todos.json` | Data storage (auto-generated) | No - data file |
| `requirements.txt` | Pip dependencies | No - unless adding libraries |
| `pyproject.toml` | UV dependencies | No - unless adding libraries |
| `README.md` | Documentation | No - reference only |

---

## Next Steps

1. ✅ Get familiar with the agent by testing basic commands
2. ✅ Read through the code comments to understand flow
3. ✅ Examine `todos.json` to see data structure
4. ✅ Try modifying the agent backstory in `config.yaml`
5. ✅ Experiment with different Ollama models
6. ✅ Add custom tools by extending `tools.py`
7. ✅ Compare with other frameworks (OpenAI, Google ADK)

---

## Key Takeaways

🎯 **CrewAI Pattern:**
- Agents read tool descriptions (docstrings)
- Agent uses LLM to choose appropriate tools
- Tools interact with storage layer
- Results flow back to user

🎯 **Why Ollama:**
- No API keys needed
- Private local inference
- Free (no usage costs)
- Great for learning and testing

🎯 **This Implementation:**
- Multi-agent framework for complex workflows
- Task-based orchestration
- Config-driven agent behavior
- Easily extensible with new tools

---

## Quick Reference

```bash
# Start Ollama (terminal 1)
ollama serve

# Install deps and run (terminal 2)
uv sync && uv run main.py          # With UV
# OR
pip install -r requirements.txt && python main.py  # With pip

# Test directly
python test_agent.py

# View todos data
cat todos.json
```

---

**Last Updated:** 2026-08-20  
**Framework Version:** CrewAI 0.35.0  
**Python Version:** 3.10+  
**Difficulty:** Intermediate  

For issues, check the troubleshooting section above or review the code comments.
