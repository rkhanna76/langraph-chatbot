"""
LangGraph builder and management module
"""

from typing import List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI

from config import ChatbotConfig
from state import State
from langsmith_integration import LangSmithMonitor


class GraphBuilder:
    """Handles the construction and management of the LangGraph"""
    
    def __init__(self, config: ChatbotConfig):
        self.config = config
        self.llm = None
        self.tools = []
        self.graph = None
        self.monitor = LangSmithMonitor(config)
        
    def build(self) -> StateGraph:
        """Build and return the compiled graph"""
        # Initialize the LLM
        self._init_llm()
        
        # Initialize tools
        self._init_tools()
        
        # Build the graph
        self._construct_graph()
        
        # Compile and return
        self.graph = self._compile_graph()
        return self.graph
    
    def _init_llm(self):
        """Initialize the LLM with system prompt"""
        try:
            from datetime import datetime
            
            # Get current date and time
            current_date = datetime.now().strftime("%B %d, %Y")
            current_time = datetime.now().strftime("%I:%M %p %Z")
            
            # Create system prompt with current date
            system_prompt = f"""You are a helpful AI assistant. 

IMPORTANT: Today's date is {current_date} and the current time is {current_time}. 
When users ask about "current", "today", "now", or similar time-related terms, 
always use the actual current date ({current_date}) and time ({current_time}), 
NOT the date when you were trained.

You have access to web search tools when needed to provide up-to-date information.
Always be helpful, accurate, and provide current information based on today's date."""

            self.llm = ChatOpenAI(
                model=self.config.model_name,
                temperature=0.7,  # Default temperature
                max_tokens=1000   # Default max tokens
            )
            
            # Store the system prompt for use in conversations
            self.system_prompt = system_prompt
            
            return self.llm
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")
    
    def _init_tools(self):
        """Initialize the tools for the graph"""
        if not self.config.enable_web_search:
            return
        
        try:
            # Initialize Tavily search tool
            search_tool = TavilySearch(
                max_results=self.config.max_search_results,
                api_key=self.config.tavily_api_key
            )
            self.tools = [search_tool]
        except Exception as e:
            print(f"Warning: Failed to initialize search tools: {e}")
            self.config.enable_web_search = False
            self.tools = []
    
    def _construct_graph(self):
        """Construct the graph structure"""
        # Create the state graph
        graph_builder = StateGraph(State)
        
        # Add the chatbot node with monitoring
        graph_builder.add_node("chatbot", self._chatbot_node_with_monitoring)
        
        # Add tools node if web search is enabled
        if self.config.enable_web_search and self.tools:
            # Use ToolNode but with a wrapper to control flow
            tool_node = ToolNode(tools=self.tools)
            graph_builder.add_node("tools", self._tools_node_with_monitoring)
            
            # Define the flow with conditional routing
            graph_builder.add_edge(START, "chatbot")
            
            # Add conditional edge from chatbot to tools or END
            graph_builder.add_conditional_edges(
                "chatbot",
                self._should_use_tools,
                {
                    "tools": "tools",
                    "end": END
                }
            )
            
            # Tools always go back to chatbot for final response
            graph_builder.add_edge("tools", "chatbot")
            
        else:
            # Simple flow without tools: START -> chatbot -> END
            graph_builder.add_edge(START, "chatbot")
            graph_builder.add_edge("chatbot", END)
        
        self._graph_builder = graph_builder
    
    def _compile_graph(self):
        """Compile the graph"""
        try:
            memory = InMemorySaver()
            return self._graph_builder.compile(
                checkpointer=memory
            )
        except Exception as e:
            raise RuntimeError(f"Failed to compile graph: {e}")
    
    def _chatbot_node_with_monitoring(self, state: State) -> Dict[str, Any]:
        """Process messages through the LLM with monitoring"""
        try:
            # Log the input to LangSmith
            self.monitor.log_node_execution(
                node_name="chatbot",
                inputs={"messages": str(state["messages"])},
                outputs={},
                metadata={"node_type": "chatbot", "timestamp": "start"}
            )
            
            # Add system message with current date if not already present
            from langchain_core.messages import SystemMessage
            messages = state["messages"]
            
            # Check if system message is already present
            has_system_message = any(
                hasattr(msg, 'type') and msg.type == 'system' 
                for msg in messages
            )
            
            if not has_system_message and hasattr(self, 'system_prompt'):
                # Add system message at the beginning
                system_message = SystemMessage(content=self.system_prompt)
                messages = [system_message] + messages
            
            # Process the message
            if self.tools:
                # Bind tools to the LLM so it can decide when to use them
                llm_with_tools = self.llm.bind_tools(self.tools)
                response = llm_with_tools.invoke(messages)
            else:
                # Use LLM without tools
                response = self.llm.invoke(messages)
            
            result = {"messages": [response]}
            
            # Log the output to LangSmith
            self.monitor.log_node_execution(
                node_name="chatbot",
                inputs={"messages": str(state["messages"])},
                outputs={"response": str(response)},
                metadata={"node_type": "chatbot", "timestamp": "end"}
            )
            
            return result
            
        except Exception as e:
            # Log error to LangSmith
            self.monitor.log_node_execution(
                node_name="chatbot",
                inputs={"messages": str(state["messages"])},
                outputs={"error": str(e)},
                metadata={"node_type": "chatbot", "error": True}
            )
            
            # Fallback to simple response on error
            print(f"Error in chatbot node: {e}")
            return {"messages": [{"role": "assistant", "content": "I encountered an error. Please try again."}]}
    
    def _tools_node_with_monitoring(self, state: State) -> Dict[str, Any]:
        """Execute tools with monitoring"""
        try:
            # Log the input to LangSmith
            self.monitor.log_node_execution(
                node_name="tools",
                inputs={"messages": str(state["messages"])},
                outputs={},
                metadata={"node_type": "tools", "timestamp": "start"}
            )
            
            # Use the standard ToolNode
            tool_node = ToolNode(tools=self.tools)
            result = tool_node.invoke(state)
            
            # Log the output to LangSmith
            self.monitor.log_node_execution(
                node_name="tools",
                inputs={"messages": str(state["messages"])},
                outputs={"result": str(result)},
                metadata={"node_type": "tools", "timestamp": "end"}
            )
            
            return result
            
        except Exception as e:
            # Log error to LangSmith
            self.monitor.log_node_execution(
                node_name="tools",
                inputs={"messages": str(state["messages"])},
                outputs={"error": str(e)},
                metadata={"node_type": "tools", "error": True}
            )
            
            print(f"Error in tools node: {e}")
            return state
    
    def _should_use_tools(self, state: State) -> str:
        """Determine if tools should be used based on the last message"""
        try:
            if not state["messages"]:
                return "end"
            
            last_message = state["messages"][-1]
            
            # Only route to tools if the message explicitly contains tool calls
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            
            # Otherwise, end the conversation
            return "end"
            
        except Exception as e:
            print(f"Error in tool routing: {e}")
            return "end"
    
    def get_llm(self):
        """Get the initialized LLM"""
        return self.llm
    
    def get_tools(self):
        """Get the initialized tools"""
        return self.tools
    
    def get_monitor(self):
        """Get the LangSmith monitor"""
        return self.monitor
