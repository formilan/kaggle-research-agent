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
        """Execute web search with smart mock responses"""
        start_time = time.time()

        query_lower = query.lower()

        # Smart responses for specific topics
        if any(word in query_lower for word in ["nvidia", "nvda"]) and any(word in query_lower for word in ["azioni", "stock", "prezzo", "price", "andamento"]):
            results = {
                "query": query,
                "results": [
                    {
                        "title": "NVIDIA Stock (NVDA) Real-Time Quote - Nov 2025",
                        "url": "https://finance.yahoo.com/quote/NVDA",
                        "snippet": "NVIDIA Corporation (NVDA) current price: $495.20. Last 30 days: +12.5% (+$55.10). High: $505.30, Low: $440.10. Strong performance driven by AI chip demand and data center growth. Volume: 45.2M shares."
                    },
                    {
                        "title": "NVIDIA Stock Analysis - AI Boom Continues",
                        "url": "https://www.bloomberg.com/nvidia-analysis",
                        "snippet": "NVIDIA shares surge 12.5% in past month reaching $495.20. Analysts cite robust Q4 earnings, new H200 GPU launch, and partnerships with Microsoft, Google for cloud AI. Price target raised to $550."
                    },
                    {
                        "title": "Why NVIDIA Stock is Up This Month - Market Watch",
                        "url": "https://marketwatch.com/nvidia-november",
                        "snippet": "Key factors driving NVIDIA's 12.5% gain: (1) Q4 revenue beat at $18.1B, (2) Data center revenue up 41%, (3) New AI partnerships announced, (4) Strong guidance for 2025. Stock outperforming S&P 500."
                    }
                ][:max_results],
                "count": min(max_results, 3)
            }

        elif any(word in query_lower for word in ["tesla", "tsla"]) and any(word in query_lower for word in ["stock", "azioni", "prezzo"]):
            results = {
                "query": query,
                "results": [
                    {
                        "title": "Tesla Inc (TSLA) Stock Price - Real-Time",
                        "url": "https://finance.yahoo.com/quote/TSLA",
                        "snippet": "Tesla (TSLA) current: $242.80. Last 30 days: +8.3% (+$18.60). Range: $224.20-$251.50. Model 3 sales strong in Europe. Cybertruck production ramping up. Volume: 98.5M."
                    }
                ][:max_results],
                "count": min(max_results, 1)
            }

        elif "machine learning" in query_lower or "ml" in query_lower:
            results = {
                "query": query,
                "results": [
                    {
                        "title": "Machine Learning: Complete Guide 2025",
                        "url": "https://towardsdatascience.com/ml-guide",
                        "snippet": "Machine Learning is a subset of AI enabling systems to learn from data. Key types: Supervised (classification, regression), Unsupervised (clustering), Reinforcement learning. Popular frameworks: TensorFlow, PyTorch, scikit-learn."
                    },
                    {
                        "title": "Latest Advances in ML - November 2025",
                        "url": "https://arxiv.org/ml-advances",
                        "snippet": "Recent breakthroughs: GPT-5 with 10T parameters, diffusion models for video generation, quantum ML algorithms. Growing applications in healthcare, finance, autonomous vehicles."
                    }
                ][:max_results],
                "count": min(max_results, 2)
            }

        elif "quantum" in query_lower:
            results = {
                "query": query,
                "results": [
                    {
                        "title": "Quantum Computing Explained - 2025 Update",
                        "url": "https://quantumcomputing.com/guide",
                        "snippet": "Quantum computers use qubits for parallel processing via superposition and entanglement. IBM's 1121-qubit processor, Google's error correction breakthrough. Applications: cryptography, drug discovery, optimization."
                    },
                    {
                        "title": "Latest Quantum Computing Developments",
                        "url": "https://nature.com/quantum-news",
                        "snippet": "IBM achieves quantum advantage in chemistry simulations. Microsoft Azure Quantum available commercially. China's photonic quantum computer processes 10^14 samples/sec. Quantum internet prototype tested."
                    }
                ][:max_results],
                "count": min(max_results, 2)
            }

        else:
            # Generic fallback for other queries
            results = {
                "query": query,
                "results": [
                    {
                        "title": f"Comprehensive Guide: {query}",
                        "url": f"https://example.com/guide",
                        "snippet": f"Detailed information about {query}: Current state, recent developments, expert analysis, and practical applications. Updated November 2025."
                    },
                    {
                        "title": f"{query} - Latest Research 2025",
                        "url": f"https://example.com/research",
                        "snippet": f"Recent advances in {query}: Key findings from leading institutions, emerging trends, and future outlook. Published by industry experts."
                    },
                    {
                        "title": f"{query}: Practical Applications",
                        "url": f"https://example.com/applications",
                        "snippet": f"Real-world applications of {query}: Case studies, success stories, implementation guides, and best practices from top companies."
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
        """Read and extract from document with smart responses"""
        start_time = time.time()

        url_lower = document_url.lower()

        # Smart responses based on URL content
        if "nvidia" in url_lower or "nvda" in url_lower:
            result = {
                "url": document_url,
                "extract_type": extract_type,
                "content": {
                    "title": "NVIDIA Q4 2025 Financial Results and Market Analysis",
                    "authors": ["Goldman Sachs Research", "Morgan Stanley Analysis Team"],
                    "date": "November 10, 2025",
                    "abstract": "NVIDIA reports exceptional Q4 performance with revenue reaching $18.1 billion, driven by unprecedented demand for AI accelerators and data center solutions.",
                    "key_findings": [
                        "Stock price: $495.20 (+12.5% monthly gain, +55.10 points)",
                        "Q4 Revenue: $18.1B, beating estimates by 8.5%",
                        "Data Center segment up 41% YoY, driven by H200 GPU adoption",
                        "New partnerships with Microsoft Azure, Google Cloud, Amazon AWS",
                        "2025 guidance raised: expected revenue growth 30-35%",
                        "Price target consensus: $550 (upside 11% from current)"
                    ],
                    "summary": "NVIDIA demonstrates exceptional momentum in AI chip market with strong financials, strategic partnerships, and robust guidance. Stock outperforming tech sector with sustained institutional buying."
                }
            }

        elif "tesla" in url_lower or "tsla" in url_lower:
            result = {
                "url": document_url,
                "extract_type": extract_type,
                "content": {
                    "title": "Tesla Stock Performance Analysis - November 2025",
                    "authors": ["UBS Investment Research"],
                    "date": "November 12, 2025",
                    "abstract": "Tesla stock analysis showing 8.3% monthly gain driven by production ramp and European sales.",
                    "key_findings": [
                        "Current price: $242.80 (+8.3% monthly, +18.60 points)",
                        "Cybertruck production ramping: 5,000 units/week achieved",
                        "Model 3/Y sales up 22% in Europe amid EV incentives",
                        "Energy storage deployments at record 3.5 GWh in Q3"
                    ],
                    "summary": "Tesla showing solid operational execution with production milestones and geographic expansion."
                }
            }

        elif "machine learning" in url_lower or "ml" in url_lower:
            result = {
                "url": document_url,
                "extract_type": extract_type,
                "content": {
                    "title": "Machine Learning: State of the Art 2025",
                    "authors": ["Dr. Andrew Ng", "Prof. Yann LeCun", "Dr. Fei-Fei Li"],
                    "date": "November 2025",
                    "abstract": "Comprehensive review of machine learning advances including transformer models, multimodal learning, and real-world applications.",
                    "key_findings": [
                        "Transformer architecture dominates: GPT, BERT, Vision Transformers",
                        "Multimodal models (text+image+audio) showing breakthrough results",
                        "Few-shot learning enabling rapid adaptation with minimal data",
                        "ML deployment in production: healthcare diagnostics, autonomous vehicles, financial trading",
                        "Emerging: neuromorphic computing, quantum ML algorithms"
                    ],
                    "summary": "ML field experiencing rapid innovation with practical applications transforming industries. Focus shifting from model size to efficiency and real-world deployment."
                }
            }

        elif "quantum" in url_lower:
            result = {
                "url": document_url,
                "extract_type": extract_type,
                "content": {
                    "title": "Quantum Computing Breakthroughs 2025",
                    "authors": ["IBM Quantum Research", "Google Quantum AI"],
                    "date": "November 2025",
                    "abstract": "Recent quantum computing advances including error correction, qubit scaling, and commercial applications.",
                    "key_findings": [
                        "IBM achieves 1121-qubit processor with improved coherence times",
                        "Google demonstrates quantum error correction at scale",
                        "Quantum advantage proven for chemistry simulations and cryptography",
                        "Commercial quantum cloud services: IBM Quantum, Azure Quantum, Amazon Braket",
                        "Applications: drug discovery, materials science, financial optimization"
                    ],
                    "summary": "Quantum computing transitioning from research to practical applications with improved hardware and accessible cloud platforms."
                }
            }

        else:
            # Generic fallback
            result = {
                "url": document_url,
                "extract_type": extract_type,
                "content": {
                    "title": "Research Document Analysis",
                    "authors": ["Research Team"],
                    "date": "November 2025",
                    "abstract": "Comprehensive analysis of current topic with latest research and industry insights.",
                    "key_findings": [
                        "Current state: Rapidly evolving field with significant research activity",
                        "Key trends: Innovation accelerating, practical applications emerging",
                        "Industry impact: Major companies investing heavily in development",
                        "Future outlook: Continued growth expected with broader adoption"
                    ],
                    "summary": "Field showing strong momentum with research breakthroughs translating to practical applications."
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
