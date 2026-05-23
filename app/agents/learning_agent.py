"""Learning Agent: skill gap analysis, course recommendations, certification tracking."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

COURSE_CATALOG = {
    "python_advanced": {"title": "Advanced Python Patterns", "platform": "Internal", "duration": "8 hours", "level": "advanced"},
    "leadership_101": {"title": "Leadership Fundamentals", "platform": "LinkedIn Learning", "duration": "6 hours", "level": "intermediate"},
    "cloud_aws": {"title": "AWS Solutions Architect Prep", "platform": "A Cloud Guru", "duration": "40 hours", "level": "advanced"},
    "data_analysis": {"title": "Data Analysis with SQL", "platform": "Coursera", "duration": "20 hours", "level": "intermediate"},
    "project_mgmt": {"title": "Project Management Essentials", "platform": "Internal", "duration": "12 hours", "level": "beginner"},
    "communication": {"title": "Effective Communication", "platform": "Internal", "duration": "4 hours", "level": "beginner"},
    "security_awareness": {"title": "Cybersecurity Awareness", "platform": "KnowBe4", "duration": "2 hours", "level": "beginner"},
}

CERTIFICATIONS = {
    "aws_sa": {"name": "AWS Solutions Architect - Associate", "provider": "AWS", "valid_years": 3},
    "pmp": {"name": "Project Management Professional", "provider": "PMI", "valid_years": 3},
    "phr": {"name": "Professional in Human Resources", "provider": "HRCI", "valid_years": 3},
    "csm": {"name": "Certified Scrum Master", "provider": "Scrum Alliance", "valid_years": 2},
}


class LearningAgent:
    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.name = "learning"
        logger.info("LearningAgent created")

    async def execute(self, task: dict) -> dict:
        action = task.get("action", "skill_gap")

        if action == "skill_gap":
            return self._analyze_skill_gap(task.get("employee", {}), task.get("target_role", ""))
        if action == "recommend_courses":
            return self._recommend_courses(task.get("employee", {}), task.get("skills_needed", []))
        if action == "certification":
            return self._track_certifications(task.get("employee", {}), task.get("certifications", []))
        return self._analyze_skill_gap(task.get("employee", {}), task.get("target_role", ""))

    def _analyze_skill_gap(self, employee: dict, target_role: str) -> dict:
        name = employee.get("name", "Employee")
        current_skills = employee.get("skills", ["Python", "SQL", "Communication"])
        target_role = target_role or "Senior Engineer"

        role_requirements = {
            "Senior Engineer": ["Python", "System Design", "Leadership", "Cloud Architecture", "Mentoring"],
            "Engineering Manager": ["Leadership", "Strategic Planning", "Budgeting", "Hiring", "Communication"],
            "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
            "Product Manager": ["Market Analysis", "User Research", "Roadmapping", "Communication", "SQL"],
        }
        required = role_requirements.get(target_role, role_requirements["Senior Engineer"])
        gaps = [s for s in required if s not in current_skills]
        strengths = [s for s in required if s in current_skills]

        return {
            "action": "skill_gap",
            "employee": name,
            "target_role": target_role,
            "current_skills": current_skills,
            "required_skills": required,
            "gaps": gaps,
            "strengths": strengths,
            "readiness_score": round(len(strengths) / len(required) * 100) if required else 0,
            "status": "completed",
            "message": f"Skill gap analysis for {name} targeting {target_role}: {len(gaps)} gaps identified.",
        }

    def _recommend_courses(self, employee: dict, skills_needed: list) -> dict:
        name = employee.get("name", "Employee")
        skill_course_map = {
            "Leadership": ["leadership_101"],
            "Cloud Architecture": ["cloud_aws"],
            "System Design": ["cloud_aws", "python_advanced"],
            "Mentoring": ["leadership_101"],
            "Communication": ["communication"],
            "SQL": ["data_analysis"],
            "Python": ["python_advanced"],
            "Project Management": ["project_mgmt"],
        }

        recommended = []
        seen = set()
        for skill in skills_needed:
            for course_key in skill_course_map.get(skill, []):
                if course_key not in seen:
                    seen.add(course_key)
                    course = COURSE_CATALOG[course_key]
                    course["course_id"] = course_key
                    course["addresses_skill"] = skill
                    recommended.append(course)

        if not recommended:
            recommended = [
                {**COURSE_CATALOG["leadership_101"], "course_id": "leadership_101", "addresses_skill": "General Development"},
                {**COURSE_CATALOG["communication"], "course_id": "communication", "addresses_skill": "Communication"},
            ]

        return {
            "action": "recommend_courses",
            "employee": name,
            "skills_needed": skills_needed or ["General Development"],
            "recommended_courses": recommended,
            "total_learning_hours": sum(int(c.get("duration", "0").split()[0]) for c in recommended),
            "status": "completed",
            "message": f"Course recommendations generated for {name}: {len(recommended)} courses suggested.",
        }

    def _track_certifications(self, employee: dict, certifications: list) -> dict:
        name = employee.get("name", "Employee")
        if not certifications:
            certifications = [
                {"cert_id": "aws_sa", "status": "in_progress", "exam_date": "2026-03-15", "prep_progress": 60},
                {"cert_id": "csm", "status": "completed", "obtained_date": "2025-06-01", "expires": "2027-06-01"},
            ]

        enriched = []
        for cert in certifications:
            cert_info = CERTIFICATIONS.get(cert.get("cert_id", ""), {})
            enriched.append({**cert, "cert_name": cert_info.get("name", "Unknown"), "provider": cert_info.get("provider", "Unknown")})

        active = [c for c in enriched if c.get("status") == "completed"]
        in_progress = [c for c in enriched if c.get("status") == "in_progress"]

        return {
            "action": "certification_tracking",
            "employee": name,
            "certifications": enriched,
            "active_certifications": len(active),
            "in_progress": len(in_progress),
            "status": "completed",
            "message": f"Certification status for {name}: {len(active)} active, {len(in_progress)} in progress.",
        }
