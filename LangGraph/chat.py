"""
Interactive CLI for LangGraph Todo Agent

This module provides a rich terminal interface for chatting with the agent.
It handles:
- User input/output
- Error handling
- Visual formatting (rich library)
- Async execution
"""

import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from agent import TodoAgent

# Suppress OpenTelemetry errors (optional)
os.environ['OTEL_SDK_DISABLED'] = 'true'

# Rich console for beautiful terminal output
console = Console()


def print_banner():
    """Display welcome banner with agent info"""
    banner = """
    # 🤖 LangGraph Todo Agent
    
    **Using Ollama Qwen 2.5 7B (4.7GB)** - Optimized for tool calling
    
    ⚠️ **IMPORTANT**: This agent uses REAL tools - it only shows actual tasks from storage.
    It will NOT make up tasks. If you see empty results, you truly have no tasks.
    
    I can help you manage your todos:
    - Add tasks: "Add task: write report with high priority"
    - List tasks: "Show my tasks" or "List all tasks"
    - Complete tasks: "Mark write report as done" or "Complete task 1"
    - Delete tasks: "Delete todo #3"
    - Get stats: "How many tasks do I have?"
    
    Type 'exit' or 'quit' to exit.
    """
    console.print(Panel(Markdown(banner), border_style="blue"))


async def main():
    """Main chat loop"""
    print_banner()
    
    # Initialize agent
    try:
        agent = TodoAgent()
        console.print("[green]✓ Agent initialized successfully[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize agent: {e}[/red]")
        return
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Show processing indicator
            console.print("[dim]🤔 Processing...[/dim]", end="\r")
            
            # Get agent response
            response = await agent.run(user_input)
            
            # Clear processing indicator and show response
            console.print(" " * 50, end="\r")  # Clear line
            console.print(f"[bold green]Agent:[/bold green] {response}")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    # Run async main function
    asyncio.run(main())
