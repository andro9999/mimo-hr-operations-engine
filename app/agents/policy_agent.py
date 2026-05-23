"""Policy Agent: HR questions, policy interpretation, compliance checks."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

POLICY_KNOWLEDGE_BASE = {
    "pto": {
        "title": "Paid Time Off Policy",
        "content": "Full-time employees accrue 15 days PTO per year, increasing to 20 days after 3 years. PTO must be requested 2 weeks in advance for absences exceeding 3 days. Maximum carryover is 5 days.",
        "category": "leave",
    },
    "remote_work": {
        "title": "Remote Work Policy",
        "content": "Employees may work remotely up to 3 days per week with manager approval. Fully remote arrangements require VP-level approval. Core hours are 10am-3pm in the employee's local timezone.",
        "category": "work_arrangement",
    },
    "expense": {
        "title": "Expense Reimbursement Policy",
        "content": "Business expenses under $500 require manager approval. Expenses $500-$2000 require director approval. Over $2000 requires VP approval. Submit within 30 days of expense. Receipts required for all expenses over $25.",
        "category": "finance",
    },
    "harassment": {
        "title": "Anti-Harassment Policy",
        "content": "Zero tolerance for harassment of any kind. Report to HR or use the anonymous hotline. All complaints investigated within 48 hours. Retaliation is strictly prohibited.",
        "category": "compliance",
    },
    "overtime": {
        "title": "Overtime Policy",
        "content": "Non-exempt employees are eligible for overtime at 1.5x rate for hours over 40/week. Overtime must be pre-approved by manager. Comp time is not offered in lieu of overtime pay.",
        "category": "compensation",
    },
}


class PolicyAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "policy"
        logger.info("PolicyAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "ask")
        question = task.get("question", "")

        if action == "ask":
            return self._answer_question(question)
        if action == "interpret":
            return self._interpret_policy(task.get("policy", ""), task.get("scenario", ""))
        if action == "compliance_check":
            return self._check_compliance(task.get("area", ""), task.get("details", {}))
        return self._answer_question(question)

    def _answer_question(self, question: str) -> dict:
        q_lower = question.lower()
        matched_policies = []
        for key, policy in POLICY_KNOWLEDGE_BASE.items():
            if key.replace("_", " ") in q_lower or any(w in q_lower for w in key.split("_")):
                matched_policies.append(policy)

        if not matched_policies:
            matched_policies = [POLICY_KNOWLEDGE_BASE["pto"]]
            note = "No exact policy match found. Showing most commonly referenced policy."
        else:
            note = f"Found {len(matched_policies)} relevant policy(ies)."

        return {
            "action": "ask",
            "question": question,
            "relevant_policies": matched_policies,
            "guidance": note,
            "status": "answered",
            "message": f"Policy response generated for question: '{question}'",
        }

    def _interpret_policy(self, policy: str, scenario: str) -> dict:
        interpretations = {
            "pto": "Based on the PTO policy, the scenario appears to be within guidelines provided the request was submitted with proper advance notice.",
            "remote_work": "The remote work arrangement described may be approved if manager and department guidelines are met.",
            "expense": "This expense appears to fall under the standard reimbursement process. Ensure receipts are attached.",
            "harassment": "This scenario should be escalated to HR immediately for a formal investigation.",
            "overtime": "The overtime described would be compensated at 1.5x the regular rate if pre-approved.",
        }
        key = policy.lower().replace(" ", "_")
        interpretation = interpretations.get(key, "This scenario requires further review by the HR team.")

        return {
            "action": "interpret",
            "policy": policy,
            "scenario": scenario,
            "interpretation": interpretation,
            "risk_level": "low",
            "requires_hr_review": False,
            "status": "completed",
            "message": f"Policy interpretation completed for '{policy}'.",
        }

    def _check_compliance(self, area: str, details: dict) -> dict:
        compliance_areas = {
            "record_keeping": {
                "requirements": ["I-9 forms on file", "Tax documents retained 4 years", "Medical records separate"],
                "status": "pass",
            },
            "workplace_safety": {
                "requirements": ["OSHA postings displayed", "Emergency exits clear", "First aid kit stocked"],
                "status": "pass",
            },
            "anti_discrimination": {
                "requirements": ["EEO policy posted", "Training completed within 90 days", "Complaint process documented"],
                "status": "review_needed",
            },
        }
        check = compliance_areas.get(area, {
            "requirements": ["Manual review required"],
            "status": "unknown",
        })

        return {
            "action": "compliance_check",
            "area": area,
            "details": details,
            "findings": check,
            "recommendations": ["Schedule quarterly compliance audits", "Update training records"],
            "status": check["status"],
            "message": f"Compliance check for '{area}' completed with status: {check['status']}.",
        }
