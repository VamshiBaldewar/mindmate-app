#!/usr/bin/env python3
"""
Simple test script for GathaFeed API
"""

import requests
import json
import time

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Services: {data['services']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_register():
    """Test user registration"""
    print("\n🔍 Testing user registration...")
    try:
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
        response = requests.post(f"{API_BASE}/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Registration successful: {data['message']}")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n🔍 Testing user login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful: {data['message']}")
            return True
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    print("\n🔍 Testing chat endpoint...")
    try:
        chat_data = {
            "text": "I'm feeling stressed about my exams",
            "mood": "anxious"
        }
        response = requests.post(f"{API_BASE}/chat", json=chat_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat successful: {data['reply'][:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False

def test_feed():
    """Test feed endpoint"""
    print("\n🔍 Testing feed endpoint...")
    try:
        response = requests.get(f"{API_BASE}/feed")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Feed successful: {len(data['panels'])} panels")
            return True
        else:
            print(f"❌ Feed failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Feed error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting GathaFeed API Tests")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    tests = [
        test_health,
        test_register,
        test_login,
        test_chat,
        test_feed
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GathaFeed API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()
