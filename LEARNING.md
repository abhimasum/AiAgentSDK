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

This project demonstrates building a **Todo Management Agent** using four different AI agent frameworks:
- **CrewAI** - Multi-agent framework with task orchestration
- **OpenAI Agents SDK** - Agent framework with tool orchestration
- **Google ADK** - Advanced agent framework with MCP support
- **LangGraph** - State-based graph framework for complex workflows

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
├── LangGraph/                     # LangGraph Implementation
│   ├── README.md                  # Comprehensive guide
│   ├── pyproject.toml             # uv dependencies
│   ├── requirements.txt           # pip dependencies
│   ├── todo_storage.py            # JSON storage handler
│   ├── tools.py                   # Tool definitions
│   ├── agent.py                   # StateGraph implementation
│   ├── chat.py                    # Interactive CLI
│   ├── automated_test.py          # Test suite
│   └── todos.json                 # Todo database (generated)
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

| Aspect | CrewAI | OpenAI SDK | Google ADK | LangGraph |
|--------|--------|-----------|-----------|-----------|
| **Agent Model** | Multi-agent crews | Single/Multi agent | LlmAgent with tools | State-based graph |
| **Tool Definition** | @tool decorator | @function_tool | Typed functions | Regular functions |
| **Orchestration** | Task-based | Tool-based | Tool + MCP | Graph-based |
| **State Management** | Implicit | Implicit | Implicit | **Explicit** |
| **Config** | YAML files | Python dicts | YAML/Config classes | Python code |
| **Learning Curve** | Medium | Easy | Medium | **Medium-High** |
| **Best For** | Complex workflows | Simple orchestration | MCP integration | **Complex state flows** |
| **Debugging** | CLI tools | OpenAI dashboard | Web console | **State inspection** |
| **Flexibility** | Medium | Low | Medium | **Very High** |
| **Cost** | Local LLM support | API-based | Flexible | Local LLM support |

### Key Differentiators

#### CrewAI
- **Focus**: Teams of specialized agents working together
- **Strength**: Task delegation and role-based workflows
- **Use Case**: Complex projects requiring multiple expertise areas

#### OpenAI SDK
- **Focus**: Simple tool calling with minimal setup
- **Strength**: Easy integration with OpenAI models
- **Use Case**: Straightforward automation tasks

#### Google ADK
- **Focus**: MCP (Model Context Protocol) integration
- **Strength**: Standardized tool interfaces
- **Use Case**: Cross-platform agent deployments

#### LangGraph
- **Focus**: State machines and complex control flow
- **Strength**: Full control over agent reasoning and routing
- **Use Case**: Multi-step workflows with conditional logic, human-in-the-loop, debugging visibility

---

## LangGraph Deep Dive 🔷

### What Makes LangGraph Different?

LangGraph treats agent behavior as a **state machine** rather than a linear process. This paradigm shift enables:

1. **Explicit State Management**: State is a first-class citizen
2. **Complex Routing**: Conditional logic determines next steps
3. **Debugging Visibility**: Inspect state at any point in the graph
4. **Human-in-the-Loop**: Pause for human input at any node

### Core Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    LangGraph Agent                        │
│                                                           │
│  ┌─────────┐     ┌──────────┐     ┌──────────┐          │
│  │  State  │────▶│   Node   │────▶│  State'  │          │
│  │ (Input) │     │(Function)│     │ (Output) │          │
│  └─────────┘     └──────────┘     └──────────┘          │
│                        │                                  │
│                        │                                  │
│                   ┌────▼────┐                            │
│                   │  Edges  │ (Route to next node)       │
│                   └────┬────┘                            │
│                        │                                  │
│              ┌─────────┴─────────┐                       │
│              │                   │                       │
│         Static Edge        Conditional Edge              │
│        (Always goes)      (Decides based on state)       │
└──────────────────────────────────────────────────────────┘
```

### 1. State: The Foundation

**State is a TypedDict that flows through every node.**

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    State structure shared across all nodes.
    Think of it as the 'context' or 'memory' of the agent.
    """
    messages: Annotated[list, add_messages]
```

#### Why `Annotated[list, add_messages]`?

Without annotation:
```python
# Node 1 returns
{"messages": [Message1]}

# Node 2 returns
{"messages": [Message2]}

# Final state (WRONG - Message1 lost!)
{"messages": [Message2]}
```

With `add_messages` annotation:
```python
# Node 1 returns
{"messages": [Message1]}

# Node 2 returns
{"messages": [Message2]}

# Final state (CORRECT - both preserved)
{"messages": [Message1, Message2]}
```

