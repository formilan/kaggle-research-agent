"""Main Research Assistant Agent"""

from typing import Dict, Optional
import time
from datetime import datetime

from llm_client import LLMClient, create_llm_client
from memory import ConversationMemory, ResearchMemory
from tools import create_default_tools, ToolRegistry
from orchestrator import TaskOrchestrator
from evaluator import AgentEvaluator


class ResearchAssistantAgent:
    """
    Research Assistant Agent for Kaggle Agents Intensive Capstone Project

    This agent demonstrates:
    1. Memory Management: Conversation history and research findings
    2. Tool Orchestration: Web search, document reading, data analysis
    3. Evaluation: Performance metrics and quality assessment
    """

    def __init__(self, llm_mode: str = "auto", verbose: bool = True):
        """
        Initialize the Research Assistant Agent

        Args:
            llm_mode: "mock", "vertex", or "auto" for LLM client
            verbose: Print detailed logs
        """
        self.verbose = verbose
        self.session_start = datetime.now()

        # Initialize components
        self._print("🚀 Initializing Research Assistant Agent...")

        self.llm = create_llm_client(llm_mode)
        self._print(f"   ✅ LLM Client initialized ({llm_mode} mode)")

        self.conv_memory = ConversationMemory(max_messages=50)
        self._print("   ✅ Conversation Memory initialized")

        self.research_memory = ResearchMemory()
        self._print("   ✅ Research Memory initialized")

        self.tools = create_default_tools()
        self._print(f"   ✅ Tools registered: {[t['name'] for t in self.tools.list_tools()]}")

        self.orchestrator = TaskOrchestrator(self.llm, self.tools)
        self._print("   ✅ Task Orchestrator initialized")

        self.evaluator = AgentEvaluator()
        self._print("   ✅ Evaluator initialized")

        self._print("\n✨ Research Assistant Agent ready!\n")

    def research(self, query: str) -> Dict:
        """
        Perform research on a query

        Args:
            query: The research question or topic

        Returns:
            Dictionary with research results and metadata
        """
        start_time = time.time()
        self._print(f"\n📚 Starting research: '{query}'\n")

        # Add to conversation memory
        self.conv_memory.add_message("user", query)

        # Step 1: Plan the research
        self._print("📋 Planning research strategy...")
        plan = self.orchestrator.plan_research(query)
        self._print(f"   Plan: {plan['plan'][:100]}...")

        # Step 2: Execute the research
        self._print("\n🔍 Executing research...")
        execution_results = self.orchestrator.execute_research(query)

        tools_used = execution_results.get("tools_used", [])
        self._print(f"   Tools used: {tools_used}")
        self._print(f"   Findings collected: {len(execution_results.get('findings', []))}")

        # Step 3: Synthesize findings
        self._print("\n🧠 Synthesizing findings...")
        if execution_results.get("findings"):
            synthesis = self.orchestrator.synthesize_findings(execution_results["findings"])

            # Store in research memory
            for finding in execution_results["findings"]:
                self.research_memory.add_finding(
                    finding=finding.get("content", ""),
                    source=finding.get("source"),
                    topic=query
                )
        else:
            synthesis = "No findings to synthesize."

        # Step 4: Generate final response
        self._print("\n💬 Generating final response...")
        response = self._generate_response(query, execution_results, synthesis)

        # Add to conversation memory
        self.conv_memory.add_message("assistant", response)

        # Step 5: Evaluate the response
        response_time = time.time() - start_time
        evaluation = self.evaluator.evaluate_response(
            query=query,
            response=response,
            response_time=response_time,
            tools_used=tools_used
        )

        self._print(f"\n📊 Evaluation Score: {evaluation['overall_score']}/100")
        self._print(f"⏱️  Response Time: {response_time:.2f}s\n")

        return {
            "query": query,
            "response": response,
            "plan": plan,
            "execution": execution_results,
            "synthesis": synthesis,
            "evaluation": evaluation,
            "response_time": response_time
        }

    def _generate_response(self, query: str, execution_results: Dict, synthesis: str) -> str:
        """Generate final response using LLM"""

        # Get recent context
        context = self.conv_memory.get_context_string(last_n=5)

        prompt = f"""You are a helpful research assistant. You've been asked to research the following:

Query: {query}

You've gathered the following information:

{synthesis}

Previous conversation context:
{context}

Provide a comprehensive, well-structured response to the query. Be informative and cite your findings."""

        response = self.llm.generate(prompt)
        return response

    def chat(self, message: str) -> str:
        """
        Simple chat interface

        Args:
            message: User message

        Returns:
            Agent response
        """
        result = self.research(message)
        return result["response"]

    def get_status(self) -> Dict:
        """Get agent status and statistics"""
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "conversation_stats": self.conv_memory.get_summary_stats(),
            "research_memory": {
                "findings_count": len(self.research_memory.findings),
                "topics": self.research_memory.topics,
                "sources": self.research_memory.sources
            },
            "tool_stats": self.tools.get_all_stats(),
            "evaluation_stats": self.evaluator.get_session_stats()
        }

    def save_session(self, directory: str = "logs") -> None:
        """Save session data"""
        import os
        os.makedirs(directory, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save conversation
        self.conv_memory.save(f"{directory}/conversation_{timestamp}.json")

        # Save evaluation report
        self.evaluator.save_report(f"{directory}/evaluation_{timestamp}.json")

        self._print(f"\n💾 Session saved to {directory}/")

    def _print(self, message: str) -> None:
        """Print if verbose mode is enabled"""
        if self.verbose:
            print(message)
