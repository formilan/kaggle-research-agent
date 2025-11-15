#!/usr/bin/env python3
"""Test Gemini API REST with Service Account OAuth2 token"""

import os
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def test_rest_api_with_service_account():
    """Test Gemini API using REST with service account token"""

    credentials_path = "service-account.json"

    if not os.path.exists(credentials_path):
        print(f"❌ Service account file not found: {credentials_path}")
        return False

    print(f"✅ Service account file found")

    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform',
                    'https://www.googleapis.com/auth/generative-language.retriever']
        )

        print(f"✅ Credentials loaded")
        print(f"   Service account: {credentials.service_account_email}")

        # Get access token
        credentials.refresh(Request())
        access_token = credentials.token

        print(f"✅ Access token obtained: {access_token[:20]}...")

        # Test Gemini API with Bearer token
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "parts": [{"text": "Say hello in Italian"}]
            }]
        }

        print("\n🧪 Testing Gemini API with OAuth2 token...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)

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
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing Gemini REST API with Service Account...\n")
    success = test_rest_api_with_service_account()

    if success:
        print("\n✅ API test successful!")
    else:
        print("\n❌ API test failed.")
