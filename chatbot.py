"""
Main entry point for the LangGraph Chatbot
"""

import sys
import traceback
from chatbot_core import LangGraphChatbot
from logger import get_logger


def main():
    """Main function to run the chatbot"""
    logger = get_logger("Main")
    
    try:
        logger.info("Starting LangGraph Chatbot...")
        
        # Initialize the chatbot
        chatbot = LangGraphChatbot()
        
        # Perform health check
        health = chatbot.health_check()
        if health["status"] != "healthy":
            logger.error(f"Chatbot health check failed: {health['errors']}")
            print("❌ Chatbot initialization failed. Check the logs for details.")
            return 1
        
        logger.info("Chatbot health check passed")
        
        # Generate visualizations
        print("📊 Generating graph visualizations...")
        visualization_results = chatbot.generate_visualizations()
        
        if visualization_results:
            print(f"✅ Generated {len([r for r in visualization_results.values() if r])} visualizations")
        else:
            print("⚠️  No visualizations were generated")
        
        print()
        
        # Run interactive mode
        chatbot.run_interactive()
        
        logger.info("Chatbot session completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Chatbot interrupted by user")
        print("\n⏹️  Chatbot interrupted. Goodbye!")
        return 0
        
    except Exception as e:
        logger.error(f"Chatbot failed with error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        print(f"💥 Chatbot failed to start: {e}")
        print("📋 Check the logs for more details")
        print("🔄 Please check your configuration and try again")
        
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
