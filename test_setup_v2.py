#!/usr/bin/env python3
"""Test Google AI Studio setup with google-generativeai"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

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
        # Configure API
        genai.configure(api_key=api_key)

        # List available models
        print("\n📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")

        # Test a simple generation
        print("\n🧪 Testing simple generation...")
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
    print("🔍 Testing Google AI Studio setup...\n")
    success = test_api_connection()

    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please check your API key.")
