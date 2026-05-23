"""Offboarding Agent: exit interviews, knowledge transfer, access revocation."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OffboardingAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "offboarding"
        logger.info("OffboardingAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "exit_interview")

        if action == "exit_interview":
            return self._conduct_exit_interview(task.get("employee", {}), task.get("responses", {}))
        if action == "knowledge_transfer":
            return self._plan_knowledge_transfer(task.get("employee", {}), task.get("knowledge_areas", []))
        if action == "access_revocation":
            return self._revoke_access(task.get("employee", {}), task.get("last_day", ""))
        if action == "full_offboarding":
            return self._full_offboarding(task.get("employee", {}), task.get("last_day", ""))
        return self._conduct_exit_interview(task.get("employee", {}), task.get("responses", {}))

    def _conduct_exit_interview(self, employee: dict, responses: dict) -> dict:
        name = employee.get("name", "Employee")
        department = employee.get("department", "General")
        tenure_years = employee.get("tenure_years", 1)

        if not responses:
            responses = {
                "reason_for_leaving": "Career growth opportunity",
                "satisfaction_with_role": 3,
                "satisfaction_with_management": 4,
                "satisfaction_with_compensation": 3,
                "would_recommend_company": True,
                "improvement_suggestions": "More transparent promotion process and better cross-team communication.",
            }

        risk_areas = []
        if responses.get("satisfaction_with_management", 5) <= 2:
            risk_areas.append("Management satisfaction")
        if responses.get("satisfaction_with_compensation", 5) <= 2:
            risk_areas.append("Compensation competitiveness")
        if not responses.get("would_recommend_company", True):
            risk_areas.append("Overall employer brand risk")

        return {
            "action": "exit_interview",
            "employee": name,
            "department": department,
            "tenure_years": tenure_years,
            "responses": responses,
            "risk_areas": risk_areas,
            "themes_extracted": [
                "Desire for career advancement",
                "Need for clearer promotion criteria",
                "Cross-team collaboration gaps",
            ],
            "recommended_actions": [
                "Review promotion process transparency",
                "Implement cross-team communication initiatives",
                f"Conduct stay interviews with {department} team to identify similar concerns",
            ],
            "status": "completed",
            "message": f"Exit interview analysis for {name} ({tenure_years}yr tenure). {len(risk_areas)} risk areas flagged.",
        }

    def _plan_knowledge_transfer(self, employee: dict, knowledge_areas: list) -> dict:
        name = employee.get("name", "Employee")
        department = employee.get("department", "General")

        if not knowledge_areas:
            knowledge_areas = [
                {
                    "area": "Client relationship management",
                    "description": "Key client contacts and relationship history",
                    "priority": "critical",
                    "recipients": ["Team Lead", "Account Manager"],
                    "format": "Document + 1:1 session",
                    "estimated_hours": 4,
                },
                {
                    "area": "Internal tool configurations",
                    "description": "Custom scripts, dashboards, and automations",
                    "priority": "high",
                    "recipients": ["Senior Engineer"],
                    "format": "Documentation + code walkthrough",
                    "estimated_hours": 6,
                },
                {
                    "area": "Ongoing project status",
                    "description": "Current project states, blockers, and next steps",
                    "priority": "critical",
                    "recipients": ["Project Manager", "Team"],
                    "format": "Status document + team handoff meeting",
                    "estimated_hours": 3,
                },
                {
                    "area": "Vendor relationships",
                    "description": "Vendor contacts, contract details, and negotiation history",
                    "priority": "medium",
                    "recipients": ["Procurement Lead"],
                    "format": "Written handoff document",
                    "estimated_hours": 2,
                },
            ]

        total_hours = sum(a.get("estimated_hours", 0) for a in knowledge_areas)
        critical_items = [a for a in knowledge_areas if a.get("priority") == "critical"]

        return {
            "action": "knowledge_transfer",
            "employee": name,
            "department": department,
            "knowledge_areas": knowledge_areas,
            "total_transfer_hours": total_hours,
            "critical_items": len(critical_items),
            "transfer_deadline": "Before last day",
            "status": "planned",
            "message": f"Knowledge transfer plan for {name}: {len(knowledge_areas)} areas, {total_hours}h total, {len(critical_items)} critical.",
        }

    def _revoke_access(self, employee: dict, last_day: str) -> dict:
        name = employee.get("name", "Employee")
        department = employee.get("department", "General")
        last_day = last_day or "TBD"

        access_items = [
            {"system": "Email (Google Workspace)", "action": "Disable account", "timing": "EOD last day", "status": "pending"},
            {"system": "Slack", "action": "Deactivate account", "action_secondary": "Archive DMs", "timing": "EOD last day", "status": "pending"},
            {"system": "VPN", "action": "Revoke certificates", "timing": "EOD last day", "status": "pending"},
            {"system": "GitHub", "action": "Remove from organization", "timing": "EOD last day", "status": "pending"},
            {"system": "AWS Console", "action": "Delete IAM user", "timing": "EOD last day", "status": "pending"},
            {"system": "Badge/Physical Access", "action": "Deactivate badge", "timing": "EOD last day", "status": "pending"},
            {"system": "HR System (Workday)", "action": "Mark as terminated", "timing": "Day after last day", "status": "pending"},
            {"system": "Benefits Portal", "action": "Send COBRA notice", "timing": "Within 14 days", "status": "pending"},
        ]

        return {
            "action": "access_revocation",
            "employee": name,
            "department": department,
            "last_day": last_day,
            "access_items": access_items,
            "total_systems": len(access_items),
            "checklist_owner": "IT Security",
            "hr_actions": [
                "Process final paycheck (within 72 hours)",
                "Send COBRA continuation notice",
                "Collect company equipment (laptop, badge, keys)",
                "Confirm PTO payout calculation",
            ],
            "status": "pending",
            "message": f"Access revocation checklist created for {name}: {len(access_items)} systems, last day {last_day}.",
        }

    def _full_offboarding(self, employee: dict, last_day: str) -> dict:
        name = employee.get("name", "Employee")
        return {
            "action": "full_offboarding",
            "employee": name,
            "last_day": last_day or "TBD",
            "exit_interview": self._conduct_exit_interview(employee, {}),
            "knowledge_transfer": self._plan_knowledge_transfer(employee, []),
            "access_revocation": self._revoke_access(employee, last_day),
            "status": "initiated",
            "message": f"Full offboarding workflow initiated for {name}. Last day: {last_day or 'TBD'}.",
        }
