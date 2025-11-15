"""Memory management for the Research Assistant Agent"""

from typing import List, Dict, Optional
from datetime import datetime
import json


class Message:
    """Represents a single message in conversation history"""

    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user', 'assistant', 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        )


class ConversationMemory:
    """Manages conversation history with context management"""

    def __init__(self, max_messages: int = 50):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.metadata: Dict = {}

    def add_message(self, role: str, content: str) -> None:
        """Add a message to history"""
        message = Message(role, content)
        self.messages.append(message)

        # Trim if exceeds max
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get conversation context as list of dicts"""
        messages = self.messages if last_n is None else self.messages[-last_n:]
        return [msg.to_dict() for msg in messages]

    def get_context_string(self, last_n: Optional[int] = None) -> str:
        """Get conversation context as formatted string"""
        messages = self.messages if last_n is None else self.messages[-last_n:]
        context_parts = []

        for msg in messages:
            context_parts.append(f"[{msg.role.upper()}]: {msg.content}")

        return "\n\n".join(context_parts)

    def clear(self) -> None:
        """Clear conversation history"""
        self.messages = []
        self.metadata = {}

    def save(self, filepath: str) -> None:
        """Save conversation to file"""
        data = {
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str) -> None:
        """Load conversation from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.messages = [Message.from_dict(msg) for msg in data["messages"]]
        self.metadata = data.get("metadata", {})

    def get_summary_stats(self) -> Dict:
        """Get summary statistics about the conversation"""
        if not self.messages:
            return {"message_count": 0}

        user_messages = [m for m in self.messages if m.role == "user"]
        assistant_messages = [m for m in self.messages if m.role == "assistant"]

        return {
            "message_count": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "first_message_time": self.messages[0].timestamp.isoformat(),
            "last_message_time": self.messages[-1].timestamp.isoformat(),
        }


class ResearchMemory:
    """Manages research-specific memory (findings, sources, etc.)"""

    def __init__(self):
        self.findings: List[Dict] = []
        self.sources: List[str] = []
        self.topics: List[str] = []

    def add_finding(self, finding: str, source: Optional[str] = None, topic: Optional[str] = None) -> None:
        """Add a research finding"""
        self.findings.append({
            "content": finding,
            "source": source,
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })

        if source and source not in self.sources:
            self.sources.append(source)

        if topic and topic not in self.topics:
            self.topics.append(topic)

    def get_findings_by_topic(self, topic: str) -> List[Dict]:
        """Get all findings for a specific topic"""
        return [f for f in self.findings if f.get("topic") == topic]

    def get_all_findings(self) -> List[Dict]:
        """Get all findings"""
        return self.findings

    def clear(self) -> None:
        """Clear research memory"""
        self.findings = []
        self.sources = []
        self.topics = []

    def to_dict(self) -> dict:
        """Export to dictionary"""
        return {
            "findings": self.findings,
            "sources": self.sources,
            "topics": self.topics
        }
