# 🤖 AI Agent Todo Management System

**Learn AI agents by building a practical todo manager with 3 frameworks - All FREE with Ollama!** 🦙

---

## ✨ What's New

**🎉 All 3 frameworks now use Ollama (100% FREE, no API keys!):**
- ✅ **Google ADK** - Simple & fast
- ✅ **OpenAI SDK** - OpenAI-compatible patterns  
- ✅ **CrewAI** - Multi-agent orchestration

**No credit cards, no API keys, runs completely locally!** 🆓🔒

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Install Ollama**
```bash
# Download from: https://ollama.ai
# Or Windows: winget install Ollama.Ollama
```

### **Step 2: Get the Model**
```bash
ollama pull llama3.2
ollama serve
```

### **Step 3: Run Any Framework**
```bash
# Google ADK (Simplest)
cd GoogleADK && uv sync && uv run python chat.py

# OpenAI SDK (OpenAI-compatible)
cd OpenAiADK && uv sync && uv run python chat.py

# CrewAI (Multi-agent)
cd CrewAiADK && uv sync && uv run python chat.py
```

**That's it!** Start chatting with your AI todo assistant! 🎯

---

## 📚 Documentation

### **Start Here:**
1. **[OLLAMA_SETUP.md](OLLAMA_SETUP.md)** - Setup guide for all frameworks (10 min)
2. **[MULTI_FRAMEWORK_GUIDE.md](MULTI_FRAMEWORK_GUIDE.md)** - Compare frameworks
3. **[TEST_RESULTS.md](TEST_RESULTS.md)** - Validation & test results

### **Framework Guides:**
- **[GoogleADK/README.md](GoogleADK/README.md)** - Google ADK setup
- **[OpenAiADK/README.md](OpenAiADK/README.md)** - OpenAI SDK setup
- **[CrewAiADK/README.md](CrewAiADK/README.md)** - CrewAI setup

---

## 🎯 Which Framework Should I Use?

| Framework | Best For | Speed | Complexity | API Cost |
|-----------|----------|-------|------------|----------|
| **Google ADK** | Learning, prototyping | ⚡ Fast | ⭐ Easy | 🆓 FREE |
| **OpenAI SDK** | OpenAI patterns | ⚡ Fast | ⭐⭐ Medium | 🆓 FREE |
| **CrewAI** | Multi-agent systems | 🐢 Slower | ⭐⭐⭐ Complex | 🆓 FREE |

**All use Llama 3.2 (2GB) - same model, different frameworks!**

---

## 🦙 Ollama Integration

### **How Each Framework Uses Ollama:**

**Google ADK** (via LiteLLM):
```python
Agent(model="ollama_chat/llama3.2", ...)
```

**OpenAI SDK** (OpenAI-compatible endpoint):
```python
OpenAI(base_url="http://localhost:11434/v1", ...)
```

**CrewAI** (via LLM wrapper):
```python
LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
```

---

## 📦 Project Structure

By default, GoogleADK uses Ollama. Others can be configured to use it.

---

## 📖 Learning Paths

### 👶 Absolute Beginner (2 hours)
1. Read **LEARNING.md** - Understand concepts (30 min)
2. Run **OpenAI SDK** - Simplest framework (20 min)
3. Test all operations (15 min)
4. Try **CrewAI** (20 min)
5. Try **Google ADK** (20 min)
6. Experiment & customize (15 min)

### 👨‍💻 Developer (1.5 hours)
1. Read **LEARNING.md** - Theory (20 min)
2. Try all 3 frameworks (60 min)
3. Customize configuration (15 min)
4. Add new tools (10 min)

### 🏭 Production (3+ hours)
1. Deep study of **LEARNING.md**
2. Read all 3 framework READMEs
3. Choose best framework
4. Customize thoroughly
5. Plan deployment

---

## 🎯 What Each Framework README Includes

Each framework folder (OpenAiADK, CrewAiADK, GoogleADK) has a **README.md** with:

