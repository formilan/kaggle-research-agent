#!/usr/bin/env python3
"""Test Vertex AI con service account"""

import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv()

def test_vertex_ai():
    """Test Vertex AI Gemini"""

    project_id = os.getenv('PROJECT_ID')
    location = os.getenv('LOCATION')

    print("=" * 60)
    print("🔍 TEST VERTEX AI")
    print("=" * 60)
    print(f"\nProject ID: {project_id}")
    print(f"Location: {location}")

    try:
        # Inizializza Vertex AI
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account.json'

        vertexai.init(project=project_id, location=location)
        print("✅ Vertex AI inizializzato")

        # Crea model
        model = GenerativeModel("gemini-2.5-pro")
        print("✅ Modello Gemini 2.5 Pro caricato")

        # Test generation
        print("\n🧪 Test generazione contenuto...")
        response = model.generate_content("Say hello in Italian")

        print(f"✅ SUCCESSO!")
        print(f"\nRisposta: {response.text}")

        return True

    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_vertex_ai()

    if success:
        print("\n" + "=" * 60)
        print("✅ VERTEX AI FUNZIONA PERFETTAMENTE!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Test fallito")
        print("=" * 60)
