"""
LangGraph builder and management module
"""

from typing import List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model

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
        """Initialize the language model"""
        try:
            self.llm = init_chat_model(self.config.model_name)
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
    
    def _compile_graph(self) -> StateGraph:
        """Compile the graph"""
        try:
            return self._graph_builder.compile()
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
            
            # Process the message
            if self.tools:
                # Bind tools to the LLM so it can decide when to use them
                llm_with_tools = self.llm.bind_tools(self.tools)
                response = llm_with_tools.invoke(state["messages"])
            else:
                # Use LLM without tools
                response = self.llm.invoke(state["messages"])
            
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
