#!/usr/bin/env python3
"""Diagnostic tool per Google AI API"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def diagnose_api_key():
    api_key = os.getenv('GOOGLE_API_KEY')

    print("=" * 60)
    print("🔍 DIAGNOSTICA GOOGLE AI API")
    print("=" * 60)

    # Test 1: API key presente
    print(f"\n1. API Key presente: {'✅' if api_key else '❌'}")
    if api_key:
        print(f"   Key: {api_key[:20]}...{api_key[-4:]}")

    # Test 2: Prova diversi endpoint
    endpoints = [
        ("Gemini Pro (v1beta)", f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"),
        ("Gemini Pro (v1)", f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"),
        ("List Models (v1beta)", f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"),
    ]

    for name, url in endpoints:
        print(f"\n2. Test {name}:")
        try:
            if "generateContent" in url:
                response = requests.post(url, json={"contents": [{"parts": [{"text": "Hi"}]}]}, timeout=10)
            else:
                response = requests.get(url, timeout=10)

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                print(f"   ✅ FUNZIONA!")
                if "models" in url:
                    data = response.json()
                    print(f"   Modelli disponibili: {len(data.get('models', []))}")
                return True
            elif response.status_code == 403:
                print(f"   ❌ 403 Forbidden - API non abilitata o chiave senza permessi")
            elif response.status_code == 400:
                print(f"   ⚠️  400 Bad Request")
                print(f"   Response: {response.text[:200]}")
            else:
                print(f"   ❌ Error: {response.text[:200]}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")

    print("\n" + "=" * 60)
    print("📋 RACCOMANDAZIONI:")
    print("=" * 60)
    print("\n1. Verifica che l'API sia abilitata:")
    print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
    print("\n2. Controlla restrizioni API key:")
    print("   https://console.cloud.google.com/apis/credentials")
    print("\n3. Se hai fatturazione attiva, considera Vertex AI:")
    print("   https://console.cloud.google.com/vertex-ai")

    return False

if __name__ == "__main__":
    diagnose_api_key()
