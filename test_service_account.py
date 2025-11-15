#!/usr/bin/env python3
"""Test Google AI with Service Account credentials"""

import os
import google.generativeai as genai
from google.oauth2 import service_account

def test_with_service_account():
    """Test Gemini API using service account"""

    credentials_path = "service-account.json"

    if not os.path.exists(credentials_path):
        print(f"❌ Service account file not found: {credentials_path}")
        return False

    print(f"✅ Service account file found")

    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/generative-language']
        )

        print(f"✅ Credentials loaded")
        print(f"   Service account: {credentials.service_account_email}")

        # Configure genai with credentials
        genai.configure(credentials=credentials)

        # List available models
        print("\n📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")

        # Test generation
        print("\n🧪 Testing content generation...")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('Say hello in Italian')
        print(f"✅ Response: {response.text}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Testing Google AI with Service Account...\n")
    success = test_with_service_account()

    if success:
        print("\n✅ Service account authentication successful!")
    else:
        print("\n❌ Service account authentication failed.")