**Key Point**: `add_messages` is a **reducer function** that tells LangGraph to **merge** lists instead of replacing them.

#### State Evolution Example

```python
# User input
state_0 = {
    "messages": [HumanMessage(content="Add task: write report")]
}

# After agent node (LLM decides to call tool)
state_1 = {
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[{"name": "add_todo", "args": {...}}])
    ]
}

# After tool node (tool executed)
state_2 = {
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[...]),
        ToolMessage(content='{"id": 1, "status": "created"}')
    ]
}

# After agent node (LLM verifies and responds)
state_3 = {
    "messages": [
        HumanMessage(content="Add task: write report"),
        AIMessage(tool_calls=[...]),
        ToolMessage(content='{"id": 1, "status": "created"}'),
        AIMessage(content="✓ Added task: write report")
    ]
}
```

### 2. Nodes: State Processors

**Nodes are functions that receive state, perform work, and return state updates.**

```python
def call_agent(state: AgentState) -> AgentState:
    """
    Agent node: LLM processes conversation and decides next action.
    
    Input: state with messages
    Processing: 
        - LLM analyzes conversation history
        - Decides whether to call tools or respond
    Output: state with new AI message added
    """
    llm = create_llm()  # LLM with tools bound
    response = llm.invoke(state["messages"])
    
    # Return state update (will be merged with existing state)
    return {"messages": [response]}
```

#### Node Rules

1. **Input**: Always receives `AgentState`
2. **Immutability**: Original state is never modified
3. **Output**: Returns dictionary with state updates
4. **Merging**: LangGraph merges output with existing state

#### Node Types in Our Agent

| Node | Purpose | Input | Output |
|------|---------|-------|--------|
| `agent` | LLM reasoning | Messages | AI response (text or tool_calls) |
| `tools` | Tool execution | AI tool_calls | Tool results (ToolMessage) |

### 3. Edges: Flow Control

Edges define **how state moves between nodes**.

#### A. Normal Edges (Static)

```python
workflow.add_edge(START, "agent")
# Meaning: Always start at "agent" node
```

```python
workflow.add_edge("tools", "agent")
# Meaning: After "tools" node, always go to "agent" node
```

#### B. Conditional Edges (Dynamic)

```python
workflow.add_conditional_edges(
    "agent",           # From this node
    should_continue,   # Router function decides next step
    {
        "tools": "tools",  # If router returns "tools", go to tools node
        "end": END         # If router returns "end", finish
    }
)
```

**Router Function:**
```python
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Examine state and decide which path to take.
    
    This is where you implement custom logic!
    """
    last_message = state["messages"][-1]
    
    # Decision logic
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"  # LLM wants to use tools
    
    return "end"  # No tools needed, we're done
```

### 4. Graph: The Complete Flow

**Graph = Nodes + Edges**

```python
def create_graph():
    # Initialize graph with state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes (functions that process state)
    workflow.add_node("agent", call_agent)
    workflow.add_node("tools", ToolNode(TOOLS))
    
    # Add edges (define flow)
    workflow.add_edge(START, "agent")  # Entry point
    
    # Conditional routing
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END}
    )
    
    # Loop back after tools
    workflow.add_edge("tools", "agent")
    
    # Compile graph
    return workflow.compile()
```

#### Visual Representation

```
     START
       │
       ▼
   ┌─────────┐
   │  agent  │ ◄──────────┐
   └────┬────┘            │
        │                 │
        │ (should_continue?)
        │                 │
    ┌───┴───┐             │
    │       │             │
    ▼       ▼             │
 tools     END            │
    │                     │
    └─────────────────────┘
```

### 5. Tool Binding in LangGraph

**How LangGraph connects tools to the LLM:**

#### Step 1: Define Tools

```python
def add_todo(task: str, priority: str = "normal") -> dict:
    """
    Add a new todo item.
    
    Args:
        task: Task description
        priority: Priority level (low/normal/high)
    
    Returns:
        Dictionary with id, status, and task
    """
    storage = TodoStorage()
    return storage.add_todo(task, priority)
```

#### Step 2: Extract Schema

LangGraph automatically extracts:
```json
{
  "name": "add_todo",
  "description": "Add a new todo item.",
  "parameters": {
    "type": "object",
    "properties": {
      "task": {"type": "string"},
      "priority": {
        "type": "string",
        "default": "normal"
      }
    },
    "required": ["task"]
  }
}
```

