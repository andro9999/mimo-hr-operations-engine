"""Onboarding Agent: paperwork, IT setup, training schedule, buddy pairing."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

CAPABILITIES = [
    "paperwork_generation",
    "it_setup_coordination",
    "training_schedule",
    "buddy_pairing",
]


class OnboardingAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "onboarding"
        kernel.event_bus.subscribe("agent.start", self._on_agent_start)
        logger.info("OnboardingAgent created")

    async def _on_agent_start(self, data: dict) -> None:
        pass

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "full_onboarding")
        employee = task.get("employee", {})
        employee_name = employee.get("name", "New Hire")
        department = employee.get("department", "General")
        start_date = employee.get("start_date", "TBD")

        if action == "paperwork":
            return self._generate_paperwork(employee_name, department)
        if action == "it_setup":
            return self._coordinate_it_setup(employee_name, department)
        if action == "training":
            return self._assign_training(employee_name, department)
        if action == "buddy":
            return self._pair_buddy(employee_name, department)
        return self._full_onboarding(employee_name, department, start_date)

    def _generate_paperwork(self, name: str, department: str) -> dict:
        documents = [
            "Employment contract",
            "Tax withholding forms (W-4)",
            "Direct deposit authorization",
            "NDA and IP assignment",
            "Employee handbook acknowledgment",
            "Benefits enrollment form",
            "Emergency contact card",
        ]
        return {
            "action": "paperwork",
            "employee": name,
            "department": department,
            "documents": documents,
            "status": "generated",
            "message": f"Onboarding paperwork package generated for {name} ({department}).",
        }

    def _coordinate_it_setup(self, name: str, department: str) -> dict:
        dept_tools = {
            "Engineering": ["GitHub", "Jira", "Slack", "AWS Console", "VPN"],
            "Marketing": ["HubSpot", "Slack", "Google Workspace", "Canva"],
            "Sales": ["Salesforce", "Slack", "Google Workspace", "Zoom"],
            "HR": ["Workday", "Slack", "Google Workspace", "DocuSign"],
            "Finance": ["NetSuite", "Slack", "Google Workspace", "Excel"],
        }
        tools = dept_tools.get(department, ["Slack", "Google Workspace", "Zoom"])
        tasks = [
            {"task": f"Create account for {tool}", "status": "pending", "eta": "1 business day"}
            for tool in tools
        ]
        return {
            "action": "it_setup",
            "employee": name,
            "department": department,
            "accounts_to_provision": tools,
            "setup_tasks": tasks,
            "status": "requested",
            "message": f"IT setup request submitted for {name}. {len(tools)} accounts to provision.",
        }

    def _assign_training(self, name: str, department: str) -> dict:
        training = [
            {"module": "Company Values and Culture", "duration": "2 hours", "format": "e-learning"},
            {"module": "Security Awareness", "duration": "1 hour", "format": "e-learning"},
            {"module": "Compliance Fundamentals", "duration": "1.5 hours", "format": "e-learning"},
            {"module": f"{department} Department Orientation", "duration": "3 hours", "format": "in-person"},
            {"module": "Tool Onboarding", "duration": "2 hours", "format": "hands-on lab"},
        ]
        return {
            "action": "training",
            "employee": name,
            "department": department,
            "training_modules": training,
            "total_hours": 9.5,
            "deadline": "First 2 weeks",
            "status": "scheduled",
            "message": f"Training schedule assigned for {name}. 9.5 hours total over 2 weeks.",
        }

    def _pair_buddy(self, name: str, department: str) -> dict:
        buddy_pool = {
            "Engineering": ["Alex Chen (Sr. Engineer)", "Maria Lopez (Tech Lead)"],
            "Marketing": ["James Park (Content Lead)", "Sara Kim (Growth Mgr)"],
            "Sales": ["Mike Davis (Account Exec)", "Lisa Wong (Sales Ops)"],
            "HR": ["Karen White (HR Generalist)", "Tom Brown (Recruiter)"],
            "Finance": ["Nina Patel (Analyst)", "Ryan Lee (Controller)"],
        }
        buddies = buddy_pool.get(department, ["Jordan Smith (Team Lead)"])
        selected = buddies[0]
        return {
            "action": "buddy_pairing",
            "employee": name,
            "department": department,
            "assigned_buddy": selected,
            "alternates": buddies[1:],
            "buddy_program_duration": "90 days",
            "first_meeting": "Day 1 lunch",
            "status": "assigned",
            "message": f"Buddy {selected} assigned for {name} in {department}.",
        }

    def _full_onboarding(self, name: str, department: str, start_date: str) -> dict:
        return {
            "action": "full_onboarding",
            "employee": name,
            "department": department,
            "start_date": start_date,
            "paperwork": self._generate_paperwork(name, department),
            "it_setup": self._coordinate_it_setup(name, department),
            "training": self._assign_training(name, department),
            "buddy": self._pair_buddy(name, department),
            "status": "initiated",
            "message": f"Full onboarding workflow initiated for {name} starting {start_date}.",
        }
