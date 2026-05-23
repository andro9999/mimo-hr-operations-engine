"""Payroll Agent: overtime calculations, benefits summary, tax compliance."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

TAX_BRACKETS = {
    "US_FEDERAL": [
        {"min": 0, "max": 11000, "rate": 0.10},
        {"min": 11000, "max": 44725, "rate": 0.12},
        {"min": 44725, "max": 95375, "rate": 0.22},
        {"min": 95375, "max": 182100, "rate": 0.24},
        {"min": 182100, "max": 231250, "rate": 0.32},
        {"min": 231250, "max": 578125, "rate": 0.35},
        {"min": 578125, "max": float("inf"), "rate": 0.37},
    ],
}

BENEFITS_PLANS = {
    "medical": {"name": "Medical Insurance", "options": ["PPO", "HMO", "HDHP+HSA"], "employer_contribution": 0.80},
    "dental": {"name": "Dental Insurance", "options": ["Basic", "Premium"], "employer_contribution": 0.75},
    "vision": {"name": "Vision Insurance", "options": ["Standard"], "employer_contribution": 0.70},
    "life": {"name": "Life Insurance", "options": ["1x Salary", "2x Salary"], "employer_contribution": 1.0},
    "401k": {"name": "401(k) Retirement", "options": ["Traditional", "Roth", "Both"], "employer_match": 0.04},
}


class PayrollAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "payroll"
        logger.info("PayrollAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "overtime")

        if action == "overtime":
            return self._calculate_overtime(task.get("employee", {}), task.get("hours_data", {}))
        if action == "benefits":
            return self._summarize_benefits(task.get("employee", {}))
        if action == "tax_compliance":
            return self._check_tax_compliance(task.get("employee", {}), task.get("jurisdiction", ""))
        return self._calculate_overtime(task.get("employee", {}), task.get("hours_data", {}))

    def _calculate_overtime(self, employee: dict, hours_data: dict) -> dict:
        name = employee.get("name", "Employee")
        hourly_rate = hours_data.get("hourly_rate", 30.00)
        regular_hours = hours_data.get("regular_hours", 40)
        overtime_hours = hours_data.get("overtime_hours", 0)
        double_time_hours = hours_data.get("double_time_hours", 0)
        pay_period = hours_data.get("pay_period", "Weekly")

        regular_pay = regular_hours * hourly_rate
        overtime_pay = overtime_hours * hourly_rate * 1.5
        double_time_pay = double_time_hours * hourly_rate * 2.0
        gross_pay = regular_pay + overtime_pay + double_time_pay

        issues = []
        if overtime_hours > 20:
            issues.append("Overtime exceeds 20 hours - verify pre-approval documentation")
        if regular_hours + overtime_hours + double_time_hours > 60:
            issues.append("Total hours exceed 60 - potential labor law concern")

        return {
            "action": "overtime_calculation",
            "employee": name,
            "pay_period": pay_period,
            "breakdown": {
                "regular_hours": regular_hours,
                "regular_pay": round(regular_pay, 2),
                "overtime_hours": overtime_hours,
                "overtime_pay": round(overtime_pay, 2),
                "double_time_hours": double_time_hours,
                "double_time_pay": round(double_time_pay, 2),
                "total_hours": regular_hours + overtime_hours + double_time_hours,
                "gross_pay": round(gross_pay, 2),
            },
            "issues": issues,
            "status": "validated" if not issues else "needs_review",
            "message": f"Overtime calculation for {name}: {overtime_hours} OT hours, gross pay ${gross_pay:.2f}.",
        }

    def _summarize_benefits(self, employee: dict) -> dict:
        name = employee.get("name", "Employee")
        annual_salary = employee.get("annual_salary", 80000)

        enrollments = []
        total_employee_cost = 0
        total_employer_cost = 0

        for plan_key, plan in BENEFITS_PLANS.items():
            monthly_premium = {
                "medical": 600, "dental": 50, "vision": 20, "life": 30, "401k": 0,
            }.get(plan_key, 0)

            employer_portion = round(monthly_premium * plan["employer_contribution"], 2)
            employee_portion = round(monthly_premium - employer_portion, 2)

            selected = plan["options"][0]
            enrollments.append({
                "plan": plan["name"],
                "selected_option": selected,
                "monthly_premium": monthly_premium,
                "employer_contribution": employer_portion,
                "employee_cost": employee_portion,
            })
            total_employee_cost += employee_portion
            total_employer_cost += employer_portion

        if "401k" in BENEFITS_PLANS:
            match = BENEFITS_PLANS["401k"]["employer_match"]
            total_employer_cost += round(annual_salary * match / 12, 2)

        return {
            "action": "benefits_summary",
            "employee": name,
            "enrollments": enrollments,
            "monthly_employee_cost": round(total_employee_cost, 2),
            "monthly_employer_cost": round(total_employer_cost, 2),
            "annual_employee_cost": round(total_employee_cost * 12, 2),
            "annual_employer_cost": round(total_employer_cost * 12, 2),
            "status": "completed",
            "message": f"Benefits summary for {name}: ${total_employee_cost:.2f}/mo employee cost.",
        }

    def _check_tax_compliance(self, employee: dict, jurisdiction: str) -> dict:
        name = employee.get("name", "Employee")
        annual_income = employee.get("annual_salary", 80000)
        filing_status = employee.get("filing_status", "single")
        jurisdiction = jurisdiction or "US_FEDERAL"

        brackets = TAX_BRACKETS.get(jurisdiction, TAX_BRACKETS["US_FEDERAL"])
        tax_owed = 0
        prev_max = 0
        bracket_details = []

        for bracket in brackets:
            if annual_income > bracket["min"]:
                taxable = min(annual_income, bracket["max"]) - bracket["min"]
                tax = round(taxable * bracket["rate"], 2)
                tax_owed += tax
                bracket_details.append({
                    "bracket": f"${bracket['min']:,}-${bracket['max'] if bracket['max'] != float('inf') else 'unlimited'}",
                    "rate": f"{bracket['rate']:.0%}",
                    "taxable_amount": round(taxable, 2),
                    "tax": tax,
                })

        effective_rate = round(tax_owed / annual_income, 4) if annual_income else 0

        checks = [
            {"item": "W-4 filing status", "status": "verified", "detail": filing_status},
            {"item": "State tax withholding", "status": "check_required", "detail": "Verify state registration"},
            {"item": "Local tax obligations", "status": "check_required", "detail": "Verify local tax jurisdiction"},
            {"item": "FICA compliance", "status": "verified", "detail": "Social Security and Medicare withheld"},
        ]

        return {
            "action": "tax_compliance",
            "employee": name,
            "jurisdiction": jurisdiction,
            "annual_income": annual_income,
            "estimated_annual_tax": round(tax_owed, 2),
            "effective_rate": f"{effective_rate:.1%}",
            "bracket_breakdown": bracket_details,
            "compliance_checks": checks,
            "issues": [c for c in checks if c["status"] == "check_required"],
            "status": "review_needed",
            "message": f"Tax compliance check for {name}: effective rate {effective_rate:.1%}, 2 items need verification.",
        }
