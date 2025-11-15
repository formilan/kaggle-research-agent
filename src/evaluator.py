"""Evaluation metrics and quality assessment for the agent"""

from typing import Dict, List, Optional
from datetime import datetime
import time
import json


class AgentEvaluator:
    """Evaluates agent performance and response quality"""

    def __init__(self):
        self.metrics: List[Dict] = []
        self.session_start = datetime.now()

    def evaluate_response(
        self,
        query: str,
        response: str,
        response_time: float,
        tools_used: List[str],
        context: Optional[Dict] = None
    ) -> Dict:
        """Evaluate a single response"""

        evaluation = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_length": len(response),
            "response_time": round(response_time, 3),
            "tools_used": tools_used,
            "tools_count": len(tools_used),
            "metrics": {}
        }

        # Calculate metrics
        evaluation["metrics"]["response_speed"] = self._evaluate_speed(response_time)
        evaluation["metrics"]["response_completeness"] = self._evaluate_completeness(response)
        evaluation["metrics"]["tool_usage_efficiency"] = self._evaluate_tool_usage(tools_used)

        # Overall score (0-100)
        scores = list(evaluation["metrics"].values())
        evaluation["overall_score"] = round(sum(scores) / len(scores), 2)

        self.metrics.append(evaluation)
        return evaluation

    def _evaluate_speed(self, response_time: float) -> float:
        """Evaluate response speed (0-100)"""
        # Excellent: < 2s, Good: 2-5s, Acceptable: 5-10s, Poor: > 10s
        if response_time < 2:
            return 100.0
        elif response_time < 5:
            return 80.0
        elif response_time < 10:
            return 60.0
        else:
            return 40.0

    def _evaluate_completeness(self, response: str) -> float:
        """Evaluate response completeness (0-100)"""
        # Based on response length and structure
        length = len(response)

        if length < 50:
            return 30.0
        elif length < 200:
            return 60.0
        elif length < 500:
            return 85.0
        else:
            return 95.0

    def _evaluate_tool_usage(self, tools_used: List[str]) -> float:
        """Evaluate tool usage efficiency (0-100)"""
        # Optimal: 2-3 tools, Acceptable: 1 or 4, Poor: 0 or 5+
        count = len(tools_used)

        if count == 0:
            return 40.0
        elif count == 1:
            return 70.0
        elif 2 <= count <= 3:
            return 100.0
        elif count == 4:
            return 75.0
        else:
            return 50.0

    def get_session_stats(self) -> Dict:
        """Get statistics for the current session"""
        if not self.metrics:
            return {"evaluations": 0}

        scores = [m["overall_score"] for m in self.metrics]
        response_times = [m["response_time"] for m in self.metrics]
        tools_counts = [m["tools_count"] for m in self.metrics]

        return {
            "session_duration": str(datetime.now() - self.session_start),
            "total_evaluations": len(self.metrics),
            "average_score": round(sum(scores) / len(scores), 2),
            "min_score": min(scores),
            "max_score": max(scores),
            "average_response_time": round(sum(response_times) / len(response_times), 3),
            "average_tools_used": round(sum(tools_counts) / len(tools_counts), 2),
            "last_evaluation": self.metrics[-1]["timestamp"]
        }

    def get_detailed_report(self) -> Dict:
        """Get detailed evaluation report"""
        stats = self.get_session_stats()

        if not self.metrics:
            return stats

        # Calculate metric breakdowns
        speed_scores = [m["metrics"]["response_speed"] for m in self.metrics]
        completeness_scores = [m["metrics"]["response_completeness"] for m in self.metrics]
        efficiency_scores = [m["metrics"]["tool_usage_efficiency"] for m in self.metrics]

        stats["metric_averages"] = {
            "response_speed": round(sum(speed_scores) / len(speed_scores), 2),
            "response_completeness": round(sum(completeness_scores) / len(completeness_scores), 2),
            "tool_usage_efficiency": round(sum(efficiency_scores) / len(efficiency_scores), 2)
        }

        # Tool usage breakdown
        all_tools = []
        for m in self.metrics:
            all_tools.extend(m["tools_used"])

        tool_usage = {}
        for tool in all_tools:
            tool_usage[tool] = tool_usage.get(tool, 0) + 1

        stats["tool_usage_breakdown"] = tool_usage

        return stats

    def save_report(self, filepath: str) -> None:
        """Save evaluation report to file"""
        report = {
            "session_info": self.get_session_stats(),
            "detailed_metrics": self.get_detailed_report(),
            "all_evaluations": self.metrics
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

    def reset(self) -> None:
        """Reset evaluator"""
        self.metrics = []
        self.session_start = datetime.now()
