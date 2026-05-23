"""Performance Agent: goal tracking, 360 feedback, review drafting."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PerformanceAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "performance"
        logger.info("PerformanceAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "goal_tracking")

        if action == "goal_tracking":
            return self._track_goals(task.get("employee", {}), task.get("goals", []))
        if action == "feedback_360":
            return self._collect_360_feedback(task.get("employee", {}), task.get("reviewers", []))
        if action == "draft_review":
            return self._draft_review(task.get("employee", {}), task.get("period", ""))
        return self._track_goals(task.get("employee", {}), task.get("goals", []))

    def _track_goals(self, employee: dict, goals: list) -> dict:
        name = employee.get("name", "Employee")
        if not goals:
            goals = [
                {"goal": "Increase customer satisfaction score by 10%", "progress": 65, "status": "on_track"},
                {"goal": "Complete leadership training program", "progress": 80, "status": "on_track"},
                {"goal": "Reduce project delivery time by 15%", "progress": 30, "status": "at_risk"},
                {"goal": "Mentor 2 junior team members", "progress": 50, "status": "on_track"},
            ]

        total_progress = sum(g.get("progress", 0) for g in goals) / len(goals) if goals else 0
        at_risk = [g for g in goals if g.get("status") == "at_risk"]

        return {
            "action": "goal_tracking",
            "employee": name,
            "goals": goals,
            "overall_progress": round(total_progress, 1),
            "goals_on_track": sum(1 for g in goals if g.get("status") == "on_track"),
            "goals_at_risk": len(at_risk),
            "at_risk_details": at_risk,
            "recommendation": "Focus on at-risk goals. Consider reallocating resources." if at_risk else "All goals progressing well.",
            "status": "completed",
            "message": f"Goal tracking report generated for {name}. Overall progress: {total_progress:.0f}%.",
        }

    def _collect_360_feedback(self, employee: dict, reviewers: list) -> dict:
        name = employee.get("name", "Employee")
        if not reviewers:
            reviewers = [
                {"name": "Manager", "relationship": "direct_manager", "submitted": True},
                {"name": "Peer A", "relationship": "peer", "submitted": True},
                {"name": "Peer B", "relationship": "peer", "submitted": False},
                {"name": "Direct Report", "relationship": "direct_report", "submitted": True},
            ]

        submitted = [r for r in reviewers if r.get("submitted")]
        pending = [r for r in reviewers if not r.get("submitted")]

        strengths = ["Strong communication", "Technical expertise", "Reliable delivery"]
        areas_for_growth = ["Delegation", "Strategic thinking", "Cross-team collaboration"]

        return {
            "action": "feedback_360",
            "employee": name,
            "reviewers_total": len(reviewers),
            "feedback_received": len(submitted),
            "feedback_pending": len(pending),
            "pending_from": [r["name"] for r in pending],
            "consolidated_strengths": strengths,
            "consolidated_areas_for_growth": areas_for_growth,
            "overall_rating": "Meets Expectations",
            "status": "partial" if pending else "completed",
            "message": f"360 feedback collected for {name}: {len(submitted)}/{len(reviewers)} responses received.",
        }

    def _draft_review(self, employee: dict, period: str) -> dict:
        name = employee.get("name", "Employee")
        period = period or "Q4 2025"

        return {
            "action": "draft_review",
            "employee": name,
            "period": period,
            "review_draft": {
                "summary": f"{name} has demonstrated strong performance during {period} with consistent delivery on core responsibilities.",
                "achievements": [
                    "Led successful product launch with zero critical defects",
                    "Mentored 2 new hires who are now fully productive",
                    "Improved team velocity by 20% through process improvements",
                ],
                "areas_for_improvement": [
                    "Increase visibility in cross-functional initiatives",
                    "Develop more strategic planning skills",
                ],
                "rating": "Exceeds Expectations",
                "recommended_actions": [
                    "Consider for promotion track in next cycle",
                    "Assign stretch project for strategic development",
                ],
            },
            "status": "draft",
            "message": f"Performance review draft generated for {name} ({period}). Requires manager approval.",
        }
