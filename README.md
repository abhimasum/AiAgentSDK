# 🤖 AI Agent Todo Management System

Learn AI agents by building a practical todo management system with three frameworks.

---

## 📚 Essential Documentation (4 Documents Only)

1. **LEARNING.md** - Complete theory & concepts (read first for understanding)
2. **CrewAiADK/README.md** - CrewAI setup & testing guide
3. **OpenAiADK/README.md** - OpenAI SDK setup & testing guide  
4. **GoogleADK/README.md** - Google ADK with Ollama setup & testing guide

---

## 🚀 Quick Start (10 minutes)

### Step 1: Choose Your Framework

| Framework | Best For | Setup | Difficulty |
|-----------|----------|-------|------------|
| **OpenAI SDK** | Learning | 10 min | Easy ⭐ |
| **CrewAI** | Production | 15 min | Medium |
| **Google ADK** | Advanced | 15 min | Medium |

### Step 2: Install & Run

```bash
# Pick one framework
cd OpenAiADK    # Start here (easiest)

# Install dependencies
pip install -r requirements.txt
# OR: uv sync

# Run the agent
python main.py

# Try: "Add task: learn AI agents"
```

### Step 3: Run Ollama (Optional but Recommended - Free & Private)

```bash
# Terminal 1: Start Ollama (free, local, private)
ollama serve

# Terminal 2: Pull a model
ollama pull mistral  # or: llama2, neural-chat
```

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