✅ Complete setup instructions  
✅ Installation with pip & uv  
✅ Configuration guide  
✅ Testing procedures  
✅ Troubleshooting (20+ scenarios)  
✅ Code explanations  
✅ Example interactions  

---

## 🌟 Features

### Todo Operations
- ✅ Add todo (with priority)
- ✅ Get todos (incomplete/all)
- ✅ Complete todo (by ID or description)
- ✅ Delete todo
- ✅ Search todos
- ✅ Get statistics

### LLM Support
- ✅ **Ollama** - Local, free, private (DEFAULT)
- ✅ **OpenAI** - Cloud API
- ✅ **Google Gemini** - Cloud API (free tier)

### Package Managers
- ✅ **pip** - Traditional (requirements.txt)
- ✅ **uv** - Modern, faster (pyproject.toml)

---

## 🏗️ Project Structure

```
AiAgentSDK/
├── LEARNING.md                    # Theory & concepts
├── README.md                      # This file
│
├── OpenAiADK/                     # Simplest ⭐
│   ├── README.md                  # Setup guide
│   ├── main.py
│   ├── tools.py
│   └── config.py
│
├── CrewAiADK/                     # Production-grade
│   ├── README.md
│   ├── main.py
│   ├── tools.py
│   └── config.yaml
│
├── GoogleADK/                     # Advanced (Ollama default)
│   ├── README.md
│   ├── main.py
│   ├── tools.py
│   └── config.yaml
│
└── shared_utils/
    └── todo_storage.py            # Shared JSON storage
```

---

## ❓ Common Questions

### Which framework should I use?
- **Learning?** → OpenAI SDK ⭐
- **Production?** → CrewAI
- **Advanced?** → Google ADK

### Can I use Ollama?
- **Yes!** All frameworks support Ollama
- **Google ADK uses it by default** (free, local, private)
- Edit config to switch to OpenAI/Google APIs

### How long to get started?
- **Installation:** 5 minutes
- **First agent running:** 10 minutes
- **Understand theory:** 30 minutes
- **Complete understanding:** 2-3 hours

---

## 🆘 Quick Troubleshooting

### Ollama connection error
```bash
# Make sure Ollama is running
ollama serve
```

### Module not found
```bash
# Reinstall
pip install -r requirements.txt
```

### Model not found
```bash
# Download model
ollama pull mistral
```

For more help, see your framework's **README.md** → Troubleshooting section

---

## 📝 Example Interactions

```
You: Add a high priority task: write report
🤖: ✅ Added 'write report' (HIGH) - ID: 1

You: Show my tasks
🤖: 📋 Your tasks:
     1. write report [HIGH]

You: Mark task 1 as complete
🤖: ✅ Completed 'write report'

You: quit
🤖: 👋 Goodbye!
```

---

## 🎓 What You'll Learn

✅ How AI agents work  
✅ Agent loop pattern  
✅ Tool calling mechanism  
✅ 3 different frameworks  
✅ Local vs cloud LLMs  
✅ JSON persistence  
✅ Production patterns  

---

## 🔗 Documentation Files

- **LEARNING.md** - Everything about agent theory, all frameworks, patterns
- **OpenAiADK/README.md** - Setup & test OpenAI SDK
- **CrewAiADK/README.md** - Setup & test CrewAI
- **GoogleADK/README.md** - Setup & test Google ADK (with Ollama)

---

## 🚀 Start Now

```bash
# 1. Pick a framework
cd OpenAiADK

# 2. Install
pip install -r requirements.txt

# 3. Run
python main.py

# 4. Try: "Add task: hello"
```

**That's it! Agent running in ~15 minutes** ⏱️

---

## 💡 Pro Tips

1. **Read LEARNING.md first** - Understand concepts deeply
2. **Use Ollama** - Free, local, private
3. **Try all 3 frameworks** - See differences
4. **Customize personality** - Edit agent instruction in config
5. **Extend with tools** - Add new functions to tools.py
6. **Check todos.json** - See JSON persistence
7. **Run tests** - Each README has test procedures

---

**Ready to learn? Start with LEARNING.md or pick a framework and run it!** 🎉
