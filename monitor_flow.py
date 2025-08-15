"""
Script to demonstrate LangSmith flow monitoring
"""

from chatbot_core import LangGraphChatbot
from config import ChatbotConfig


def demonstrate_flow_monitoring():
    """Demonstrate LangSmith flow monitoring"""
    print("🔍 LangSmith Flow Monitoring Demo")
    print("=" * 50)
    
    try:
        # Initialize chatbot
        chatbot = LangGraphChatbot()
        
        # Check if LangSmith is enabled
        if not chatbot.get_monitor().is_enabled():
            print("❌ LangSmith is not enabled. Please set LANGSMITH_API_KEY in your .env file")
            print("💡 Get your API key from: https://smith.langchain.com/")
            return
        
        print("✅ LangSmith monitoring is enabled!")
        print(f"📊 Project URL: {chatbot.get_monitor().get_project_url()}")
        
        # Start a new session
        session_id = chatbot.start_session("demo_session")
        print(f"🆔 Session ID: {session_id}")
        
        # Test conversation with monitoring
        test_queries = [
            "Hello, how are you?",
            "What's the latest news about AI?",
            "Tell me a joke"
        ]
        
        print("\n🧪 Testing conversation flow with monitoring...")
        print("-" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Turn {i}: {query}")
            print("🔄 Processing...")
            
            # Process the query
            chatbot.stream_response(query)
            
            print(f"✅ Turn {i} completed and logged to LangSmith")
        
        print("\n🎉 Demo completed!")
        print(f"📊 View detailed traces at: {chatbot.get_monitor().get_project_url()}")
        print("\n💡 In LangSmith, you can see:")
        print("   - Node execution details (chatbot & tools)")
        print("   - Input/output for each step")
        print("   - Tool usage and results")
        print("   - Conversation flow visualization")
        print("   - Performance metrics and timing")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


def show_monitoring_features():
    """Show available monitoring features"""
    print("\n📋 LangSmith Monitoring Features:")
    print("=" * 40)
    print("🔍 Node Execution Tracking:")
    print("   - Input/output for each node")
    print("   - Execution time and performance")
    print("   - Error tracking and debugging")
    print()
    print("🛠️ Tool Usage Monitoring:")
    print("   - Which tools were called")
    print("   - Tool input and output")
    print("   - Tool execution success/failure")
    print()
    print("💬 Conversation Tracking:")
    print("   - Complete conversation history")
    print("   - Turn-by-turn analysis")
    print("   - Session management")
    print()
    print("📊 Visualization:")
    print("   - Flow diagrams")
    print("   - Performance graphs")
    print("   - Error analysis")
    print()
    print("🔗 Integration:")
    print("   - Real-time monitoring")
    print("   - API access for custom dashboards")
    print("   - Export capabilities")


if __name__ == "__main__":
    demonstrate_flow_monitoring()
    show_monitoring_features()
