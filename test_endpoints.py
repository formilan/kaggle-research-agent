#!/usr/bin/env python3
"""Test different Gemini API endpoints"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_endpoints():
    api_key = os.getenv('GOOGLE_API_KEY')

    endpoints_to_test = [
        ("v1beta", "gemini-pro"),
        ("v1", "gemini-pro"),
        ("v1beta", "gemini-1.5-flash"),
        ("v1", "gemini-1.5-flash"),
    ]

    for version, model in endpoints_to_test:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{"text": "Hello"}]
            }]
        }

        try:
            print(f"\n🧪 Testing {version}/{model}...")
            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                print(f"   ✅ SUCCESS!")
                result = response.json()
                print(f"   Response: {result['candidates'][0]['content']['parts'][0]['text'][:50]}")
                return True
            else:
                print(f"   ❌ Error {response.status_code}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")

    return False

if __name__ == "__main__":
    print("🔍 Testing different Gemini API endpoints...")
    test_endpoints()
