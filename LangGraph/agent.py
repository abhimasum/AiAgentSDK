"""
LangGraph Todo Agent with State Graph

This module implements a stateful agent using LangGraph's StateGraph.
LangGraph uses a graph-based approach where:
- Nodes = Functions that process state
- Edges = Transitions between nodes
- State = Shared data structure passed between nodes

Key LangGraph Concepts:
1. **StateGraph**: Defines the flow of the agent
2. **State**: Shared data (messages, context) passed through nodes
3. **Nodes**: Functions that read/modify state
4. **Edges**: Define which node to execute next
5. **Conditional Edges**: Dynamic routing based on state

Agent Loop Flow:
User Input → Agent Node (LLM) → Tool Call? 
    ├─ Yes → Tool Node → Agent Node (verify)
    └─ No → End (return response)
"""

from typing import Annotated, Literal, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from tools import TOOLS


# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """
    State shared across all nodes in the graph.
    
    LangGraph passes this state through every node, allowing them to:
    - Read previous messages
    - Add new messages
    - Track conversation history
    
    The 'add_messages' annotation tells LangGraph to append messages
    rather than replacing them, maintaining conversation history.
    """
    messages: Annotated[list, add_messages]


# ============================================================================
# LLM SETUP WITH TOOL BINDING
# ============================================================================

def create_llm():
    """
    Create and configure the LLM with tool binding.
    
    Tool Binding Process:
    1. ChatOllama creates the LLM connection
    2. .bind_tools(TOOLS) attaches tool schemas to the LLM
    3. LLM receives tool names, descriptions, and parameter types
    4. LLM can now output tool calls in its responses
    
    Returns:
        LLM instance bound with tools
    """
    llm = ChatOllama(
        model="llama3.2",  # Use your preferred Ollama model
        temperature=0.1,   # Low temperature for consistent behavior
        base_url="http://localhost:11434"  # Ollama server
    )
    
    # Bind tools to LLM - this teaches the LLM what tools are available
    llm_with_tools = llm.bind_tools(TOOLS)
    
    return llm_with_tools


# ============================================================================
# NODE FUNCTIONS
# ============================================================================

def call_agent(state: AgentState) -> AgentState:
    """
    Agent Node: LLM processes messages and decides next action.
    
    This node:
    1. Receives current state (conversation history)
    2. Sends messages to LLM
    3. LLM analyzes and decides:
       - If it needs to call a tool (returns tool_calls)
       - If it can respond directly (returns text response)
    4. Appends LLM response to state
    
    Args:
        state: Current agent state with message history
        
    Returns:
        Updated state with LLM response added
    """
    llm = create_llm()
    
    # LLM processes all messages and generates response
    response = llm.invoke(state["messages"])
    
    # Add LLM response to state (includes tool_calls if any)
    return {"messages": [response]}


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Router: Decide if we need to call tools or end the conversation.
    
    This is a CONDITIONAL EDGE - it examines the state and returns
    the name of the next node to execute.
    
    Logic:
    - If last message has tool_calls → route to "tools" node
    - Otherwise → route to "end" (finish conversation)
    
    Args:
        state: Current agent state
        
    Returns:
        "tools" if tool calls exist, "end" otherwise
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check if LLM wants to call tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"  # Route to tool execution node
    
    return "end"  # No tools needed, finish


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_graph():
    """
    Build the LangGraph StateGraph.
    
    Graph Structure:
    
        START
          ↓
        agent (call_agent)
          ↓
    should_continue?
       ├─ tools → ToolNode → agent (verify result)
       └─ end → END
    
    Nodes:
    - agent: LLM reasoning and tool decision
    - tools: Execute tool calls and return results
    
    Edges:
    - START → agent: Begin with LLM
    - agent → should_continue: Conditional routing
    - tools → agent: After tool execution, LLM verifies
    
    Returns:
        Compiled graph ready for execution
    """
    # Initialize graph with state schema
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_agent)  # LLM reasoning node
    workflow.add_node("tools", ToolNode(TOOLS))  # Tool execution node
    
    # Add edges
    workflow.add_edge(START, "agent")  # Start at agent node
    
    # Conditional edge: agent decides next step
    workflow.add_conditional_edges(
        "agent",  # From agent node
        should_continue,  # Router function
        {
            "tools": "tools",  # If "tools" returned, go to tools node
            "end": END  # If "end" returned, finish
        }
    )
    
    # After tool execution, always go back to agent for verification
    workflow.add_edge("tools", "agent")
    
    # Compile graph into executable form
    return workflow.compile()


# ============================================================================
# AGENT INTERFACE
# ============================================================================

class TodoAgent:
    """
    High-level interface for the LangGraph Todo Agent.
    
    This class wraps the graph execution and provides a simple
    chat interface for interacting with the agent.
    """
    
    def __init__(self):
        """Initialize the agent by compiling the graph"""
        self.graph = create_graph()
    
    async def run(self, user_input: str) -> str:
        """
        Process user input through the agent graph.
        
        Execution Flow:
        1. Convert user input to HumanMessage
        2. Pass to graph starting at START node
        3. Graph executes: agent → (tools?) → agent → end
        4. Extract final response from state
        
        Args:
            user_input: User's natural language request
            
        Returns:
            Agent's final response as string
        """
        # Create initial state with user message
        initial_state = {
            "messages": [HumanMessage(content=user_input)]
        }
        
        # Execute graph (async streaming)
        final_state = None
        async for state in self.graph.astream(initial_state):
            final_state = state
        
        # Extract final response
        if final_state:
            # Get the last value from the state dict (contains "agent" or "tools" key)
            last_step = list(final_state.values())[-1]
            messages = last_step.get("messages", [])
            
            if messages:
                last_message = messages[-1]
                if isinstance(last_message, AIMessage):
                    return last_message.content
        
        return "I couldn't process that request."
    
    def visualize(self):
        """
        Generate a visual representation of the graph.
        
        Useful for understanding the agent's flow.
        Requires graphviz to be installed.
        """
        try:
            from IPython.display import Image, display
            display(Image(self.graph.get_graph().draw_mermaid_png()))
        except Exception as e:
            print(f"Visualization requires IPython and graphviz: {e}")
