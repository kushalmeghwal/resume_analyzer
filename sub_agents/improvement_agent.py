"""Improvement Suggestion Agent."""

from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai


class ImprovementSuggestionAgent:
    """Agent responsible for generating targeted resume improvements."""

    name = "improvement_suggestion_agent"

    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        """Initialize the agent with a Gemini model name."""
        self.model_name = model_name

    def _fallback_suggestions(self, missing_keywords: list[str]) -> dict[str, Any]:
        """Provide deterministic suggestions when LLM generation is unavailable."""
        top_missing = missing_keywords[:5]
        suggestions = [f"Add measurable experience with {kw}." for kw in top_missing]
        if not suggestions:
            suggestions = ["Increase impact-focused bullets with quantified results."]
        return {
            "suggested_improvements": suggestions,
            "summary": "Resume has relevant baseline skills; add missing role-specific keywords with project outcomes.",
        }

    def run(
        self,
        resume_text: str,
        job_description: str,
        keyword_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate improvement suggestions from keyword gaps and context."""
        missing_keywords = keyword_analysis.get("missing_keywords", [])
        api_key = os.getenv("GOOGLE_API_KEY", "").strip()
        if not api_key:
            return self._fallback_suggestions(missing_keywords)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.model_name)

        prompt = (
            "You are a resume optimization assistant. "
            "Given resume text, job description, and missing keywords, return concise JSON with keys "
            "'suggested_improvements' (list of bullet-ready strings) and 'summary' (2 sentences max)."
            f"\n\nResume:\n{resume_text[:6000]}"
            f"\n\nJob Description:\n{job_description[:3000]}"
            f"\n\nMissing Keywords:\n{missing_keywords}"
        )

        try:
            response = model.generate_content(prompt)
            text = (response.text or "").strip()
        except Exception:
            return self._fallback_suggestions(missing_keywords)

        if not text:
            return self._fallback_suggestions(missing_keywords)

        lines = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
        suggestions = [line for line in lines if len(line) > 20][:6]
        if not suggestions:
            return self._fallback_suggestions(missing_keywords)

        return {
            "suggested_improvements": suggestions,
            "summary": "Suggestions generated using Gemini based on detected keyword gaps.",
        }
