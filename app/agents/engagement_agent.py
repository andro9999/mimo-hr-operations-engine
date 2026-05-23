"""Engagement Agent: pulse surveys, sentiment analysis, retention risk."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class EngagementAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "engagement"
        logger.info("EngagementAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "pulse_survey")

        if action == "pulse_survey":
            return self._design_pulse_survey(task.get("department", ""), task.get("theme", ""))
        if action == "sentiment":
            return self._analyze_sentiment(task.get("feedback_data", []))
        if action == "retention_risk":
            return self._assess_retention_risk(task.get("employee", {}), task.get("signals", []))
        return self._design_pulse_survey(task.get("department", ""), task.get("theme", ""))

    def _design_pulse_survey(self, department: str, theme: str) -> dict:
        department = department or "Company-wide"
        theme = theme or "General Engagement"

        question_sets = {
            "General Engagement": [
                {"question": "How satisfied are you with your current role?", "type": "rating", "scale": "1-5"},
                {"question": "Do you feel valued by your team?", "type": "rating", "scale": "1-5"},
                {"question": "How likely are you to recommend this company as a workplace?", "type": "rating", "scale": "0-10"},
                {"question": "What one thing would improve your work experience?", "type": "open_text"},
            ],
            "Work-Life Balance": [
                {"question": "How manageable is your current workload?", "type": "rating", "scale": "1-5"},
                {"question": "Do you feel you have enough time for personal life?", "type": "rating", "scale": "1-5"},
                {"question": "How often do you work beyond scheduled hours?", "type": "multiple_choice", "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]},
                {"question": "What would help improve your work-life balance?", "type": "open_text"},
            ],
            "Career Growth": [
                {"question": "Do you see a clear career path at this company?", "type": "rating", "scale": "1-5"},
                {"question": "How satisfied are you with learning opportunities?", "type": "rating", "scale": "1-5"},
                {"question": "Does your manager support your career development?", "type": "rating", "scale": "1-5"},
                {"question": "What skills would you like to develop?", "type": "open_text"},
            ],
        }
        questions = question_sets.get(theme, question_sets["General Engagement"])

        return {
            "action": "pulse_survey",
            "department": department,
            "theme": theme,
            "questions": questions,
            "survey_length": f"{len(questions)} questions, estimated 3 minutes",
            "distribution_method": "email + Slack",
            "anonymous": True,
            "response_window": "5 business days",
            "status": "created",
            "message": f"Pulse survey designed for {department} on '{theme}' theme.",
        }

    def _analyze_sentiment(self, feedback_data: list) -> dict:
        if not feedback_data:
            feedback_data = [
                "I really enjoy working here but feel overwhelmed with the current workload.",
                "Great team culture, but career growth opportunities are limited.",
                "Management is supportive and communication has improved.",
                "Compensation could be more competitive for the market.",
                "Love the flexible work arrangement and the learning budget.",
            ]

        positive_indicators = ["enjoy", "great", "love", "supportive", "improved", "flexible"]
        negative_indicators = ["overwhelmed", "limited", "could be", "concerned", "frustrated"]

        positive_count = 0
        negative_count = 0
        for fb in feedback_data:
            fb_lower = fb.lower()
            positive_count += sum(1 for w in positive_indicators if w in fb_lower)
            negative_count += sum(1 for w in negative_indicators if w in fb_lower)

        total = positive_count + negative_count or 1
        sentiment_score = round((positive_count - negative_count) / total, 2)

        if sentiment_score > 0.3:
            overall = "positive"
        elif sentiment_score < -0.3:
            overall = "negative"
        else:
            overall = "neutral"

        themes = [
            {"theme": "Workload", "sentiment": "mixed", "mentions": 2},
            {"theme": "Team Culture", "sentiment": "positive", "mentions": 3},
            {"theme": "Career Growth", "sentiment": "negative", "mentions": 2},
            {"theme": "Management", "sentiment": "positive", "mentions": 2},
            {"theme": "Compensation", "sentiment": "negative", "mentions": 1},
        ]

        return {
            "action": "sentiment_analysis",
            "feedback_count": len(feedback_data),
            "sentiment_score": sentiment_score,
            "overall_sentiment": overall,
            "positive_signals": positive_count,
            "negative_signals": negative_count,
            "key_themes": themes,
            "top_concern": "Career growth opportunities",
            "top_positive": "Team culture and management support",
            "recommendations": [
                "Address career development path clarity",
                "Review workload distribution",
                "Maintain strengths in team culture",
            ],
            "status": "completed",
            "message": f"Sentiment analysis completed on {len(feedback_data)} feedback items. Overall: {overall}.",
        }

    def _assess_retention_risk(self, employee: dict, signals: list) -> dict:
        name = employee.get("name", "Employee")
        tenure_years = employee.get("tenure_years", 2)

        if not signals:
            signals = [
                {"signal": "Reduced participation in team activities", "weight": 0.3},
                {"signal": "Updated LinkedIn profile recently", "weight": 0.5},
                {"signal": "Declined optional training", "weight": 0.2},
            ]

        risk_score = sum(s.get("weight", 0) for s in signals) / len(signals) if signals else 0
        risk_score = round(min(risk_score * 1.5, 1.0), 2)

        if risk_score > 0.6:
            risk_level = "high"
        elif risk_score > 0.35:
            risk_level = "medium"
        else:
            risk_level = "low"

        interventions = {
            "high": [
                "Schedule immediate 1:1 with skip-level manager",
                "Discuss career development plan",
                "Review compensation against market",
                "Consider retention bonus",
            ],
            "medium": [
                "Schedule career conversation with manager",
                "Explore stretch assignments",
                "Ensure workload is sustainable",
            ],
            "low": [
                "Continue regular check-ins",
                "Monitor for additional signals",
            ],
        }

        return {
            "action": "retention_risk",
            "employee": name,
            "tenure_years": tenure_years,
            "signals": signals,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "interventions": interventions[risk_level],
            "status": "assessed",
            "message": f"Retention risk for {name}: {risk_level} (score: {risk_score}).",
        }
