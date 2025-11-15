#!/usr/bin/env python3
"""Test Google AI Studio setup"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

def test_api_connection():
    """Test connection to Google AI Studio"""
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("❌ API key not found in .env file")
        return False

    print(f"✅ API key loaded: {api_key[:20]}...")

    try:
        # Initialize client
        client = genai.Client(api_key=api_key)

        # List available models
        print("\n📋 Available models:")
        models = client.models.list()
        for model in models:
            if 'gemini' in model.name.lower():
                print(f"  - {model.name}")

        # Test a simple generation
        print("\n🧪 Testing simple generation...")
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents='Say hello in Italian'
        )
        print(f"✅ Response: {response.text}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Google AI Studio setup...\n")
    success = test_api_connection()

    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please check your API key.")
