# OpenAI Agents SDK Todo Manager - Setup Guide

**Framework:** OpenAI Agents SDK  
**LLM:** OpenAI API (or Ollama locally)  
**Complexity:** Beginner-Friendly  
**Setup Time:** 10-15 minutes  

---

## Overview

A **simple, direct Todo Management Agent** using OpenAI's Agents SDK.

✅ Natural language todo management  
✅ Works with OpenAI models or Ollama  
✅ JSON persistence  
✅ Tool-based orchestration  
✅ Easy to understand and extend  

### Quick Example

```
You: Add a high priority task: write quarterly report
Agent: ✅ Added 'write quarterly report' (HIGH) - ID: 1

You: Show my tasks
Agent: 📋 You have 1 incomplete task:
       [1] write quarterly report (HIGH)

You: Mark it done
Agent: ✅ Completed 'write quarterly report'
```

---

## Prerequisites

### Required
- Python 3.10+: `python --version`
- Either:
  - **OpenAI API Key** from https://platform.openai.com/api-keys (paid), OR
  - **Ollama** running locally (free) from https://ollama.ai

### Verify Installation

```bash
python --version  # Should be 3.10+

# If using Ollama:
ollama --version
ollama pull mistral  # Pull a model
ollama serve         # Start Ollama
```

---

## Installation

### Step 1: Setup Ollama (Free) OR OpenAI API Key

**Option A: Ollama (Recommended for Learning)**

```bash
# Install from https://ollama.ai
ollama pull mistral
ollama serve  # Keep running in background
```

**Option B: OpenAI API**

```bash
# Set environment variable
export OPENAI_API_KEY="sk-..."  # Your API key
# OR on Windows:
set OPENAI_API_KEY=sk-...
```

### Step 2: Install Dependencies

**Using UV (Faster):**

```bash
uv sync
uv run main.py
```

**Using Pip:**

```bash
python -m venv venv

# Activate venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
python main.py
```

---

## Running the Agent

### Start Ollama (if using local)

```bash
ollama serve
```

### Run the Agent

```bash
uv run main.py    # With uv
# OR
python main.py    # With pip
```

---

## File Structure

```
OpenAiADK/
├── main.py           # Entry point - run this
├── tools.py          # Tool functions (add_todo, etc.)
├── config.py         # Configuration (agent settings)
├── pyproject.toml    # UV dependencies
├── requirements.txt  # Pip dependencies
├── README.md         # This file
└── todos.json        # Generated data file
```

---

## Key Code Sections

### 1. Tools (tools.py)

Tools are functions decorated with `@function_tool`:

```python
@function_tool
def add_todo(task: str, priority: str = "normal") -> str:
    """Add a new todo item"""
    result = storage.add_todo(task, priority)
    return json.dumps(result)
```

**Important:** OpenAI requires tools to return JSON strings (not dicts like CrewAI).

### 2. Agent Creation (main.py)

Simple agent setup:

```python
agent = Agent(
    name="TodoManager",
    instructions="You are a helpful todo assistant",
    model="gpt-3.5-turbo",  # Or "ollama/mistral"
    tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats]
)
```

### 3. Running Agent

```python
result = Runner.run(agent, user_input)
print(result.final_output)
```

---

## Configuration

Edit `config.py` to change:

```python
# Change model
LLM_CONFIG = {
    "model": "gpt-4-turbo",  # More capable
    # OR
    "model": "gpt-3.5-turbo",  # Cheaper
    # OR for Ollama
    "model": "mistral",
}

# Change temperature (0.0 = deterministic, 1.0 = random)
"temperature": 0.3,  # Good for todos

# Change agent personality
AGENT_CONFIG = {
    "instructions": """Your custom instructions here..."""
}
```

---

## Testing

### Manual Test

```
You: Add task: Write report
Expected: Task created with ID

You: Show tasks
Expected: List with task and ID

You: Complete task 1
Expected: Marked as complete

You: Stats
Expected: Summary showing completed/incomplete counts
```

### Run All Operations

```
1. Add task: "Write report" (high priority)
2. Add task: "Review code" (normal priority)
3. Show all tasks
4. Complete task 1 by ID
5. Complete task 2 by description
6. Show remaining tasks
7. Get statistics
8. Delete a task
9. Verify deletion
```

---

## Troubleshooting

### "No module named 'openai'"

```bash
pip install -r requirements.txt
# OR
uv sync
```

### "OPENAI_API_KEY not set"

```bash
# Set environment variable
export OPENAI_API_KEY="sk-..."

# Then run
python main.py
```

### "Connection error to Ollama"

```bash
# Make sure Ollama is running in another terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### "Model not found"

```bash
ollama pull mistral     # Pull the model first
ollama list            # Verify it's installed
```

---

## Comparing Frameworks

| Aspect | CrewAI | OpenAI SDK | Google ADK |
|--------|--------|-----------|-----------|
| Complexity | Medium | **Simple** | Medium |
| Tool Definition | @tool | **@function_tool** | Typed functions |
| Returns | dicts | **JSON strings** | dicts |
| Config | YAML | **Python** | YAML |
| Multi-agent | **Yes** | Limited | Yes |
| MCP Support | No | No | **Yes** |

**OpenAI SDK** is best for:
- Simple, direct agent needs
- Learning agent basics
- Quick prototyping

---

## Architecture

```
User Input
    ↓
Agent (OpenAI SDK)
    ├─ Reads your message
    ├─ Chooses a tool
    ├─ Calls tool with parameters
    ├─ Receives result
    └─ Formats response
    ↓
Tools Layer
    ├─ add_todo()
    ├─ get_todos()
    ├─ complete_todo()
    ├─ delete_todo()
    └─ get_stats()
    ↓
Storage (JSON)
    └─ todos.json
```

---

## Next Steps

1. ✅ Run basic commands
2. ✅ Look at `tools.py` to understand tool structure
3. ✅ Modify `config.py` to change agent behavior
4. ✅ Add a new custom tool
5. ✅ Compare with CrewAI and Google ADK implementations
6. ✅ Try different Ollama models

---

## Advanced: Add Custom Tool

```python
# In tools.py
@function_tool
def search_todos(query: str) -> str:
    """Search todos by keyword"""
    results = storage.search_todos(query)
    return json.dumps({"results": results})

# In main.py
agent = Agent(
    ...
    tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats, search_todos]
)
```

---

## Key Differences from CrewAI

| CrewAI | OpenAI SDK |
|--------|-----------|
| Tasks + Agents | Just Agents |
| Orchestration layer | Direct tool calling |
| YAML config | Python config |
| `@tool` returns dict | `@function_tool` returns JSON string |
| More setup | Less setup |

---

## Resources

- **OpenAI API Docs:** https://platform.openai.com/docs
- **Ollama:** https://ollama.ai
- **Agent Concepts:** See `LEARNING.md` in parent directory

---

**Version:** 1.0.0  
**Last Updated:** 2026-08-20  
**Python:** 3.10+  

For detailed learning theory, see [LEARNING.md](../LEARNING.md)
