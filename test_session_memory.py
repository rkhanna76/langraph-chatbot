#!/usr/bin/env python3
"""
Test script to verify session memory functionality in the web UI
"""

import requests
import json
import time

def test_session_memory():
    """Test if the web UI maintains conversation memory across requests"""
    
    base_url = "http://localhost:5000"
    
    # Test 1: Send first message
    print("🧪 Test 1: Sending first message...")
    response1 = requests.post(f"{base_url}/api/chat", 
                             json={"message": "Hello, my name is TestUser"})
    
    if response1.status_code == 200:
        data1 = response1.json()
        session_id1 = data1['session_id']
        print(f"✅ First message sent successfully")
        print(f"   Session ID: {session_id1}")
        print(f"   Response: {data1['response']}")
    else:
        print(f"❌ First message failed: {response1.status_code}")
        return
    
    print()
    
    # Test 2: Send follow-up message using the same session ID
    print("🧪 Test 2: Sending follow-up message with session header...")
    headers = {'X-Session-ID': session_id1}
    response2 = requests.post(f"{base_url}/api/chat", 
                             json={"message": "What is my name?"},
                             headers=headers)
    
    if response2.status_code == 200:
        data2 = response2.json()
        session_id2 = data2['session_id']
        print(f"✅ Follow-up message sent successfully")
        print(f"   Session ID: {session_id2}")
        print(f"   Response: {data2['response']}")
    else:
        print(f"❌ Follow-up message failed: {response2.status_code}")
        return
    
    print()
    
    # Test 3: Check if session IDs are the same
    print("🧪 Test 3: Checking session consistency...")
    if session_id1 == session_id2:
        print(f"✅ Session IDs match: {session_id1}")
        print("   This means the same session is being used")
    else:
        print(f"❌ Session IDs don't match!")
        print(f"   First: {session_id1}")
        print(f"   Second: {session_id2}")
        print("   This means new sessions are being created")
    
    print()
    
    # Test 4: Check chat history for the specific session
    print("🧪 Test 4: Checking chat history for session...")
    headers = {'X-Session-ID': session_id1}
    history_response = requests.get(f"{base_url}/api/chat_history", headers=headers)
    
    if history_response.status_code == 200:
        history_data = history_response.json()
        print(f"✅ Chat history retrieved successfully")
        print(f"   Session ID: {history_data['session_id']}")
        print(f"   Message count: {len(history_data['messages'])}")
        
        if history_data['messages']:
            print("   Messages:")
            for i, msg in enumerate(history_data['messages']):
                role = msg['role']
                content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                print(f"     {i+1}. [{role}] {content}")
        else:
            print("   No messages found in this session")
    else:
        print(f"❌ Chat history failed: {history_response.status_code}")
    
    print()
    
    # Test 5: Test new session functionality
    print("🧪 Test 5: Testing new session...")
    new_session_response = requests.post(f"{base_url}/api/new_session")
    
    if new_session_response.status_code == 200:
        new_session_data = new_session_response.json()
        print(f"✅ New session created successfully")
        print(f"   New Session ID: {new_session_data['session_id']}")
    else:
        print(f"❌ New session failed: {new_session_response.status_code}")
    
    print()
    print("🎯 Test completed!")

if __name__ == "__main__":
    print("🚀 Testing Web UI Session Memory Functionality")
    print("=" * 50)
    print()
    
    try:
        test_session_memory()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the web UI")
        print("   Make sure the web UI is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
