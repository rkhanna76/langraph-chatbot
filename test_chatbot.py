"""
Test script for the modular LangGraph Chatbot
"""

import sys
import traceback
from chatbot_core import LangGraphChatbot
from config import ChatbotConfig
from logger import get_logger


def test_configuration():
    """Test configuration loading"""
    print("🧪 Testing configuration...")
    try:
        config = ChatbotConfig.from_env()
        config.validate()
        print("✅ Configuration test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_chatbot_initialization():
    """Test chatbot initialization"""
    print("🧪 Testing chatbot initialization...")
    try:
        chatbot = LangGraphChatbot()
        print("✅ Chatbot initialization test passed")
        return chatbot
    except Exception as e:
        print(f"❌ Chatbot initialization test failed: {e}")
        return None


def test_health_check(chatbot):
    """Test health check functionality"""
    print("🧪 Testing health check...")
    try:
        health = chatbot.health_check()
        print(f"✅ Health check passed: {health['status']}")
        return health['status'] == 'healthy'
    except Exception as e:
        print(f"❌ Health check test failed: {e}")
        return False


def test_visualization_generation(chatbot):
    """Test visualization generation"""
    print("🧪 Testing visualization generation...")
    try:
        results = chatbot.generate_visualizations()
        print(f"✅ Visualization generation test passed: {len(results)} formats")
        return True
    except Exception as e:
        print(f"❌ Visualization generation test failed: {e}")
        return False


def test_single_response(chatbot):
    """Test single response generation"""
    print("🧪 Testing single response generation...")
    try:
        # Test with a simple query
        test_input = "Hello, how are you?"
        print(f"📝 Test input: {test_input}")
        
        # This would normally stream, but for testing we'll just check it doesn't crash
        chatbot.stream_response(test_input)
        print("✅ Single response test passed")
        return True
    except Exception as e:
        print(f"❌ Single response test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🚀 Starting LangGraph Chatbot tests...")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Configuration
    if test_configuration():
        tests_passed += 1
    
    # Test 2: Chatbot initialization
    chatbot = test_chatbot_initialization()
    if chatbot:
        tests_passed += 1
        
        # Test 3: Health check
        if test_health_check(chatbot):
            tests_passed += 1
        
        # Test 4: Visualization generation
        if test_visualization_generation(chatbot):
            tests_passed += 1
        
        # Test 5: Single response
        if test_single_response(chatbot):
            tests_passed += 1
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The chatbot is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


def main():
    """Main test function"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 0
    except Exception as e:
        print(f"💥 Test suite failed with error: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
