"""LLM Client with Vertex AI support and Mock mode"""

import os
from typing import Optional
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass


class MockLLMClient(LLMClient):
    """Mock LLM client for testing without API calls"""

    def __init__(self):
        self.call_count = 0

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate mock responses"""
        self.call_count += 1

        # Intelligent mock based on prompt content
        prompt_lower = prompt.lower()

        if "search" in prompt_lower or "find" in prompt_lower:
            return """Based on my search, here are the key findings:
1. The topic has several important aspects
2. Recent developments show significant progress
3. Expert consensus indicates this is a growing field

Would you like me to dive deeper into any specific area?"""

        elif "summarize" in prompt_lower or "summary" in prompt_lower:
            return """Summary of key points:
- Main concept: The subject matter is complex but well-documented
- Key findings: Multiple sources confirm the central thesis
- Implications: This has broad applications across various domains
- Conclusion: Further research is recommended"""

        elif "analyze" in prompt_lower or "analysis" in prompt_lower:
            return """Analysis:

Strengths:
- Well-supported by evidence
- Clear methodology
- Consistent results

Weaknesses:
- Limited scope in some areas
- Could benefit from additional data
- Some assumptions need validation

Overall assessment: The research is solid with room for expansion."""

        else:
            return f"""I understand you're asking about: {prompt[:100]}...

Let me provide a comprehensive response:
- This is a well-researched topic with significant documentation
- There are multiple perspectives to consider
- The evidence suggests a nuanced understanding is necessary

Would you like me to explore any specific aspect in more detail?"""


class VertexAIClient(LLMClient):
    """Vertex AI LLM client"""

    def __init__(self, project_id: str, location: str, model_name: str = "gemini-2.5-pro"):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.call_count = 0

        # Initialize Vertex AI
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel

            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account.json'
            vertexai.init(project=project_id, location=location)
            self.model = GenerativeModel(model_name)
            self.available = True
        except Exception as e:
            print(f"⚠️  Vertex AI initialization failed: {e}")
            print("📝 Falling back to mock mode")
            self.available = False
            self.mock_client = MockLLMClient()

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Vertex AI or fallback to mock"""
        self.call_count += 1

        if not self.available:
            return self.mock_client.generate(prompt, **kwargs)

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️  Vertex AI call failed: {e}")
            print("📝 Using mock response")
            if not hasattr(self, 'mock_client'):
                self.mock_client = MockLLMClient()
            return self.mock_client.generate(prompt, **kwargs)


def create_llm_client(mode: str = "auto") -> LLMClient:
    """Factory function to create LLM client

    Args:
        mode: "mock", "vertex", or "auto" (tries vertex, falls back to mock)
    """
    if mode == "mock":
        print("🤖 Using Mock LLM Client")
        return MockLLMClient()

    elif mode == "vertex" or mode == "auto":
        project_id = os.getenv('PROJECT_ID')
        location = os.getenv('LOCATION', 'us-central1')

        if not project_id:
            print("⚠️  PROJECT_ID not set, using mock mode")
            return MockLLMClient()

        print(f"🚀 Initializing Vertex AI (project: {project_id}, location: {location})")
        return VertexAIClient(project_id, location)

    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'mock', 'vertex', or 'auto'")
