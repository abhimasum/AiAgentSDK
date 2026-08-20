# Google ADK Todo Manager

A simple todo management agent using **Google ADK 2.7** with **Ollama** (runs locally, no API key needed!).

**Recommended models:**
- **llama3.2** (2GB) - Fast, good function calling ✅
- **qwen2.5** (4.7GB) - More accurate, slower
- ❌ mistral - Does NOT support function calling properly

## 📁 Files (Only 4!)

```
GoogleADK/
├── agent.py          # Your AI agent (54 lines)
├── pyproject.toml    # Dependencies
├── todos.json        # Your todo data
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd GoogleADK
uv sync
```

### 2. Start Ollama

Make sure Ollama is running with llama3.2:

```bash
# Start Ollama server (if not running)
ollama serve

# Pull llama3.2 model (recommended, fast function calling)
ollama pull llama3.2

# OR pull qwen2.5 (more accurate but slower)
ollama pull qwen2.5

# Verify it's working
ollama run mistral "hello"
```

### 3. Run the Chat

```bash
uv run python chat.py
```

Then chat naturally with your AI assistant:
```
You: show me all my tasks
You: add a task to learn Python
You: mark task 1 as complete
You: give me statistics
You: quit
```

## 💡 Example Commands

```
"add a high priority task to finish the report"
"show me all my tasks"
"mark task 1 as complete"
"give me statistics"
"delete task 2"
```

## 🛠️ What's Inside

- **Model:** Ollama Mistral (runs locally)
- **Storage:** JSON file (todos.json)
- **No API key needed!**
- **Tools:** 5 functions
  - `add_todo` - Add new tasks
  - `get_todos` - List all tasks
  - `complete_todo` - Mark tasks complete
  - `delete_todo` - Remove tasks
  - `get_stats` - Get statistics

## ✅ Verify Setup

```bash
uv run python -c "from agent import root_agent; print(f'Agent ready: {root_agent.name}')"
```

Expected: `Agent ready: TodoManager`

## 📚 Learn More

- [Google ADK Docs](https://google.github.io/adk-docs/)
- [ADK GitHub](https://github.com/google/adk-python)
