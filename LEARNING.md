# 📚 AI Agent Todo Management System - Complete Learning Guide

Master the fundamentals of AI agents through building a practical todo management system.

---

## 📖 Table of Contents

1. [What is an AI Agent?](#what-is-an-ai-agent)
2. [System Architecture](#system-architecture)
3. [Core Concepts](#core-concepts)
4. [Agent Loop Workflow](#agent-loop-workflow)
5. [Sequence Diagrams](#sequence-diagrams)
6. [Framework Comparison](#framework-comparison)
7. [Implementation Patterns](#implementation-patterns)
8. [Key Takeaways](#key-takeaways)
9. [Glossary](#glossary)

---

## Overview

This project demonstrates building a **Todo Management Agent** using three different AI agent frameworks:
- **CrewAI** - Multi-agent framework with task orchestration
- **OpenAI Agents SDK** - Agent framework with tool orchestration
- **Google ADK** - Advanced agent framework with MCP support

All frameworks integrate with **Ollama** (local LLM) for privacy and cost-effectiveness.

### What is a Todo Management Agent?

An AI agent that autonomously manages todo items using:
- **Natural Language Processing** - Understand user intent
- **Tool Calling** - Execute actions (add, complete, retrieve todos)
- **Persistent Storage** - JSON-based todo database per folder
- **Agent Loop** - Continuous reasoning: understand → plan → act → verify

---

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                            │
│                   (Natural Language)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │      Agent Framework Layer         │
        │  (CrewAI/OpenAI/Google ADK)        │
        │  - Parse Intent                    │
        │  - Choose Tools                    │
        │  - Orchestrate Loop                │
        └────────────┬─────────────────────┘
                     │
        ┌────────────┴──────────────────┐
        │                               │
        ▼                               ▼
    ┌─────────────┐          ┌──────────────────┐
    │  LLM Engine │          │   Tool Layer     │
    │  (Ollama)   │          │  - add_todo()    │
    │             │          │  - complete_todo()
    │ Local       │          │  - get_todos()   │
    │ Private     │          │  - delete_todo() │
    └─────────────┘          └────────┬─────────┘
                                      │
                                      ▼
                             ┌─────────────────┐
                             │  Storage Layer  │
                             │  (JSON Files)   │
                             │  Per Folder     │
                             └─────────────────┘
```

### Folder Structure

```
AiAgentSDK/
├── LEARNING.md                    # This file
├── master_config.json             # Shared configuration
│
├── CrewAiADK/                     # CrewAI Implementation
│   ├── README.md                  # Setup & testing guide
│   ├── pyproject.toml             # uv dependencies
│   ├── requirements.txt           # pip dependencies
│   ├── todo_manager.py            # Main agent logic
│   ├── todo_storage.py            # JSON storage handler
│   ├── tools.py                   # Tool definitions
│   ├── config.yaml                # Agent configuration
│   ├── main.py                    # Entry point
│   └── todos.json                 # Todo database (generated)
│
├── OpenAiADK/                     # OpenAI Agent SDK
│   ├── README.md
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── todo_manager.py
│   ├── todo_storage.py
│   ├── tools.py
│   ├── config.py
│   ├── main.py
│   └── todos.json
│
├── GoogleADK/                     # Google ADK Implementation
│   ├── README.md
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── todo_manager.py
│   ├── todo_storage.py
│   ├── tools.py
│   ├── config.yaml
│   ├── main.py
│   └── todos.json
│
└── shared_utils/                  # Shared utilities
    ├── __init__.py
    └── common.py                  # Common functions
```

---

## Core Concepts

### 1. **Agent Loop**

The fundamental cycle any agent framework executes:

```
PERCEPTION → REASONING → ACTION → OBSERVATION → (repeat)
```

**In our Todo Agent:**
1. **Perception**: Parse user request ("Add task: write report")
2. **Reasoning**: LLM decides which tool to use (add_todo)
3. **Action**: Call tool with parameters (task="write report")
4. **Observation**: Receive result (task_id=123 created)
5. **Loop**: If goal not achieved, continue reasoning

### 2. **Tools / Functions**

A tool is a function the agent can call autonomously. The agent:
- Reads the tool's docstring (description)
- Reads parameter types (schema)
- Decides whether to call it based on user intent
- Receives the result and reasons about next steps

**Core Tools:**
```python
def add_todo(task: str, priority: str = "normal") -> dict
    """Add new todo item to the list"""
    
def get_todos(include_completed: bool = False) -> list
    """Retrieve all incomplete todos"""
    
def complete_todo(todo_id: int, description: str = None) -> dict
    """Mark todo as complete by ID or description"""
    
def delete_todo(todo_id: int) -> dict
    """Delete a todo permanently"""
```

### 3. **Storage Layer**

Todos are stored in **JSON files** per folder for:
- **Persistence**: Data survives agent restarts
- **Simplicity**: No database server needed
- **Portability**: Easy to backup/version control
- **Inspection**: Human-readable format

**Todo Schema:**
```json
{
  "todos": [
    {
      "id": 1,
      "task": "Write project report",
      "priority": "high",
      "created_at": "2026-08-20T10:30:00",
      "completed_at": null,
      "is_completed": false,
      "description": "Quarterly performance report"
    },
    {
      "id": 2,
      "task": "Review code",
      "priority": "normal",
      "created_at": "2026-08-20T11:00:00",
      "completed_at": "2026-08-20T14:00:00",
      "is_completed": true,
      "description": ""
    }
  ]
}
```

### 4. **LLM Integration (Ollama)**

Ollama provides:
- **Local Execution**: Run LLM on your machine (private)
- **No API Costs**: Free inference
- **Multiple Models**: llama2, mistral, neural-chat, etc.
- **Lightweight**: ~4GB disk for a model

**Why Ollama for Learning:**
- Understand agent reasoning without external API calls
- Experiment freely without costs
- Guaranteed consistent responses for testing

---

## Sequence Diagrams

### Scenario 1: Adding a Todo

```
User                 Agent              LLM              Tools             Storage
  │                   │                  │                 │                │
  ├─"Add task: Write report"──────┤                         │                │
  │                   │                  │                 │                │
  │                   ├─Parse input────>│                 │                │
  │                   │                  │                 │                │
  │                   │<─Decide tool─────┤                 │                │
  │                   │ (use add_todo)    │                 │                │
  │                   │                  │                 │                │
  │                   ├──Call add_todo(task="Write report")─>│                │
  │                   │                  │                 │                │
  │                   │                  │                 ├─Read todos.json─>│
  │                   │                  │                 │<────Load────────┤
  │                   │                  │                 │                │
  │                   │                  │                 ├─Generate ID─────┤
  │                   │                  │                 │ (id=5)          │
  │                   │                  │                 │                │
  │                   │                  │                 ├─Create entry────>│
  │                   │                  │                 │                │
  │                   │                  │                 ├─Write to JSON───>│
  │                   │<─Result: {"id":5, "task":"Write report", ...}│
  │                   │                  │                 │                │
  │                   ├─Verify success──>│                 │                │
  │                   │                  │                 │                │
  │<─"✅ Added: Write report (ID:5)"────┤                 │                │
```

### Scenario 2: Completing a Todo

```
User              Agent           LLM            Tools          Storage
  │                │               │              │              │
  ├─"Complete: Write report"──────┤               │              │
  │                │               │              │              │
  │                ├─Parse Input──>│              │              │
  │                │               │              │              │
  │                │<─Tool choice──┤              │              │
  │                │ (complete_todo)              │              │
  │                │               │              │              │
  │                ├─Search by description────────>│             │
  │                │               │              │              │
  │                │               │              ├─Load JSON────>│
  │                │               │              │<─todos data──┤
  │                │               │              │              │
  │                │               │              ├─Find match──┤│
  │                │               │ "Write report" found (id=5)
  │                │               │              │              │
  │                │               │              ├─Mark complete│
  │                │               │              │              │
  │                │               │              ├─Save JSON───>│
  │                │               │              │              │
  │                │<─Success result────────────────┤             │
  │                │                               │              │
  │<─"✅ Completed: Write report"────┤             │              │
```

### Scenario 3: Get Incomplete Todos

```
User          Agent        LLM           Tools        Storage
  │            │            │             │            │
  ├─"Show my tasks"────────┤             │            │
  │            │            │             │            │
  │            ├─Interpret─>│             │            │
  │            │            │             │            │
  │            │<─Use tool──┤             │            │
  │            │(get_todos) │             │            │
  │            │            │             │            │
  │            ├─Call get_todos(include_completed=False)──>│
  │            │            │             │            │
  │            │            │             ├─Read JSON──>│
  │            │            │             │<─Load──────┤
  │            │            │             │            │
  │            │            │             ├─Filter────┤│
  │            │            │             │ (is_completed=false)
  │            │            │             │            │
  │            │            │             ├─Return list│
  │            │<─[Task1, Task3, Task6]────┤             │
  │            │            │             │            │
  │<─Display formatted list─┤             │            │
  │  1. Write report        │             │            │
  │  2. Review code         │             │            │
  │  3. Deploy app          │             │            │
```

---

## Framework Comparison

| Aspect | CrewAI | OpenAI SDK | Google ADK |
|--------|--------|-----------|-----------|
| **Agent Model** | Multi-agent crews | Single/Multi agent | LlmAgent with tools |
| **Tool Definition** | @tool decorator | @function_tool | Typed functions |
| **Orchestration** | Task-based | Tool-based | Tool + MCP |
| **Config** | YAML files | Python dicts | YAML/Config classes |
| **Learning Curve** | Medium | Easy | Medium |
| **Best For** | Complex workflows | Simple orchestration | MCP integration |
| **Debugging** | CLI tools | OpenAI dashboard | Web console |
| **Cost** | Local LLM support | API-based | Flexible |

---

## Implementation Details

### 1. **Tool Definition Pattern**

**CrewAI:**
```python
@tool
def add_todo(task: str, priority: str = "normal") -> dict:
    """Add a new todo item"""
    storage = TodoStorage()
    return storage.add_todo(task, priority)
```

**OpenAI SDK:**
```python
@function_tool
def add_todo(task: str, priority: str = "normal") -> str:
    """Add a new todo item"""
    storage = TodoStorage()
    result = storage.add_todo(task, priority)
    return json.dumps(result)
```

**Google ADK:**
```python
def add_todo(task: str, priority: str = "normal") -> dict:
    """Add a new todo item"""
    storage = TodoStorage()
    return storage.add_todo(task, priority)

# Pass to agent: tools=[add_todo]
```

### 2. **Agent Initialization**

**CrewAI:**
```python
@agent
def todo_agent(self) -> Agent:
    return Agent(
        role="Todo Manager",
        goal="Manage todos effectively",
        backstory="You are a helpful todo assistant",
        tools=[add_todo, complete_todo, get_todos],
        llm=ChatOllama(model="mistral")
    )
```

**OpenAI SDK:**
```python
agent = Agent(
    name="TodoManager",
    instructions="You manage todos. Use tools to add, complete, and retrieve tasks.",
    tools=[add_todo, complete_todo, get_todos],
    model="gpt-4-turbo"  # or local via Ollama proxy
)
```

**Google ADK:**
```python
agent = LlmAgent(
    model="gemini-pro",  # or custom endpoint
    name="todo_manager",
    instruction="You manage todos using available tools",
    tools=[add_todo, complete_todo, get_todos]
)
```

### 3. **Storage Pattern**

All implementations use the same `TodoStorage` class:

```python
class TodoStorage:
    def __init__(self, filepath: str = "todos.json"):
        self.filepath = filepath
        self._ensure_file()
    
    def _ensure_file(self):
        """Create todos.json if it doesn't exist"""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({"todos": []}, f, indent=2)
    
    def add_todo(self, task: str, priority: str) -> dict:
        """Add new todo and return result"""
        data = self._load()
        new_id = max([t["id"] for t in data["todos"]], default=0) + 1
        todo = {
            "id": new_id,
            "task": task,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "is_completed": False
        }
        data["todos"].append(todo)
        self._save(data)
        return {"id": new_id, "status": "created", "task": task}
    
    def complete_todo(self, todo_id: int = None, description: str = None) -> dict:
        """Mark todo complete by ID or description"""
        data = self._load()
        
        # Search by ID or description
        for todo in data["todos"]:
            if (todo_id and todo["id"] == todo_id) or \
               (description and todo_id is None and description.lower() in todo["task"].lower()):
                todo["is_completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self._save(data)
                return {"status": "completed", "id": todo["id"], "task": todo["task"]}
        
        return {"status": "error", "message": "Todo not found"}
    
    def get_todos(self, include_completed: bool = False) -> list:
        """Get todos, optionally including completed ones"""
        data = self._load()
        if include_completed:
            return data["todos"]
        return [t for t in data["todos"] if not t["is_completed"]]
    
    def delete_todo(self, todo_id: int) -> dict:
        """Delete todo by ID"""
        data = self._load()
        original_count = len(data["todos"])
        data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
        
        if len(data["todos"]) < original_count:
            self._save(data)
            return {"status": "deleted", "id": todo_id}
        return {"status": "error", "message": "Todo not found"}
    
    def _load(self) -> dict:
        with open(self.filepath, 'r') as f:
            return json.load(f)
    
    def _save(self, data: dict):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
```

---

## Setup & Execution

### Prerequisites
1. **Ollama** installed and running
2. **Python 3.10+**
3. **uv** and/or **pip** for package management
4. **Git** (optional, for version control)

### Ollama Setup

```bash
# Install Ollama from https://ollama.ai

# Pull a model
ollama pull mistral      # Recommended for todo tasks
ollama pull llama2       # Alternative
ollama pull neural-chat  # Lightweight option

# Start Ollama (runs on localhost:11434)
ollama serve
```

### Package Management Approaches

**Using uv (Faster, Modern):**
```bash
cd CrewAiADK
uv sync                  # Install dependencies
uv run main.py          # Run the agent
```

**Using pip (Traditional):**
```bash
cd CrewAiADK
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Testing the Agent

Each framework has a dedicated README with testing instructions.

---

## Next Steps

1. Read the **README.md** in each framework folder
2. Install dependencies using your preferred method (uv or pip)
3. Start Ollama and pull a model
4. Run `main.py` in each framework
5. Interact with the todo agent via natural language
6. Examine `todos.json` to see persistent storage
7. Compare agent behavior across frameworks
8. Experiment with different prompts and Ollama models

---

## Key Takeaways

✅ **Agent Framework Pattern**: All frameworks follow the same loop (perceive → reason → act → observe)

✅ **Tool Calling**: Agents autonomously choose and call functions based on user intent

✅ **Persistent Storage**: JSON provides simple, portable todo storage

✅ **Local LLM**: Ollama enables free, private agent inference

✅ **Framework Diversity**: Different tools for different needs (CrewAI for complex, OpenAI for simple, Google for MCP)

✅ **Scalability**: Pattern can extend to complex multi-agent systems

---

## Glossary

| Term | Definition |
|------|-----------|
| **Agent** | AI system that perceives environment, reasons, takes actions |
| **Tool** | Function an agent can call to interact with the world |
| **LLM** | Large Language Model (brain of the agent) |
| **Ollama** | Local LLM runner (privacy + cost-effective) |
| **Orchestration** | Coordinating multiple agents/tools to achieve goals |
| **Persistence** | Data saved to disk (JSON in our case) |
| **Agent Loop** | Continuous cycle: perceive → reason → act → observe |
| **Schema** | Description of tool parameters (helps LLM choose tools) |

---

**Last Updated**: 2026-08-20  
**Difficulty Level**: Intermediate  
**Time to Complete**: 2-3 hours  

