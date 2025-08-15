"""
LangSmith integration for monitoring and tracing LangGraph flows
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime

from config import ChatbotConfig
from logger import get_logger


class LangSmithMonitor:
    """LangSmith monitoring and tracing integration"""
    
    def __init__(self, config: ChatbotConfig):
        self.config = config
        self.logger = get_logger("LangSmithMonitor")
        self.tracer = None
        self.project_name = config.langsmith_project
        
        # Initialize LangSmith if enabled
        if config.enable_langsmith and config.langsmith_api_key:
            self._setup_langsmith()
        else:
            self.logger.warning("LangSmith monitoring disabled - no API key provided")
    
    def _setup_langsmith(self):
        """Set up LangSmith tracing"""
        try:
            # Set environment variables for LangSmith
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = self.config.langsmith_api_key
            os.environ["LANGCHAIN_PROJECT"] = self.project_name
            os.environ["LANGCHAIN_ENDPOINT"] = self.config.langsmith_endpoint
            
            # Import and initialize tracer
            from langsmith import Client
            from langchain_core.tracers import LangChainTracer
            
            self.client = Client()
            self.tracer = LangChainTracer(project_name=self.project_name)
            
            self.logger.info(f"LangSmith monitoring enabled for project: {self.project_name}")
            
        except ImportError:
            self.logger.error("LangSmith not installed. Install with: pip install langsmith")
            self.config.enable_langsmith = False
        except Exception as e:
            self.logger.error(f"Failed to setup LangSmith: {e}")
            self.config.enable_langsmith = False
    
    def start_trace(self, session_id: str = None) -> Optional[str]:
        """Start a new trace session"""
        if not self.config.enable_langsmith:
            return None
        
        try:
            if not session_id:
                session_id = f"chatbot_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create a new run
            from langsmith import RunTree
            
            run_tree = RunTree(
                name="LangGraph Chatbot Session",
                run_type="chain",
                inputs={"session_id": session_id},
                project_name=self.project_name
            )
            
            self.logger.info(f"Started LangSmith trace: {session_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to start trace: {e}")
            return None
    
    def log_node_execution(self, node_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any], 
                          session_id: str = None, metadata: Dict[str, Any] = None):
        """Log a node execution to LangSmith"""
        if not self.config.enable_langsmith:
            return
        
        try:
            from langsmith import RunTree
            
            run_tree = RunTree(
                name=f"Node: {node_name}",
                run_type="tool",
                inputs=inputs,
                outputs=outputs,
                metadata=metadata or {},
                project_name=self.project_name
            )
            
            self.logger.info(f"Logged {node_name} execution to LangSmith")
            
        except Exception as e:
            self.logger.error(f"Failed to log node execution: {e}")
    
    def log_tool_usage(self, tool_name: str, tool_input: str, tool_output: str, 
                      session_id: str = None):
        """Log tool usage to LangSmith"""
        if not self.config.enable_langsmith:
            return
        
        try:
            from langsmith import RunTree
            
            run_tree = RunTree(
                name=f"Tool: {tool_name}",
                run_type="tool",
                inputs={"query": tool_input},
                outputs={"result": tool_output},
                metadata={"tool_name": tool_name, "session_id": session_id},
                project_name=self.project_name
            )
            
            self.logger.info(f"Logged tool usage: {tool_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to log tool usage: {e}")
    
    def log_conversation_turn(self, user_input: str, assistant_response: str, 
                             session_id: str = None, turn_number: int = None):
        """Log a conversation turn to LangSmith"""
        if not self.config.enable_langsmith:
            return
        
        try:
            from langsmith import RunTree
            
            metadata = {
                "session_id": session_id,
                "turn_number": turn_number,
                "timestamp": datetime.now().isoformat()
            }
            
            run_tree = RunTree(
                name="Conversation Turn",
                run_type="chain",
                inputs={"user_input": user_input},
                outputs={"assistant_response": assistant_response},
                metadata=metadata,
                project_name=self.project_name
            )
            
            self.logger.info(f"Logged conversation turn {turn_number} to LangSmith")
            
        except Exception as e:
            self.logger.error(f"Failed to log conversation turn: {e}")
    
    def get_trace_url(self, run_id: str) -> str:
        """Get the URL for a specific trace"""
        if not self.config.enable_langsmith:
            return "LangSmith not enabled"
        
        try:
            base_url = self.config.langsmith_endpoint.replace("api.", "")
            return f"{base_url}/runs/{run_id}"
        except Exception as e:
            self.logger.error(f"Failed to generate trace URL: {e}")
            return "URL generation failed"
    
    def get_project_url(self) -> str:
        """Get the URL for the current project"""
        if not self.config.enable_langsmith:
            return "LangSmith not enabled"
        
        try:
            base_url = self.config.langsmith_endpoint.replace("api.", "")
            return f"{base_url}/projects/{self.project_name}"
        except Exception as e:
            self.logger.error(f"Failed to generate project URL: {e}")
            return "URL generation failed"
    
    def is_enabled(self) -> bool:
        """Check if LangSmith monitoring is enabled"""
        return self.config.enable_langsmith and self.config.langsmith_api_key != "dummy-key"
