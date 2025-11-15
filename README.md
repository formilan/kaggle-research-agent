# Research Assistant Agent

**Kaggle Agents Intensive Capstone Project**

An intelligent research assistant agent built with Google Vertex AI, demonstrating advanced agentic capabilities including memory management, tool orchestration, and comprehensive evaluation.

## 🎯 Features

This agent demonstrates the **3+ key concepts** required for the Kaggle Agents Intensive Capstone:

### 1. **Memory Management** 🧠
- **Conversation Memory**: Maintains full conversation history with context management
- **Research Memory**: Tracks findings, sources, and topics across sessions
- **Persistent Storage**: Save and load session data

### 2. **Tool Orchestration** 🛠️
- **Web Search**: Find relevant information across the web
- **Document Reader**: Extract key information from documents
- **Data Analysis**: Synthesize findings from multiple sources
- **Intelligent Planning**: LLM-powered research strategy planning

### 3. **Quality Evaluation** 📊
- **Response Quality Metrics**: Speed, completeness, tool usage efficiency
- **Real-time Scoring**: 0-100 evaluation of each response
- **Session Analytics**: Comprehensive statistics and reporting
- **Performance Tracking**: Monitor tool usage and execution times

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd kaggle-research-agent

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Basic Usage

```python
from src.agent import ResearchAssistantAgent

# Create agent (auto mode tries Vertex AI, falls back to mock)
agent = ResearchAssistantAgent(llm_mode="auto", verbose=True)

# Perform research
result = agent.research("What are the latest developments in quantum computing?")

print(result["response"])
print(f"Score: {result['evaluation']['overall_score']}/100")

# Get agent status
status = agent.get_status()
print(status)

# Save session
agent.save_session()
```

### Run Demo

```bash
# Basic demo (uses mock LLM)
python main.py

# Interactive mode
python main.py interactive

# Vertex AI mode (requires credentials)
python main.py vertex
```

## 📁 Project Structure

```
kaggle-research-agent/
├── src/
│   ├── agent.py          # Main ResearchAssistantAgent class
│   ├── memory.py         # Memory management (ConversationMemory, ResearchMemory)
│   ├── tools.py          # Research tools (WebSearch, DocumentReader, DataAnalysis)
│   ├── orchestrator.py   # Tool orchestration and task planning
│   ├── evaluator.py      # Quality evaluation and metrics
│   └── llm_client.py     # LLM client (Vertex AI + Mock)
├── tests/                # Unit tests
├── examples/             # Example notebooks
├── logs/                 # Session logs and evaluations
├── main.py               # Demo applications
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
GOOGLE_API_KEY=your_api_key_here
PROJECT_ID=your_gcp_project_id
LOCATION=us-central1
```

### Vertex AI Setup

1. Create a Google Cloud project
2. Enable Vertex AI API
3. Create service account with proper permissions
4. Download service account JSON credentials as `service-account.json`

## 📊 Evaluation Metrics

The agent evaluates each response across multiple dimensions:

- **Response Speed**: Time to generate response (target: < 2s)
- **Response Completeness**: Quality and depth of information
- **Tool Usage Efficiency**: Optimal tool selection and usage
- **Overall Score**: Composite score (0-100)

Example output:

```json
{
  "overall_score": 95.0,
  "metrics": {
    "response_speed": 100.0,
    "response_completeness": 85.0,
    "tool_usage_efficiency": 100.0
  },
  "response_time": 1.23,
  "tools_used": ["web_search", "document_reader", "data_analysis"]
}
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_agent.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 📚 Examples

### Simple Research Query

```python
agent = ResearchAssistantAgent()
result = agent.research("Explain machine learning")
print(result["response"])
```

### Multi-turn Conversation

```python
agent = ResearchAssistantAgent(verbose=False)

queries = [
    "What is quantum computing?",
    "How does it compare to classical computing?",
    "What are the main challenges?"
]

for query in queries:
    result = agent.research(query)
    print(f"Q: {query}")
    print(f"A: {result['response']}\n")

# Agent maintains context across queries
status = agent.get_status()
print(f"Total findings: {status['research_memory']['findings_count']}")
```

## 🎓 Kaggle Competition Requirements

This project fulfills all requirements for the **Agents Intensive Capstone Project**:

✅ **Built with Agent Development Kit principles**
✅ **Demonstrates 3+ concepts**: Memory, Tool Orchestration, Evaluation
✅ **Production-ready code** with proper error handling
✅ **Comprehensive documentation**
✅ **Working demo** (Kaggle Notebook included)
✅ **Technical write-up** explaining design decisions

## 📝 Technical Details

### Architecture

The agent follows a modular architecture:

1. **LLM Client Layer**: Abstracts LLM interactions (Vertex AI / Mock)
2. **Memory Layer**: Manages conversation and research context
3. **Tool Layer**: Implements research capabilities
4. **Orchestration Layer**: Coordinates tool usage
5. **Evaluation Layer**: Assesses response quality

### Design Decisions

- **Mock Mode**: Enables development/testing without API costs
- **Flexible LLM Backend**: Easy to switch between Vertex AI and other providers
- **Comprehensive Logging**: Track all interactions for debugging
- **Modular Tools**: Easy to add new research capabilities
- **Real-time Evaluation**: Immediate feedback on response quality

## 🤝 Contributing

This is a capstone project for the Kaggle Agents Intensive course. For issues or suggestions, please open an issue on GitHub.

## 📄 License

This project is created for educational purposes as part of the Kaggle Agents Intensive Capstone.

## 🙏 Acknowledgments

- **Google & Kaggle** for the Agents Intensive Course
- **Vertex AI team** for the excellent AI platform
- **Community** for feedback and support

---

**Author**: Kaggle Agents Intensive Participant
**Date**: November 2025
**Competition**: https://www.kaggle.com/competitions/agents-intensive-capstone-project
