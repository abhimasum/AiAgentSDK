"""
CrewAI Todo Manager Agent

This module defines the CrewAI agent that manages todo items.
The agent reads user requests in natural language and uses available tools
to perform todo operations.

Architecture:
- Agent: Responsible for understanding user intent and choosing tools
- Task: Represents a unit of work (managing todos)
- Crew: Orchestrates agent and tasks

LLM Integration:
- Uses Ollama for local, private inference
- Model: mistral (configurable in config.yaml)
- No external API calls needed
"""

import os
from pathlib import Path
from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms.ollama import OllamaLLM

# Import tools from tools.py
from tools import add_todo, get_todos, complete_todo, delete_todo, get_stats


class TodoManagerCrew(CrewBase):
    """
    Todo Management Crew using CrewAI Framework
    
    This class encapsulates the agent and task definitions for managing todos.
    CrewBase provides a structured way to define agents, tasks, and their relationships.
    
    Attributes:
        agents_config (str): Path to agents configuration file
        tasks_config (str): Path to tasks configuration file
    """
    
    # Configuration file paths (relative to this file's directory)
    agents_config = "config.yaml"
    tasks_config = "config.yaml"
    
    def __init__(self):
        """
        Initialize the TodoManagerCrew.
        
        Sets up the Ollama LLM connection which will be used by agents.
        """
        super().__init__()
        
        # Ollama LLM Configuration
        # Ollama runs on localhost:11434 by default
        # Make sure Ollama is running before starting the agent:
        # > ollama serve
        self.llm = OllamaLLM(
            model="mistral",              # Model name - must be pulled with: ollama pull mistral
            base_url="http://localhost:11434",  # Ollama server address
            temperature=0.3,              # Lower temperature for more deterministic responses
            verbose=True                  # Print debug information
        )
    
    @agent
    def todo_manager_agent(self) -> Agent:
        """
        Create the Todo Manager Agent.
        
        The agent is the AI entity that:
        1. Reads user input
        2. Understands intent
        3. Chooses appropriate tools
        4. Executes actions
        5. Reports results
        
        Returns:
            Agent: Configured CrewAI Agent for todo management
        
        Agent Characteristics:
        - Role: Todo Manager - understands task organization
        - Goal: Help users manage todos efficiently
        - Tools: add_todo, get_todos, complete_todo, delete_todo, get_stats
        - LLM: Ollama mistral (local, private)
        - Temperature: 0.3 (deterministic)
        """
        return Agent(
            # Load configuration from config.yaml
            config=self.agents_config["todo_manager_agent"],
            
            # Provide tools the agent can call
            # The agent will read tool docstrings to understand what they do
            tools=[add_todo, get_todos, complete_todo, delete_todo, get_stats],
            
            # Use Ollama LLM instead of default
            llm=self.llm,
            
            # Print agent's reasoning steps for debugging
            verbose=True
        )
    
    @task
    def manage_todos_task(self) -> Task:
        """
        Define the Todo Management Task.
        
        A Task in CrewAI represents a unit of work with:
        - Description: What needs to be done
        - Expected output: What success looks like
        - Agent: Who does the work
        
        Returns:
            Task: Configured task for managing todos
        
        Task Flow:
        1. User provides input (e.g., "Add a high priority task")
        2. Agent reads the configuration from config.yaml
        3. Agent chooses appropriate tool(s)
        4. Agent executes tool and gets result
        5. Agent provides formatted response to user
        """
        return Task(
            config=self.tasks_config["manage_todos_task"]
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Create and return the Crew.
        
        The Crew orchestrates agents and tasks together.
        It defines how agents work (sequentially in this case).
        
        Returns:
            Crew: Configured crew with agent and task
        
        Process Types in CrewAI:
        - Process.sequential: Execute tasks one after another (used here)
        - Process.hierarchical: One agent directs others
        """
        return Crew(
            # Agents in this crew
            agents=self.agents,
            
            # Tasks in this crew
            tasks=self.tasks,
            
            # Process: sequential = one task at a time
            process=Process.sequential,
            
            # Verbose output for debugging
            verbose=True
        )


def main():
    """
    Main entry point for the CrewAI Todo Agent.
    
    This function:
    1. Initializes the TodoManagerCrew
    2. Takes user input
    3. Runs the agent
    4. Displays results
    
    Prerequisites:
    - Ollama running (ollama serve)
    - Mistral model pulled (ollama pull mistral)
    
    Example Interactions:
    - "Add a high priority task: write quarterly report"
    - "Show me my tasks"
    - "Mark the report task as done"
    - "Delete task number 1"
    - "Give me a summary of my todos"
    """
    
    # Display welcome message
    print("=" * 60)
    print("🤖 CrewAI Todo Manager Agent")
    print("=" * 60)
    print("\nWelcome! I can help you manage your todos.")
    print("Commands examples:")
    print("  - Add a task: 'Add task: write report with high priority'")
    print("  - Show tasks: 'Show my incomplete tasks'")
    print("  - Complete task: 'Mark report as done' or 'Complete task 1'")
    print("  - Get stats: 'How many tasks do I have?'")
    print("  - Delete task: 'Remove task 1'")
    print("\nType 'quit' to exit.")
    print("=" * 60)
    
    try:
        # Initialize the crew
        crew_instance = TodoManagerCrew()
        
        # Main loop - keep asking for user input
        while True:
            try:
                # Get user input
                user_input = input("\n📝 You: ").strip()
                
                # Allow user to exit
                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("\n👋 Goodbye! Your todos have been saved.")
                    break
                
                # Skip empty input
                if not user_input:
                    print("Please enter a command.")
                    continue
                
                # Run the crew with user input
                print("\n🔄 Processing your request...\n")
                result = crew_instance.crew().kickoff(
                    inputs={"user_request": user_input}
                )
                
                # Display agent response
                print(f"\n🤖 Agent: {result}")
                
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print("\n\n⚠️ Interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'quit' to exit.")
    
    except ConnectionError:
        print("\n❌ ERROR: Cannot connect to Ollama!")
        print("\nPlease make sure:")
        print("1. Ollama is installed (https://ollama.ai)")
        print("2. Ollama is running: ollama serve")
        print("3. Mistral model is pulled: ollama pull mistral")
    
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        print("Check the logs above for more details.")


if __name__ == "__main__":
    main()
