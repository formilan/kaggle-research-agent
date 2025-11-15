#!/usr/bin/env python3
"""Test Google AI Studio API with REST endpoint"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_rest_api():
    """Test Gemini API using REST"""
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("❌ API key not found in .env file")
        return False

    print(f"✅ API key loaded: {api_key[:20]}...")

    # Test with Gemini API REST endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "parts": [{"text": "Say hello in Italian"}]
        }]
    }

    try:
        print("\n🧪 Testing Gemini API...")
        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Response: {text}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Google AI Studio REST API...\n")
    success = test_gemini_rest_api()

    if success:
        print("\n✅ API test successful!")
    else:
        print("\n❌ API test failed.")
