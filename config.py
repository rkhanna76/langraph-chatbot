"""
Configuration management for the LangGraph Chatbot
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class ChatbotConfig:
    """Configuration class for the chatbot"""
    
    # API Keys
    openai_api_key: str
    tavily_api_key: str
    langsmith_api_key: str = None
    
    # Model Configuration
    model_name: str = "openai:gpt-4.1"
    max_search_results: int = 3
    
    # Visualization Settings
    save_visualizations: bool = True
    visualization_formats: list = None
    
    # Chat Settings
    max_conversation_turns: int = 50
    enable_web_search: bool = True
    
    # LangSmith Settings
    enable_langsmith: bool = True
    langsmith_project: str = "langgraph-chatbot"
    langsmith_tracing: bool = True
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    
    def __post_init__(self):
        if self.visualization_formats is None:
            self.visualization_formats = ["png", "mermaid"]
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "ChatbotConfig":
        """Create configuration from environment variables"""
        # Load .env file if it exists
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
        except ImportError:
            print("python-dotenv not installed. Install with: pip install python-dotenv")
        
        # Get required API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        langsmith_key = os.getenv("LANGSMITH_API_KEY")
        
        if not openai_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not tavily_key:
            print("Warning: TAVILY_API_KEY not found. Web search will be disabled.")
            tavily_key = "dummy-key"
        
        if not langsmith_key:
            print("Warning: LANGSMITH_API_KEY not found. LangSmith monitoring will be disabled.")
            langsmith_key = "dummy-key"
        
        return cls(
            openai_api_key=openai_key,
            tavily_api_key=tavily_key,
            langsmith_api_key=langsmith_key
        )
    
    def validate(self) -> bool:
        """Validate the configuration"""
        if not self.openai_api_key or self.openai_api_key == "your-openai-api-key-here":
            raise ValueError("Valid OpenAI API key is required")
        
        if self.enable_web_search and (not self.tavily_api_key or self.tavily_api_key == "your-tavily-api-key-here"):
            raise ValueError("Valid Tavily API key is required for web search")
        
        return True
