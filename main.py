#!/usr/bin/env python3
"""
Research Assistant Agent - Main Demo
Kaggle Agents Intensive Capstone Project
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent import ResearchAssistantAgent


def demo_basic():
    """Basic demo of the agent"""
    print("=" * 70)
    print("  RESEARCH ASSISTANT AGENT - BASIC DEMO")
    print("=" * 70)

    # Create agent in mock mode (no API calls needed)
    agent = ResearchAssistantAgent(llm_mode="mock", verbose=True)

    # Example research queries
    queries = [
        "What are the latest developments in quantum computing?",
        "Explain the principles of machine learning",
    ]

    for query in queries:
        result = agent.research(query)

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        print(f"\nRESPONSE:\n{result['response']}")
        print(f"\nEVALUATION SCORE: {result['evaluation']['overall_score']}/100")
        print(f"RESPONSE TIME: {result['response_time']:.2f}s")
        print(f"TOOLS USED: {result['execution']['tools_used']}")
        print("=" * 70)

    # Display agent status
    print("\n" + "=" * 70)
    print("  AGENT STATUS")
    print("=" * 70)
    status = agent.get_status()
    print(f"\nSession Duration: {status['session_duration']}")
    print(f"Total Conversations: {status['conversation_stats']['message_count']}")
    print(f"Research Findings: {status['research_memory']['findings_count']}")
    print(f"Total Evaluations: {status['evaluation_stats']['total_evaluations']}")
    print(f"Average Score: {status['evaluation_stats']['average_score']}/100")

    # Save session
    agent.save_session()


def demo_interactive():
    """Interactive demo"""
    print("=" * 70)
    print("  RESEARCH ASSISTANT AGENT - INTERACTIVE MODE")
    print("=" * 70)
    print("\nType 'quit' to exit, 'status' for agent status\n")

    agent = ResearchAssistantAgent(llm_mode="auto", verbose=False)

    while True:
        try:
            query = input("\n🔍 Your question: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break

            if query.lower() == 'status':
                status = agent.get_status()
                print(f"\n📊 Status:")
                print(f"   Conversations: {status['conversation_stats']['message_count']}")
                print(f"   Findings: {status['research_memory']['findings_count']}")
                print(f"   Avg Score: {status['evaluation_stats'].get('average_score', 'N/A')}")
                continue

            if not query:
                continue

            result = agent.research(query)
            print(f"\n💬 Response:\n{result['response']}")
            print(f"\n📊 Score: {result['evaluation']['overall_score']}/100 | "
                  f"Time: {result['response_time']:.2f}s")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

    agent.save_session()


def demo_vertex_ai():
    """Demo with Vertex AI (requires proper credentials)"""
    print("=" * 70)
    print("  RESEARCH ASSISTANT AGENT - VERTEX AI MODE")
    print("=" * 70)

    try:
        agent = ResearchAssistantAgent(llm_mode="vertex", verbose=True)

        query = "What is the future of artificial intelligence?"
        result = agent.research(query)

        print(f"\nRESPONSE:\n{result['response']}")
        print(f"\nSCORE: {result['evaluation']['overall_score']}/100")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Tip: Make sure Vertex AI is properly configured")


if __name__ == "__main__":
    load_dotenv()

    print("\n🤖 Research Assistant Agent")
    print("   Kaggle Agents Intensive Capstone Project\n")

    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "interactive":
            demo_interactive()
        elif mode == "vertex":
            demo_vertex_ai()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python main.py [interactive|vertex]")
    else:
        # Run basic demo by default
        demo_basic()
