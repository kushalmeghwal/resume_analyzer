"""Keyword Analysis Agent."""

from __future__ import annotations

from typing import Any

from tools.keyword_tool import analyze_keywords

try:
    from google.adk.agents import Agent  # type: ignore

    keyword_adk_agent = Agent(
        name="keyword_analysis_agent",
        model="gemini-1.5-flash",
        description="Compares extracted resume text against job-description keywords.",
        instruction=(
            "Identify matching and missing skills from the resume relative to the target role. "
            "Return a deterministic structure with match score, matching_skills, and missing_keywords."
        ),
    )
except Exception:
    keyword_adk_agent = None


class KeywordAnalysisAgent:
    """Agent responsible for keyword matching and gap analysis."""

    name = "keyword_analysis_agent"

    def run(self, resume_text: str, job_description: str) -> dict[str, Any]:
        """Analyze keyword matches and missing terms for the target role.

        Args:
            resume_text: Extracted plain text from resume.
            job_description: Target role requirements.

        Returns:
            Structured keyword analysis.
        """
        if not resume_text.strip():
            raise ValueError("resume_text is empty; cannot run keyword analysis")
        if not job_description.strip():
            raise ValueError("job_description is empty; cannot run keyword analysis")

        return analyze_keywords(resume_text=resume_text, job_description=job_description)
