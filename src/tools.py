"""Research tools for the agent"""

from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import time


class Tool(ABC):
    """Abstract base class for tools"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.execution_count = 0
        self.total_execution_time = 0.0

    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict:
        """Execute the tool"""
        pass

    def _track_execution(self, start_time: float) -> None:
        """Track execution metrics"""
        self.execution_count += 1
        self.total_execution_time += time.time() - start_time

    def get_stats(self) -> Dict:
        """Get tool usage statistics"""
        avg_time = (self.total_execution_time / self.execution_count
                   if self.execution_count > 0 else 0)
        return {
            "name": self.name,
            "executions": self.execution_count,
            "total_time": round(self.total_execution_time, 3),
            "avg_time": round(avg_time, 3)
        }


class WebSearchTool(Tool):
    """Tool for web search (mock implementation)"""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information on a given query"
        )

    def execute(self, query: str, max_results: int = 5) -> Dict:
        """Execute web search"""
        start_time = time.time()

        # Mock search results
        results = {
            "query": query,
            "results": [
                {
                    "title": f"Research Article on {query}",
                    "url": f"https://example.com/article1",
                    "snippet": f"Comprehensive overview of {query} including latest developments and expert insights..."
                },
                {
                    "title": f"{query}: A Complete Guide",
                    "url": f"https://example.com/guide",
                    "snippet": f"Everything you need to know about {query}, from basics to advanced concepts..."
                },
                {
                    "title": f"Recent Advances in {query}",
                    "url": f"https://example.com/advances",
                    "snippet": f"Latest research and breakthroughs in {query} field, published by leading experts..."
                }
            ][:max_results],
            "count": min(max_results, 3)
        }

        self._track_execution(start_time)
        return results


class DocumentReaderTool(Tool):
    """Tool for reading and extracting information from documents"""

    def __init__(self):
        super().__init__(
            name="document_reader",
            description="Read and extract key information from documents"
        )

    def execute(self, document_url: str, extract_type: str = "summary") -> Dict:
        """Read and extract from document"""
        start_time = time.time()

        # Mock document reading
        result = {
            "url": document_url,
            "extract_type": extract_type,
            "content": {
                "title": "Sample Research Document",
                "authors": ["Dr. Smith", "Dr. Johnson"],
                "abstract": "This document presents comprehensive research on the topic...",
                "key_findings": [
                    "Finding 1: Significant correlation discovered",
                    "Finding 2: Novel methodology validated",
                    "Finding 3: Practical applications identified"
                ],
                "summary": "A comprehensive study revealing important insights and practical applications."
            }
        }

        self._track_execution(start_time)
        return result


class DataAnalysisTool(Tool):
    """Tool for analyzing and synthesizing information"""

    def __init__(self):
        super().__init__(
            name="data_analysis",
            description="Analyze and synthesize information from multiple sources"
        )

    def execute(self, data: List[Dict], analysis_type: str = "synthesis") -> Dict:
        """Analyze data"""
        start_time = time.time()

        # Mock analysis
        result = {
            "analysis_type": analysis_type,
            "data_points": len(data),
            "insights": [
                "Common theme identified across sources",
                "Contradictions found requiring further investigation",
                "Strong consensus on key points",
                "Gaps identified in current research"
            ],
            "summary": f"Analysis of {len(data)} data points reveals consistent patterns and some areas needing further research.",
            "confidence": 0.85
        }

        self._track_execution(start_time)
        return result


class ToolRegistry:
    """Registry for managing available tools"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool"""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]

    def get_all_stats(self) -> List[Dict]:
        """Get statistics for all tools"""
        return [tool.get_stats() for tool in self.tools.values()]


def create_default_tools() -> ToolRegistry:
    """Create and register default tools"""
    registry = ToolRegistry()
    registry.register(WebSearchTool())
    registry.register(DocumentReaderTool())
    registry.register(DataAnalysisTool())
    return registry
