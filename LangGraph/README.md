# 🔷 LangGraph Todo Agent - Deep Dive Guide

## 📋 Table of Contents
1. [What is LangGraph?](#what-is-langgraph)
2. [Why LangGraph vs Other Frameworks](#why-langgraph-vs-other-frameworks)
3. [Core Concepts Explained](#core-concepts-explained)
4. [Installation & Setup](#installation--setup)
5. [Architecture Deep Dive](#architecture-deep-dive)
6. [Code Walkthrough](#code-walkthrough)
7. [Testing Guide](#testing-guide)
8. [Troubleshooting](#troubleshooting)

---

## What is LangGraph?

**LangGraph** is a framework for building **stateful, multi-actor applications** with LLMs. Unlike simple chat interfaces, LangGraph models agent behavior as a **graph of states and transitions**.

### Key Philosophy

```
Traditional Agent: User Input → LLM → Response
LangGraph Agent: User Input → State Graph → (Multiple LLM + Tool calls) → Response
```

**Think of it like a state machine:**
- **States**: Snapshots of the conversation + context
- **Nodes**: Functions that process and modify state
- **Edges**: Define which node runs next
- **Graph**: The complete flow of your agent

---

## Why LangGraph vs Other Frameworks?

| Framework | Best For | Complexity | Control |
|-----------|----------|------------|---------|
| **CrewAI** | Multi-agent teams | Medium | Task-based |
| **OpenAI SDK** | Simple tool calling | Low | Limited |
| **LangGraph** | Complex workflows | Medium-High | Full control |
| **Google ADK** | MCP integration | Medium | Moderate |

### When to Choose LangGraph

✅ **Use LangGraph when you need:**
- Complex multi-step reasoning
- State persistence across interactions
- Custom routing logic (conditional flows)
- Human-in-the-loop workflows
- Debugging visibility (inspect state at each step)

❌ **Don't use LangGraph for:**
- Simple one-shot tool calls (overkill)
- Non-stateful tasks (no state to manage)

---

## Core Concepts Explained

### 1. **State** 🗂️

State is the **shared data structure** passed through every node in the graph.

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
```

**Why `Annotated[list, add_messages]`?**
- `add_messages`: Special reducer that **appends** new messages instead of replacing
- Without it: Each node would overwrite previous messages
- With it: Conversation history is preserved

**What's in State?**
- `messages`: List of all conversation messages
  - `HumanMessage`: User input
  - `AIMessage`: LLM response (may include tool_calls)
  - `ToolMessage`: Tool execution results

### 2. **Nodes** ⚙️

Nodes are **functions that process state**.

```python
def call_agent(state: AgentState) -> AgentState:
    llm = create_llm()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

**Node Rules:**
1. **Input**: Receives current state
2. **Process**: Performs work (call LLM, execute logic)
3. **Output**: Returns dictionary with state updates
4. **Immutability**: Original state unchanged; returns new data

**Node Types:**
- **Agent Node** (`call_agent`): LLM reasoning
- **Tool Node** (`ToolNode`): Executes tool calls
- **Custom Nodes**: Any logic you need

### 3. **Edges** 🔗

Edges define **transitions between nodes**.

**Types:**

#### a) **Normal Edges** (Static)
```python
workflow.add_edge(START, "agent")  # Always go from START to agent
workflow.add_edge("tools", "agent")  # Always return to agent after tools
```

#### b) **Conditional Edges** (Dynamic)
```python
workflow.add_conditional_edges(
    "agent",  # From this node
    should_continue,  # Router function
    {
        "tools": "tools",  # If router returns "tools", go to tools node
        "end": END  # If router returns "end", finish
    }
)
```

**Router Function:**
```python
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"  # LLM wants to call tools
    return "end"  # No tools needed, finish
```

### 4. **Graph Flow** 🌊

Here's how our todo agent's graph executes:

```
┌─────────┐
│  START  │ (User: "Add task: write report")
└────┬────┘
     │
     ▼
┌─────────────┐
│   agent     │ LLM analyzes → Decides to call add_todo()
│ (call_agent)│ Returns: AIMessage with tool_calls
└────┬────────┘
     │
     ▼
┌──────────────┐ (Conditional Edge checks tool_calls)
│should_continue│ → Sees tool_calls → Returns "tools"
└────┬─────────┘
     │
     ▼
┌─────────────┐
│    tools    │ Executes add_todo(task="write report")
│ (ToolNode)  │ Returns: ToolMessage with result
└────┬────────┘
     │
     ▼
┌─────────────┐
│   agent     │ LLM verifies result
│ (call_agent)│ Returns: AIMessage "Added task successfully!"
└────┬────────┘
     │
     ▼
┌──────────────┐ (Conditional Edge checks tool_calls)
│should_continue│ → No tool_calls → Returns "end"
└────┬─────────┘
     │
     ▼
┌─────────┐
│   END   │ (Return response to user)
└─────────┘
```

---

## Installation & Setup

### Prerequisites

1. **Ollama** installed and running:
   ```bash
   # Install from https://ollama.ai
   ollama pull llama3.2  # Download model
   ollama serve          # Start server (localhost:11434)
   ```

2. **Python 3.10+**

### Install Dependencies

#### Using `uv` (Recommended - Faster)

```bash
cd LangGraph
uv sync                    # Install all dependencies
uv run python chat.py     # Run interactive agent
```

#### Using `pip` (Traditional)

```bash
cd LangGraph
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python chat.py
```

### Verify Installation

```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Run automated tests
uv run python automated_test.py
```

---

## Architecture Deep Dive

### File Structure

```
LangGraph/
├── pyproject.toml          # uv dependencies
├── requirements.txt        # pip dependencies
├── todo_storage.py         # JSON persistence layer
├── tools.py                # Tool definitions (add, complete, etc.)
├── agent.py                # LangGraph state graph
├── chat.py                 # Interactive CLI
├── automated_test.py       # Test suite
├── README.md               # This file
└── todos.json              # Generated: Todo database
```

### Component Breakdown

#### 1. **Storage Layer** (`todo_storage.py`)

**Responsibility**: Persist todos to JSON file

**Key Methods:**
```python
add_todo(task, priority)      # Create new todo
get_todos(include_completed)  # Retrieve todos
complete_todo(id/description) # Mark as done
delete_todo(id)               # Remove todo
get_stats()                   # Get counts
```

**Storage Format:**
```json
{
  "todos": [
    {
      "id": 1,
      "task": "write report",
      "priority": "high",
      "created_at": "2026-08-21T10:00:00",
      "completed_at": null,
      "is_completed": false,
      "description": ""
    }
  ]
}
```

#### 2. **Tools Layer** (`tools.py`)

**Responsibility**: Define functions the LLM can call

**How Tool Binding Works:**

1. **Define Function:**
   ```python
   def add_todo(task: str, priority: str = "normal") -> dict:
       """Add a new todo item"""  # LLM reads this!
       storage = TodoStorage()
       return storage.add_todo(task, priority)
   ```

2. **LangGraph Extracts Schema:**
   ```json
   {
     "name": "add_todo",
     "description": "Add a new todo item",
     "parameters": {
       "task": {"type": "string", "required": true},
       "priority": {"type": "string", "default": "normal"}
     }
   }
   ```

3. **LLM Decides:**
   - User: "Add task: write report"
   - LLM: "I should call add_todo(task='write report')"

4. **LangGraph Executes:**
   - Calls Python function
   - Returns result to LLM

#### 3. **Agent Layer** (`agent.py`)

**Responsibility**: Define state graph and execution flow

**Graph Construction:**

```python
def create_graph():
    workflow = StateGraph(AgentState)
    
    # Define nodes
    workflow.add_node("agent", call_agent)    # LLM reasoning
    workflow.add_node("tools", ToolNode(TOOLS))  # Tool execution
    
    # Define edges
    workflow.add_edge(START, "agent")  # Entry point
    
    # Conditional routing
    workflow.add_conditional_edges(
        "agent",
        should_continue,  # Router function
        {"tools": "tools", "end": END}
    )
    
    workflow.add_edge("tools", "agent")  # Loop back after tools
    
    return workflow.compile()
```

**State Management:**

- **Initial State**: `{"messages": [HumanMessage(content="user input")]}`
- **After Agent Node**: `{"messages": [..., AIMessage(tool_calls=[...])]}`
- **After Tool Node**: `{"messages": [..., ToolMessage(content="result")]}`
- **After Agent Verify**: `{"messages": [..., AIMessage(content="response")]}`

#### 4. **Interface Layer** (`chat.py`)

**Responsibility**: Provide user-friendly CLI

**Features:**
- Rich terminal formatting (colors, panels)
- Async execution (non-blocking)
- Error handling
- Exit commands

---

## Code Walkthrough

### Example: "Add task: write report"

Let's trace execution step-by-step:

#### Step 1: User Input → Initial State

```python
user_input = "Add task: write report"
initial_state = {
    "messages": [HumanMessage(content="Add task: write report")]
}
```

#### Step 2: Graph Execution Starts

Graph routes to **START → agent**

#### Step 3: Agent Node (`call_agent`)

```python
def call_agent(state: AgentState):
    llm = create_llm()  # LLM with tools bound
    response = llm.invoke(state["messages"])
    # LLM analyzes: "User wants to add todo, I'll call add_todo"
    # response = AIMessage(
    #     content="",
    #     tool_calls=[{
    #         "name": "add_todo",
    #         "args": {"task": "write report", "priority": "normal"}
    #     }]
    # )
    return {"messages": [response]}
```

**State after agent node:**
```python
{
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[{"name": "add_todo", ...}])
    ]
}
```

#### Step 4: Conditional Edge (`should_continue`)

```python
def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"  # Route to tools node
    return "end"
```

**Result**: Returns `"tools"` → Graph routes to tools node

#### Step 5: Tool Node Execution

```python
# ToolNode automatically:
# 1. Extracts tool_calls from last message
# 2. Calls add_todo(task="write report", priority="normal")
# 3. Receives result: {"id": 1, "status": "created", ...}
# 4. Creates ToolMessage with result
```

**State after tool node:**
```python
{
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[...]),
        ToolMessage(content='{"id": 1, "status": "created", ...}')
    ]
}
```

#### Step 6: Back to Agent Node (Verification)

Graph routes **tools → agent**

```python
def call_agent(state: AgentState):
    llm = create_llm()
    response = llm.invoke(state["messages"])
    # LLM sees ToolMessage result
    # Generates human-friendly response
    # response = AIMessage(content="✓ Added task: write report (ID: 1)")
    return {"messages": [response]}
```

**State after agent verification:**
```python
{
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[...]),
        ToolMessage(content='{"id": 1, ...}'),
        AIMessage(content="✓ Added task: write report (ID: 1)")
    ]
}
```

#### Step 7: Conditional Edge Again

```python
def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:  # No tool_calls this time
        return "tools"
    return "end"  # Route to END
```

**Result**: Returns `"end"` → Graph finishes

#### Step 8: Return Response

```python
# Extract final message
final_message = state["messages"][-1]
return final_message.content  # "✓ Added task: write report (ID: 1)"
```

---

## Testing Guide

### Automated Test Suite

```bash
uv run python automated_test.py
```

**What it tests:**
1. ✅ Add todo (default priority)
2. ✅ Add todo (high priority)
3. ✅ Add todo (low priority)
4. ✅ List todos
5. ✅ Complete todo by description
6. ✅ Get statistics
7. ✅ Complete todo (partial match)
8. ✅ List remaining todos
9. ✅ Delete todo
10. ✅ Final statistics

**Expected Output:**
```
🧪 LangGraph Todo Agent - Automated Test Suite
[Test 1] Add todo with default priority
✓ Response: Added task #1: learn python

[Test 2] Add todo with high priority
✓ Response: Added task #2: exercise (high priority)

...

✅ All tests completed!
```

### Interactive Testing

```bash
uv run python chat.py
```

**Try these commands:**

| User Input | Expected Behavior |
|------------|-------------------|
| `Add task: write report with high priority` | Creates todo with ID and priority |
| `Show my tasks` | Lists all incomplete todos |
| `What tasks do I have?` | Same as above (natural language) |
| `Mark write report as done` | Completes todo by description match |
| `Complete task 1` | Completes todo by ID |
| `Delete todo #3` | Permanently removes todo |
| `How many tasks do I have?` | Shows statistics |
| `exit` | Closes chat |

### Manual Testing

```python
# Test individual components
from todo_storage import TodoStorage

storage = TodoStorage()
result = storage.add_todo("test task", "high")
print(result)  # {'id': 1, 'status': 'created', ...}

todos = storage.get_todos()
print(todos)  # [{'id': 1, 'task': 'test task', ...}]
```

---

## Troubleshooting

### Common Issues

#### 1. **"Connection refused" Error**

**Problem**: Ollama server not running

**Solution**:
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

#### 2. **"Model not found" Error**

**Problem**: Model not downloaded

**Solution**:
```bash
# Download model
ollama pull llama3.2

# Verify available models
ollama list
```

#### 3. **"Module not found" Error**

**Problem**: Dependencies not installed

**Solution**:
```bash
# Using uv
uv sync

# Using pip
pip install -r requirements.txt
```

#### 4. **Agent Doesn't Call Tools**

**Problem**: LLM not understanding tool descriptions

**Solutions**:
1. Check tool docstrings are detailed
2. Try different Ollama model: `mistral`, `neural-chat`
3. Lower temperature in `agent.py`:
   ```python
   llm = ChatOllama(model="llama3.2", temperature=0.0)
   ```

#### 5. **Tools Return Errors**

**Problem**: JSON file corrupted or permissions issue

**Solution**:
```bash
# Delete and recreate
rm todos.json
python chat.py  # Will auto-create new file
```

#### 6. **Slow Response Time**

**Problem**: Model too large for your hardware

**Solutions**:
1. Use smaller model:
   ```bash
   ollama pull llama3.2:2b  # Smaller variant
   ```
2. Increase Ollama memory:
   ```bash
   export OLLAMA_NUM_GPU=0  # Use CPU only
   ```

---

## Advanced Topics

### Custom Routing Logic

Add more complex decision-making:

```python
def should_continue(state: AgentState) -> Literal["tools", "human", "end"]:
    last_message = state["messages"][-1]
    
    # Check for tool calls
    if last_message.tool_calls:
        return "tools"
    
    # Check if LLM is uncertain
    if "I'm not sure" in last_message.content:
        return "human"  # Route to human-in-the-loop node
    
    return "end"
```

### State Persistence

Save conversation history:

```python
import json

def save_state(state: AgentState, filepath: str):
    with open(filepath, 'w') as f:
        json.dump({
            "messages": [msg.dict() for msg in state["messages"]]
        }, f)

def load_state(filepath: str) -> AgentState:
    with open(filepath, 'r') as f:
        data = json.load(f)
    # Reconstruct messages from dict
    # ...
```

### Graph Visualization

```python
from agent import TodoAgent

agent = TodoAgent()
agent.visualize()  # Requires graphviz
```

---

## Key Takeaways

1. **LangGraph = State Machine**: Model agent behavior as a graph
2. **State**: Shared data structure passed through nodes
3. **Nodes**: Functions that process and modify state
4. **Edges**: Define transitions (static or conditional)
5. **Tool Binding**: LLM automatically calls Python functions
6. **Async Execution**: Use `async/await` for non-blocking operations

---

## Next Steps

1. ✅ Run automated tests
2. ✅ Try interactive chat
3. ✅ Read code comments in `agent.py`
4. ✅ Compare with CrewAI/OpenAI implementations
5. ✅ Experiment with custom routing logic
6. ✅ Try different Ollama models
7. ✅ Build your own graph-based agent!

---

**Last Updated**: 2026-08-21  
**Difficulty Level**: Intermediate  
**Estimated Time**: 2-3 hours  
**Prerequisites**: Basic Python, async/await, understanding of LLM tool calling
