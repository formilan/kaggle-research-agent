"""Tool orchestration and workflow management"""

from typing import List, Dict, Optional
import time
from tools import ToolRegistry
from llm_client import LLMClient


class TaskOrchestrator:
    """Orchestrates tool usage and task execution"""

    def __init__(self, llm_client: LLMClient, tool_registry: ToolRegistry):
        self.llm = llm_client
        self.tools = tool_registry
        self.execution_log: List[Dict] = []

    def plan_research(self, query: str) -> Dict:
        """Plan research strategy for a query"""
        start_time = time.time()

        # Use LLM to plan the research
        planning_prompt = f"""You are a research planning assistant. Given the following query,
create a research plan using available tools.

Query: {query}

Available tools:
{self._format_tools()}

Create a step-by-step research plan. Be concise."""

        plan_text = self.llm.generate(planning_prompt)

        plan = {
            "query": query,
            "plan": plan_text,
            "estimated_tools": self._extract_tool_names(plan_text),
            "planning_time": time.time() - start_time
        }

        self.execution_log.append({
            "action": "plan_research",
            "timestamp": time.time(),
            "result": plan
        })

        return plan

    def execute_research(self, query: str) -> Dict:
        """Execute a complete research task"""
        start_time = time.time()
        results = {
            "query": query,
            "steps": [],
            "tools_used": [],
            "findings": []
        }

        # Step 1: Web search
        search_tool = self.tools.get("web_search")
        if search_tool:
            search_results = search_tool.execute(query)
            results["steps"].append({
                "tool": "web_search",
                "result": search_results
            })
            results["tools_used"].append("web_search")

            # Extract findings from search
            for result in search_results.get("results", []):
                results["findings"].append({
                    "source": result.get("title"),
                    "content": result.get("snippet")
                })

        # Step 2: Document reading (if search found results)
        if results["findings"]:
            doc_tool = self.tools.get("document_reader")
            if doc_tool:
                # Read first document
                doc_url = results["steps"][0]["result"]["results"][0]["url"]
                doc_result = doc_tool.execute(doc_url)
                results["steps"].append({
                    "tool": "document_reader",
                    "result": doc_result
                })
                results["tools_used"].append("document_reader")

                # Add document findings
                content = doc_result.get("content", {})
                if "key_findings" in content:
                    for finding in content["key_findings"]:
                        results["findings"].append({
                            "source": "document",
                            "content": finding
                        })

        # Step 3: Synthesis
        analysis_tool = self.tools.get("data_analysis")
        if analysis_tool and results["findings"]:
            analysis = analysis_tool.execute(results["findings"])
            results["steps"].append({
                "tool": "data_analysis",
                "result": analysis
            })
            results["tools_used"].append("data_analysis")
            results["synthesis"] = analysis

        results["execution_time"] = time.time() - start_time
        results["success"] = len(results["tools_used"]) > 0

        self.execution_log.append({
            "action": "execute_research",
            "timestamp": time.time(),
            "result": results
        })

        return results

    def synthesize_findings(self, findings: List[Dict]) -> str:
        """Synthesize research findings into coherent response"""
        synthesis_prompt = f"""You are a research synthesizer. Create a comprehensive summary
of the following research findings:

Findings:
{self._format_findings(findings)}

Provide a clear, structured summary that integrates these findings."""

        synthesis = self.llm.generate(synthesis_prompt)
        return synthesis

    def _format_tools(self) -> str:
        """Format available tools for prompt"""
        tools = self.tools.list_tools()
        return "\n".join([f"- {t['name']}: {t['description']}" for t in tools])

    def _format_findings(self, findings: List[Dict]) -> str:
        """Format findings for prompt"""
        formatted = []
        for i, finding in enumerate(findings, 1):
            source = finding.get("source", "Unknown")
            content = finding.get("content", "")
            formatted.append(f"{i}. [{source}] {content}")
        return "\n".join(formatted)

    def _extract_tool_names(self, plan_text: str) -> List[str]:
        """Extract tool names mentioned in plan"""
        tool_names = []
        available_tools = self.tools.list_tools()

        for tool in available_tools:
            if tool["name"] in plan_text.lower():
                tool_names.append(tool["name"])

        return tool_names

    def get_execution_summary(self) -> Dict:
        """Get summary of all executions"""
        return {
            "total_executions": len(self.execution_log),
            "tool_stats": self.tools.get_all_stats()
        }