#### Step 3: Bind to LLM

```python
llm = ChatOllama(model="llama3.2")
llm_with_tools = llm.bind_tools([add_todo, get_todos, ...])
```

Now when you call `llm_with_tools.invoke(messages)`, the LLM:
1. Receives tool schemas
2. Analyzes user request
3. Returns either:
   - Text response: `AIMessage(content="...")`
   - Tool call: `AIMessage(tool_calls=[...])`

#### Step 4: Execute Tools

```python
# ToolNode automatically handles tool execution
tool_node = ToolNode([add_todo, get_todos, ...])

# When agent returns tool_calls, ToolNode:
# 1. Extracts tool_calls from AIMessage
# 2. Calls corresponding Python functions
# 3. Returns ToolMessage with results
```

### 6. Execution Flow: Complete Example

**User Input**: "Add task: write report with high priority"

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Initial State                                       │
│                                                              │
│ state = {                                                    │
│   "messages": [                                              │
│     HumanMessage("Add task: write report with high priority")│
│   ]                                                          │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Agent Node (call_agent)                             │
│                                                              │
│ - LLM receives messages                                      │
│ - Sees tool schemas (add_todo, get_todos, ...)              │
│ - Analyzes: "User wants to add todo with high priority"     │
│ - Decision: Call add_todo()                                  │
│                                                              │
│ Returns: AIMessage(                                          │
│   tool_calls=[{                                              │
│     "name": "add_todo",                                      │
│     "args": {"task": "write report", "priority": "high"}    │
│   }]                                                         │
│ )                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: State After Agent                                   │
│                                                              │
│ state = {                                                    │
│   "messages": [                                              │
│     HumanMessage("Add task: ..."),                          │
│     AIMessage(tool_calls=[...])  ← NEW                       │
│   ]                                                          │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Conditional Edge (should_continue)                  │
│                                                              │
│ - Checks last message for tool_calls                        │
│ - Finds: tool_calls exist                                   │
│ - Returns: "tools"                                          │
│ - Graph routes to tools node                                │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Tools Node (ToolNode)                               │
│                                                              │
│ - Extracts tool_calls from AIMessage                        │
│ - Calls: add_todo(task="write report", priority="high")    │
│ - Receives: {"id": 1, "status": "created", ...}            │
│                                                              │
│ Returns: ToolMessage(                                        │
│   content='{"id": 1, "status": "created", ...}'             │
│ )                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: State After Tools                                   │
│                                                              │
│ state = {                                                    │
│   "messages": [                                              │
│     HumanMessage("Add task: ..."),                          │
│     AIMessage(tool_calls=[...]),                            │
│     ToolMessage(content='{"id": 1, ...}')  ← NEW            │
│   ]                                                          │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼ (Edge: tools → agent)
┌─────────────────────────────────────────────────────────────┐
│ Step 7: Agent Node Again (Verification)                     │
│                                                              │
│ - LLM receives all messages (including ToolMessage)         │
│ - Sees tool result: {"id": 1, "status": "created", ...}    │
│ - Generates human-friendly response                         │
│                                                              │
│ Returns: AIMessage(                                          │
│   content="✓ Added task: write report (ID: 1, high priority)"│
│ )                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 8: Final State                                         │
│                                                              │
│ state = {                                                    │
│   "messages": [                                              │
│     HumanMessage("Add task: ..."),                          │
│     AIMessage(tool_calls=[...]),                            │
│     ToolMessage(content='{"id": 1, ...}'),                  │
│     AIMessage(content="✓ Added task: ...")  ← NEW           │
│   ]                                                          │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 9: Conditional Edge (should_continue)                  │
│                                                              │
│ - Checks last message for tool_calls                        │
│ - Finds: No tool_calls (just text response)                 │
│ - Returns: "end"                                            │
│ - Graph routes to END                                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 10: END                                                │
│                                                              │
│ - Extract final message content                             │
│ - Return to user: "✓ Added task: write report (ID: 1, ...)" │
└─────────────────────────────────────────────────────────────┘
```

### 7. Why LangGraph for Complex Workflows?

#### Scenario: Multi-step Research Agent

**Traditional Agent Problem:**
```
User: "Research competitors and create a report"

Agent: Calls search_tool() → Gets 100 results
       [Tries to process all at once, runs out of context]
       Returns: Incomplete response
```

**LangGraph Solution:**
```python
def create_research_graph():
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("search", search_competitors)
    workflow.add_node("filter", filter_relevant)
    workflow.add_node("analyze", analyze_data)
    workflow.add_node("report", generate_report)
    workflow.add_node("review", human_review)
    
    workflow.add_edge(START, "search")
    workflow.add_edge("search", "filter")
    workflow.add_edge("filter", "analyze")
    workflow.add_edge("analyze", "report")
    
    # Conditional: human review if confidence low
    workflow.add_conditional_edges(
        "report",
        check_confidence,
        {
            "review": "review",  # Low confidence → human review
            "end": END           # High confidence → done
        }
    )
    
    workflow.add_edge("review", END)
    
    return workflow.compile()
```

**Benefits:**
- Each step is isolated and testable
- State carries intermediate results
- Human can intervene at specific points
- Easy to debug (inspect state at each node)

### 8. Advanced Patterns

#### A. Parallel Execution

```python
# Execute multiple nodes in parallel
workflow.add_node("fetch_news", fetch_news)
workflow.add_node("fetch_social", fetch_social)
workflow.add_node("fetch_reports", fetch_reports)

# All fetch nodes run in parallel
workflow.add_edge(START, "fetch_news")
workflow.add_edge(START, "fetch_social")
workflow.add_edge(START, "fetch_reports")

# Merge results
workflow.add_node("merge", merge_results)
workflow.add_edge("fetch_news", "merge")
workflow.add_edge("fetch_social", "merge")
workflow.add_edge("fetch_reports", "merge")
```

#### B. Loops and Retries

```python
def should_retry(state: AgentState) -> Literal["retry", "end"]:
    """Retry if result not satisfactory"""
    if state["attempts"] < 3 and not state["success"]:
        return "retry"
    return "end"

workflow.add_conditional_edges(
    "process",
    should_retry,
    {
        "retry": "process",  # Loop back
        "end": END
    }
)
```

#### C. Human-in-the-Loop

```python
def wait_for_approval(state: AgentState) -> AgentState:
    """Pause and wait for human input"""
    print(f"Review this: {state['draft']}")
    approval = input("Approve? (yes/no): ")
    
    state["approved"] = (approval.lower() == "yes")
    return state

workflow.add_node("human_review", wait_for_approval)
```

### 9. Key Takeaways

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **State** | Shared data structure | Maintains context across nodes |
| **Nodes** | Functions that process state | Modular, testable logic |
| **Edges** | Define transitions | Control flow (static or conditional) |
| **Graph** | Nodes + Edges | Complete agent workflow |
| **Tool Binding** | LLM knows available functions | Autonomous tool calling |
| **Conditional Routing** | State-based decisions | Complex workflows |

### 10. When to Use LangGraph

✅ **Use LangGraph for:**
- Multi-step workflows with decision points
- Agents that need state persistence
- Complex routing logic
- Human-in-the-loop scenarios
- Debugging complex agent behavior
- Parallel execution needs

❌ **Don't use LangGraph for:**
- Simple one-shot tool calls
- Linear workflows without branching
- Stateless question-answering

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

**LangGraph:**
```python
def add_todo(task: str, priority: str = "normal") -> dict:
    """Add a new todo item"""
    storage = TodoStorage()
    return storage.add_todo(task, priority)

# Bind to LLM
llm = ChatOllama(model="llama3.2")
llm_with_tools = llm.bind_tools([add_todo, get_todos, ...])

# Use in ToolNode
tool_node = ToolNode([add_todo, get_todos, ...])
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

**LangGraph:**
```python
# Define state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Create graph
workflow = StateGraph(AgentState)

# Add nodes
def call_agent(state):
    llm = ChatOllama(model="llama3.2").bind_tools(TOOLS)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

workflow.add_node("agent", call_agent)
workflow.add_node("tools", ToolNode(TOOLS))

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,  # Router function
    {"tools": "tools", "end": END}
)
workflow.add_edge("tools", "agent")

# Compile
agent = workflow.compile()
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
| **State** | Shared data structure in LangGraph (conversation context) |
| **Node** | Function in LangGraph that processes state |
| **Edge** | Transition between nodes (static or conditional) |
| **Graph** | Complete workflow (nodes + edges) in LangGraph |
| **Reducer** | Function that merges state updates (e.g., `add_messages`) |
| **StateGraph** | LangGraph class for building stateful agents |
| **ToolNode** | LangGraph node that executes tool calls |
| **Conditional Edge** | Edge that routes based on state inspection |

---

**Last Updated**: 2026-08-20  
**Difficulty Level**: Intermediate  
**Time to Complete**: 2-3 hours  

