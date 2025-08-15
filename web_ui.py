#!/usr/bin/env python3
"""
Web UI for the LangGraph Chatbot
"""

from flask import Flask, render_template, request, jsonify, session
from chatbot_core import LangGraphChatbot
import json
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'langgraph_chatbot_secret_key'  # Required for Flask sessions

# Initialize the chatbot
chatbot = None

# Store active web sessions
web_sessions = {}

# Global session counter for unique IDs
session_counter = 0

def init_chatbot():
    """Initialize the chatbot instance"""
    global chatbot
    if chatbot is None:
        chatbot = LangGraphChatbot()
    return chatbot

def create_new_session():
    """Create a new session and return its ID"""
    global session_counter
    session_counter += 1
    session_id = f"web_session_{int(time.time())}_{session_counter}"
    
    # Initialize the session in the chatbot
    chatbot.start_session(session_id)
    web_sessions[session_id] = {
        'messages': [],
        'created_at': time.time(),
        'last_activity': time.time()
    }
    
    return session_id

def get_or_create_session():
    """Get existing session or create new one for the current user"""
    if 'session_id' not in session:
        # Create a new session
        session['session_id'] = create_new_session()
    else:
        # Update last activity for existing session
        session_id = session['session_id']
        if session_id in web_sessions:
            web_sessions[session_id]['last_activity'] = time.time()
        else:
            # Session was lost, create new one
            session['session_id'] = create_new_session()
    
    return session['session_id']

def get_session_id():
    """Get the current session ID without creating a new one"""
    return session.get('session_id')

def ensure_session_exists():
    """Ensure a session exists and return its ID"""
    return get_or_create_session()

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
        
        # Try to get session from request header first, then from Flask session
        session_id = request.headers.get('X-Session-ID')
        
        if not session_id or session_id not in web_sessions:
            # Create new session
            session_id = create_new_session()
        
        # Update session activity
        web_sessions[session_id]['last_activity'] = time.time()
        
        # Add user message to session history
        web_sessions[session_id]['messages'].append({
            'role': 'user',
            'content': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process the message
        start_time = time.time()
        
        # Collect the response
        response_parts = []
        final_response = None
        
        # Stream the response - use the same approach as interactive mode
        config = {"configurable": {"thread_id": session_id}}
        for event in chatbot.graph.stream(
            {"messages": [{"role": "user", "content": user_message}]},  # Only current message
            config=config
        ):
            for value in event.values():
                if "messages" in value and value["messages"]:
                    messages = value["messages"]
                    if messages and hasattr(messages[-1], 'content'):
                        response = messages[-1]
                        response_parts.append(response.content)
                        final_response = response.content
                    elif messages and isinstance(messages[-1], dict) and 'content' in messages[-1]:
                        response = messages[-1]
                        response_parts.append(response['content'])
                        final_response = response['content']
        
        # Use the final response if available, otherwise combine all parts
        if final_response:
            full_response = final_response
        else:
            full_response = '\n'.join(response_parts) if response_parts else "I'm sorry, I couldn't generate a response."
        
        # Add assistant response to session history
        web_sessions[session_id]['messages'].append({
            'role': 'assistant',
            'content': full_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Format the response the same way as the interactive mode
        formatted_response = f"🤖 Assistant: {full_response}"
        
        response_time = time.time() - start_time
        
        return jsonify({
            'response': formatted_response,
            'timestamp': datetime.now().isoformat(),
            'response_time': round(response_time, 2),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/api/chat_history', methods=['GET'])
def get_chat_history():
    """Get chat history for the current session"""
    try:
        # Try to get session from request header first
        session_id = request.headers.get('X-Session-ID')
        
        if not session_id or session_id not in web_sessions:
            return jsonify({'messages': [], 'session_id': 'no_session'})
        
        return jsonify({
            'messages': web_sessions[session_id]['messages'],
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': f'Error retrieving chat history: {str(e)}'}), 500

@app.route('/api/new_session', methods=['POST'])
def new_session():
    """Start a new conversation session"""
    try:
        # Clear current session
        if 'session_id' in session and session['session_id'] in web_sessions:
            del web_sessions[session['session_id']]
        
        # Create new session
        session_id = f"web_session_{int(time.time())}"
        session['session_id'] = session_id
        chatbot.start_session(session_id)
        web_sessions[session_id] = {
            'messages': [],
            'created_at': time.time()
        }
        
        return jsonify({
            'message': 'New session started',
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': f'Error starting new session: {str(e)}'}), 500

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
