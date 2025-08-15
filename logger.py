"""
Logging module for the LangGraph Chatbot
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class ChatbotLogger:
    """Centralized logging for the chatbot"""
    
    def __init__(self, 
                 name: str = "LangGraphChatbot",
                 level: int = logging.INFO,
                 log_file: Optional[str] = None,
                 console_output: bool = True):
        self.name = name
        self.level = level
        self.log_file = log_file
        self.console_output = console_output
        
        # Configure the logger
        self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logger configuration"""
        # Create logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if self.log_file:
            try:
                log_path = Path(self.log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(log_path)
                file_handler.setLevel(self.level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Could not set up file logging: {e}")
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_api_call(self, api_name: str, success: bool, duration: float = None, error: str = None):
        """Log API call information"""
        if success:
            duration_msg = f" (took {duration:.2f}s)" if duration else ""
            self.info(f"API call to {api_name} successful{duration_msg}")
        else:
            error_msg = f": {error}" if error else ""
            self.error(f"API call to {api_name} failed{error_msg}")
    
    def log_conversation_turn(self, turn_number: int, user_input: str, response_length: int):
        """Log conversation turn information"""
        self.info(f"Turn {turn_number}: User input length={len(user_input)}, Response length={response_length}")
    
    def log_graph_operation(self, operation: str, success: bool, details: str = None):
        """Log graph operation information"""
        if success:
            details_msg = f" - {details}" if details else ""
            self.info(f"Graph operation '{operation}' successful{details_msg}")
        else:
            details_msg = f" - {details}" if details else ""
            self.error(f"Graph operation '{operation}' failed{details_msg}")
    
    def set_level(self, level: int):
        """Change the logging level"""
        self.level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def get_logger(self):
        """Get the underlying logger instance"""
        return self.logger


# Global logger instance
logger = ChatbotLogger()


def get_logger(name: str = None) -> ChatbotLogger:
    """Get a logger instance"""
    if name:
        return ChatbotLogger(name=name)
    return logger
