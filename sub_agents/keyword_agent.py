"""Keyword Analysis Agent."""

from __future__ import annotations

from typing import Any

from tools.keyword_tool import analyze_keywords


class KeywordAnalysisAgent:
    """Agent responsible for keyword matching and gap analysis."""

    name = "keyword_analysis_agent"

    def run(self, resume_text: str, job_description: str) -> dict[str, Any]:
        """Analyze keyword matches and missing terms for the target role."""
        return analyze_keywords(resume_text=resume_text, job_description=job_description)
