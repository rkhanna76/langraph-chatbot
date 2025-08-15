"""
Main chatbot core implementation
"""

import time
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph

from config import ChatbotConfig
from graph_builder import GraphBuilder
from visualization import GraphVisualizer
from chat_interface import ChatInterface
from state import State
from logger import get_logger


class LangGraphChatbot:
    """Main chatbot class that integrates all components"""
    
    def __init__(self, config: Optional[ChatbotConfig] = None):
        """Initialize the chatbot with configuration"""
        self.logger = get_logger("ChatbotCore")
        
        # Load configuration
        if config is None:
            try:
                config = ChatbotConfig.from_env()
                config.validate()
            except Exception as e:
                self.logger.error(f"Configuration error: {e}")
                raise
        
        self.config = config
        self.logger.info("Configuration loaded successfully")
        
        # Initialize components
        self._init_components()
        
        # Build the graph
        self._build_graph()
        
        # Initialize session tracking
        self.current_session_id = None
        self.turn_count = 0
        
        self.logger.info("Chatbot initialized successfully")
    
    def _init_components(self):
        """Initialize all chatbot components"""
        try:
            # Initialize graph builder
            self.graph_builder = GraphBuilder(self.config)
            self.logger.info("Graph builder initialized")
            
            # Initialize visualizer
            self.visualizer = GraphVisualizer(
                output_dir=".",
                formats=self.config.visualization_formats
            )
            self.logger.info("Visualizer initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _build_graph(self):
        """Build the LangGraph"""
        try:
            start_time = time.time()
            self.graph = self.graph_builder.build()
            build_time = time.time() - start_time
            
            self.logger.log_graph_operation("build", True, f"took {build_time:.2f}s")
            
        except Exception as e:
            self.logger.log_graph_operation("build", False, str(e))
            raise RuntimeError(f"Failed to build graph: {e}")
    
    def start_session(self, session_id: str = None) -> str:
        """Start a new conversation session with LangSmith tracking"""
        self.current_session_id = self.graph_builder.get_monitor().start_trace(session_id)
        self.turn_count = 0
        
        if self.current_session_id:
            self.logger.info(f"Started new session: {self.current_session_id}")
            print(f"🔗 LangSmith session: {self.current_session_id}")
            print(f"📊 Monitor at: {self.graph_builder.get_monitor().get_project_url()}")
        
        return self.current_session_id
    
    def generate_visualizations(self) -> Dict[str, Optional[str]]:
        """Generate and save graph visualizations"""
        if not self.config.save_visualizations:
            self.logger.info("Visualization generation disabled")
            return {}
        
        try:
            self.logger.info("Generating graph visualizations...")
            
            # Clean up old visualizations
            self.visualizer.cleanup_old_visualizations()
            
            # Generate new visualizations
            results = self.visualizer.generate_visualizations(self.graph)
            
            # Log results
            successful_formats = [fmt for fmt, result in results.items() if result]
            if successful_formats:
                self.logger.info(f"Generated visualizations: {', '.join(successful_formats)}")
            else:
                self.logger.warning("No visualizations were generated successfully")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to generate visualizations: {e}")
            return {}
    
    def stream_response(self, user_input: str) -> None:
        """Stream the chatbot response for given user input"""
        try:
            start_time = time.time()
            self.turn_count += 1
            
            # Log conversation turn to LangSmith
            monitor = self.graph_builder.get_monitor()
            monitor.log_conversation_turn(
                user_input=user_input,
                assistant_response="",  # Will be updated after response
                session_id=self.current_session_id,
                turn_number=self.turn_count
            )
            
            # Process the input through the graph
            assistant_response = ""
            for event in self.graph.stream({"messages": [{"role": "user", "content": user_input}]}):
                for value in event.values():
                    if "messages" in value and value["messages"]:
                        # Get the last message from the response
                        messages = value["messages"]
                        if messages and hasattr(messages[-1], 'content'):
                            response = messages[-1]
                            assistant_response = response.content
                            print("🤖 Assistant:", response.content)
                        elif messages and isinstance(messages[-1], dict) and 'content' in messages[-1]:
                            response = messages[-1]
                            assistant_response = response['content']
                            print("🤖 Assistant:", response['content'])
                    
                    # Log the response
                    response_time = time.time() - start_time
                    self.logger.log_api_call("OpenAI", True, response_time)
            
            # Update the conversation turn with the actual response
            if assistant_response:
                monitor.log_conversation_turn(
                    user_input=user_input,
                    assistant_response=assistant_response,
                    session_id=self.current_session_id,
                    turn_number=self.turn_count
                )
            
        except Exception as e:
            self.logger.error(f"Error processing response: {e}")
            print(f"❌ Error: {e}")
            print("🔄 Please try again.")
    
    def run_interactive(self) -> None:
        """Run the chatbot in interactive mode"""
        try:
            # Start a new session
            self.start_session()
            
            # Create chat interface
            chat_interface = ChatInterface(
                stream_handler=self.stream_response,
                max_turns=self.config.max_conversation_turns
            )
            
            # Run the interface
            chat_interface.run_interactive()
            
            # Log session summary
            self.logger.info(f"Interactive session ended after {self.turn_count} turns")
            
        except Exception as e:
            self.logger.error(f"Error in interactive mode: {e}")
            raise
    
    def get_graph(self) -> StateGraph:
        """Get the compiled graph"""
        return self.graph
    
    def get_config(self) -> ChatbotConfig:
        """Get the current configuration"""
        return self.config
    
    def get_monitor(self):
        """Get the LangSmith monitor"""
        return self.graph_builder.get_monitor()
    
    def update_config(self, **kwargs):
        """Update configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Updated config: {key} = {value}")
            else:
                self.logger.warning(f"Unknown config key: {key}")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the chatbot"""
        health_status = {
            "status": "healthy",
            "config_loaded": True,
            "graph_built": self.graph is not None,
            "components_initialized": True,
            "langsmith_enabled": self.get_monitor().is_enabled(),
            "errors": []
        }
        
        try:
            # Check configuration
            self.config.validate()
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["config_loaded"] = False
            health_status["errors"].append(f"Config validation failed: {e}")
        
        try:
            # Check graph
            if self.graph is None:
                health_status["status"] = "unhealthy"
                health_status["graph_built"] = False
                health_status["errors"].append("Graph not built")
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["graph_built"] = False
            health_status["errors"].append(f"Graph check failed: {e}")
        
        self.logger.info(f"Health check completed: {health_status['status']}")
        return health_status
