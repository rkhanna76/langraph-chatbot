"""
Chat interface module for the LangGraph Chatbot
"""

import sys
from typing import Optional, Callable
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """Represents a chat message"""
    role: str
    content: str
    timestamp: Optional[str] = None


class ChatInterface:
    """Handles the chat interface and user interactions"""
    
    def __init__(self, 
                 stream_handler: Callable,
                 max_turns: int = 50,
                 welcome_message: str = None):
        self.stream_handler = stream_handler
        self.max_turns = max_turns
        self.welcome_message = welcome_message or self._get_default_welcome()
        self.turn_count = 0
    
    def run_interactive(self) -> None:
        """Run the chatbot in interactive mode"""
        self._display_welcome()
        
        while self.turn_count < self.max_turns:
            try:
                user_input = self._get_user_input()
                
                if self._should_exit(user_input):
                    self._display_goodbye()
                    break
                
                if not user_input.strip():
                    continue
                
                # Process the user input
                self._process_user_input(user_input)
                self.turn_count += 1
                
                # Add spacing between exchanges
                print()
                
            except KeyboardInterrupt:
                self._handle_interrupt()
                break
            except EOFError:
                self._handle_eof()
                break
            except Exception as e:
                self._handle_error(e)
                break
        
        if self.turn_count >= self.max_turns:
            print(f"\nReached maximum conversation turns ({self.max_turns}). Ending session.")
    
    def _display_welcome(self):
        """Display the welcome message"""
        print(self.welcome_message)
        print("-" * 50)
    
    def _get_default_welcome(self) -> str:
        """Get the default welcome message"""
        return (
            "🤖 LangGraph Chatbot started!\n"
            "💡 Type 'quit', 'exit', or 'q' to end the session\n"
            "🔍 Web search is enabled for real-time information\n"
            "📊 Graph visualizations are generated automatically"
        )
    
    def _get_user_input(self) -> str:
        """Get input from the user"""
        try:
            return input("👤 User: ").strip()
        except (EOFError, KeyboardInterrupt):
            raise
    
    def _should_exit(self, user_input: str) -> bool:
        """Check if the user wants to exit"""
        return user_input.lower() in ["quit", "exit", "q"]
    
    def _process_user_input(self, user_input: str):
        """Process the user input through the chatbot"""
        try:
            self.stream_handler(user_input)
        except Exception as e:
            print(f"❌ Error processing response: {e}")
            print("🔄 Please try again or restart the chatbot.")
    
    def _display_goodbye(self):
        """Display goodbye message"""
        print("👋 Goodbye! Thanks for chatting!")
    
    def _handle_interrupt(self):
        """Handle keyboard interrupt"""
        print("\n⏹️  Session interrupted. Goodbye!")
    
    def _handle_eof(self):
        """Handle end of file"""
        print("\n📄 End of input. Goodbye!")
    
    def _handle_error(self, error: Exception):
        """Handle unexpected errors"""
        print(f"\n💥 Unexpected error: {error}")
        print("🔄 Please restart the chatbot if the problem persists.")
    
    def get_turn_count(self) -> int:
        """Get the current turn count"""
        return self.turn_count
    
    def reset_turn_count(self):
        """Reset the turn count"""
        self.turn_count = 0


class NonInteractiveChatInterface(ChatInterface):
    """Non-interactive chat interface for testing or programmatic use"""
    
    def __init__(self, stream_handler: Callable, **kwargs):
        super().__init__(stream_handler, **kwargs)
        self.conversation_history = []
    
    def send_message(self, message: str) -> str:
        """Send a message and return the response"""
        if self.turn_count >= self.max_turns:
            return "Maximum conversation turns reached."
        
        try:
            # Store the message
            chat_msg = ChatMessage(role="user", content=message)
            self.conversation_history.append(chat_msg)
            
            # Process the message
            self._process_user_input(message)
            self.turn_count += 1
            
            # Return a placeholder response (in real implementation, you'd capture the actual response)
            return f"Message processed (turn {self.turn_count})"
            
        except Exception as e:
            return f"Error: {e}"
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history.clear()
        self.reset_turn_count()
