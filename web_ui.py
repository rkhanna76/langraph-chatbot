#!/usr/bin/env python3
"""
Web UI for the LangGraph Chatbot
"""

from flask import Flask, render_template, request, jsonify
from chatbot_core import LangGraphChatbot
import json
import time
from datetime import datetime

app = Flask(__name__)

# Initialize the chatbot
chatbot = None

def init_chatbot():
    """Initialize the chatbot instance"""
    global chatbot
    if chatbot is None:
        chatbot = LangGraphChatbot()
    return chatbot

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize chatbot if needed
        init_chatbot()
        
        # Start a new session for web UI
        session_id = f"web_session_{int(time.time())}"
        chatbot.start_session(session_id)
        
        # Process the message
        start_time = time.time()
        
        # Collect the response
        response_parts = []
        
        # Stream the response
        config = {"configurable": {"thread_id": session_id}}
        for event in chatbot.graph.stream(
            {"messages": [{"role": "user", "content": user_message}]},
            config=config
        ):
            for value in event.values():
                if "messages" in value and value["messages"]:
                    messages = value["messages"]
                    if messages and hasattr(messages[-1], 'content'):
                        response = messages[-1]
                        response_parts.append(response.content)
                    elif messages and isinstance(messages[-1], dict) and 'content' in messages[-1]:
                        response = messages[-1]
                        response_parts.append(response['content'])
        
        # Combine all response parts
        full_response = '\n'.join(response_parts) if response_parts else "I'm sorry, I couldn't generate a response."
        
        response_time = time.time() - start_time
        
        return jsonify({
            'response': full_response,
            'timestamp': datetime.now().isoformat(),
            'response_time': round(response_time, 2)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        init_chatbot()
        health_status = chatbot.health_check()
        return jsonify({
            'status': 'healthy',
            'chatbot_health': health_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🌐 Starting LangGraph Chatbot Web UI...")
    print("📱 Web interface will be available at: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - GET  /api/health - Health check")
    print("   - POST /api/chat   - Send chat message")
    print("💡 Keep the command-line interface running in another terminal!")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
