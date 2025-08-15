#!/usr/bin/env python3
"""
Simple launcher for the LangGraph Chatbot Web UI
"""

import sys
import subprocess
import webbrowser
import time
import os

def main():
    print("🌐 LangGraph Chatbot Web UI Launcher")
    print("=" * 50)
    
    # Check if Flask is installed
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask>=2.3.0"])
        print("✅ Flask installed successfully")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please make sure you have configured your API keys.")
        print("   You can create a .env file with:")
        print("   OPENAI_API_KEY=your-openai-key")
        print("   TAVILY_API_KEY=your-tavily-key")
        print("   LANGSMITH_API_KEY=your-langsmith-key")
    
    print("\n🚀 Starting web server...")
    print("📱 Web interface will open automatically in your browser")
    print("🔧 Server will run on: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opening browser...")
    except:
        print("⚠️  Could not open browser automatically. Please visit: http://localhost:5000")
    
    # Start the web server
    try:
        from web_ui import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
