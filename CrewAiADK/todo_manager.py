"""
CrewAI Todo Manager - Agent Definition Module

This module defines the TodoManagerCrew class which orchestrates the
CrewAI agent and task for managing todos.

The CrewBase pattern in CrewAI provides:
- Decorator-based agent and task definitions
- Automatic configuration loading from YAML
- Clean orchestration setup
- Extensible architecture for adding more agents/tasks
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms.ollama import OllamaLLM

from tools import add_todo, get_todos, complete_todo, delete_todo, get_stats


class TodoManagerCrew(CrewBase):
    """
    CrewAI Todo Management Crew
    
    A CrewBase subclass that defines agents and tasks for managing todos.
    CrewBase provides decorator-based agent/task definition with automatic
    YAML configuration loading.
    
    Architecture:
    - Inherits from CrewBase for structured agent setup
    - Uses @agent decorator for agent definitions
    - Uses @task decorator for task definitions
    - Uses @crew decorator to compose agents and tasks
    
    Attributes:
        agents_config (str): Path to agents configuration (config.yaml)
        tasks_config (str): Path to tasks configuration (config.yaml)
    """
    
    # Configuration file paths - CrewBase loads from these
    agents_config = "config.yaml"
    tasks_config = "config.yaml"
    
    def __init__(self):
        """
        Initialize TodoManagerCrew and setup the Ollama LLM connection.
        
        The Ollama LLM will be used by all agents in this crew.
        
        Prerequisites:
        - Ollama must be running: ollama serve
        - Model must be pulled: ollama pull mistral
        
        Raises:
            ConnectionError: If Ollama is not accessible at localhost:11434
        """
        super().__init__()
        
        # Initialize Ollama LLM for this crew
        # All agents will use this LLM unless overridden
        self.llm = OllamaLLM(
            model="mistral",                              # LLM model name
            base_url="http://localhost:11434",            # Ollama server URL
            temperature=0.3,                              # Lower = more deterministic
            verbose=True                                  # Print debug info
        )
    
    @agent
    def todo_manager_agent(self) -> Agent:
        """
        Define the Todo Manager Agent.
        
        This decorator-based method creates an Agent by loading configuration
        from config.yaml under the 'todo_manager_agent' key.
        
        The agent combines:
        - Configuration (role, goal, backstory) from YAML
        - Tools (functions it can call)
        - LLM (language model for reasoning)
        
        Returns:
            Agent: Fully configured agent ready to execute tasks
        
        Flow:
        1. @agent decorator intercepts this method
        2. Loads config from config.yaml["todo_manager_agent"]
        3. Combines with tools and LLM
        4. Returns ready-to-use Agent
        
        The agent will:
        - Understand user requests in natural language
        - Choose appropriate tools based on intent
        - Execute tools and process results
        - Generate human-readable responses
        """
        return Agent(
            # Load agent configuration from config.yaml
            # This includes: role, goal, backstory, model, temperature, etc.
            config=self.agents_config["todo_manager_agent"],
            
            # Provide tools the agent can use
            # Agent reads docstrings to understand what each tool does
            tools=[
                add_todo,           # Add new todo
                get_todos,          # List todos
                complete_todo,      # Mark as done
                delete_todo,        # Remove todo
                get_stats           # Get statistics
            ],
            
            # Use Ollama LLM (local, private, free)
            llm=self.llm,
            
            # Print agent's reasoning steps for debugging
            verbose=True
        )
    
    @task
    def manage_todos_task(self) -> Task:
        """
        Define the Todo Management Task.
        
        This decorator-based method creates a Task by loading configuration
        from config.yaml under the 'manage_todos_task' key.
        
        A Task represents a unit of work that the crew should accomplish.
        It defines:
        - What needs to be done (description)
        - What success looks like (expected_output)
        - Who does it (assigned agent)
        
        Returns:
            Task: Fully configured task ready to execute
        
        Flow:
        1. @task decorator intercepts this method
        2. Loads config from config.yaml["manage_todos_task"]
        3. Creates Task with description and expected output
        4. Automatically assigns to appropriate agent
        
        Task Purpose:
        - Accept user requests about todos
        - Orchestrate agent to handle the request
        - Return formatted response with confirmation
        
        Supported Requests:
        - "Add task: write report"
        - "Show my incomplete tasks"
        - "Mark task 1 as complete"
        - "Delete task 2"
        - "How many tasks do I have?"
        """
        return Task(
            # Load task configuration from config.yaml
            # This includes: description, expected_output, agent assignment
            config=self.tasks_config["manage_todos_task"]
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Create and return the complete Crew.
        
        The Crew orchestrates agents and tasks together.
        It defines how agents work collaboratively.
        
        In this simple example:
        - One agent (todo_manager_agent)
        - One task (manage_todos_task)
        - Sequential execution (one at a time)
        
        Returns:
            Crew: Fully configured crew ready to execute
        
        Flow:
        1. @crew decorator intercepts this method
        2. Collects all agents (self.agents)
        3. Collects all tasks (self.tasks)
        4. Sets execution process (sequential)
        5. Returns ready-to-run Crew
        
        Execution Model:
        - Process.sequential: Execute tasks one after another
        - Each task is handled by its assigned agent
        - Results flow from one task to the next
        
        Process.sequential Flow:
        Task 1 → Agent 1 executes → Output → Task 2 → Agent 2 executes → Output
        
        Alternative: Process.hierarchical (one agent directs others)
        Used for complex multi-agent workflows
        """
        return Crew(
            # All agents in this crew
            # Loaded by @agent decorators above
            agents=self.agents,
            
            # All tasks in this crew
            # Loaded by @task decorators above
            tasks=self.tasks,
            
            # Execution process: sequential (one task at a time)
            # Other option: Process.hierarchical (for complex coordination)
            process=Process.sequential,
            
            # Print detailed execution logs for debugging
            verbose=True
        )
