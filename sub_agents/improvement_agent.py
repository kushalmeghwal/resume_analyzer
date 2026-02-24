"""Improvement Suggestion Agent."""

from __future__ import annotations

import json
import os
from typing import Any

import google.generativeai as genai

try:
    from google.adk.agents import Agent  # type: ignore

    improvement_adk_agent = Agent(
        name="improvement_suggestion_agent",
        model="gemini-1.5-flash",
        description="Suggests resume improvements based on detected keyword gaps.",
        instruction=(
            "Recommend practical resume improvements, action verbs, and missing technologies "
            "for the target Python role. Keep output concise and actionable."
        ),
    )
except Exception:
    improvement_adk_agent = None


class ImprovementSuggestionAgent:
    """Agent responsible for generating targeted resume improvements."""

    name = "improvement_suggestion_agent"

    def __init__(self, model_name: str = "gemini-1.5-flash") -> None:
        """Initialize the agent with a Gemini model name."""
        self.model_name = model_name

    def _fallback_suggestions(self, missing_keywords: list[str]) -> dict[str, Any]:
        """Provide deterministic suggestions when LLM generation is unavailable."""
        top_missing = missing_keywords[:4]
        suggestions = [f"Add project bullets showing hands-on experience with {kw}." for kw in top_missing]
        suggestions.append("Use strong action verbs such as Designed, Implemented, Optimized, and Automated.")
        suggestions.append("Quantify impact (latency reduction, throughput gain, or cost savings) in each core bullet.")
        return {
            "suggested_improvements": suggestions,
            "summary": "Resume has a solid baseline; align it better with Python backend expectations and measurable outcomes.",
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
            "You are a resume optimization assistant for Python backend roles. "
            "Return strict JSON with this schema: "
            "{\"suggested_improvements\": [str], \"summary\": str}. "
            "Suggestions must include missing technologies and action-verb usage guidance."
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

        # Prefer strict JSON parsing; fallback to line parsing if model adds formatting.
        parsed: dict[str, Any] | None = None
        try:
            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`")
                cleaned = cleaned.replace("json", "", 1).strip()
            candidate = json.loads(cleaned)
            if isinstance(candidate, dict):
                parsed = candidate
        except Exception:
            parsed = None

        if parsed:
            suggestions = parsed.get("suggested_improvements", [])
            summary = parsed.get("summary", "")
            if isinstance(suggestions, list) and suggestions:
                safe_suggestions = [str(item).strip() for item in suggestions if str(item).strip()][:8]
                if safe_suggestions:
                    return {
                        "suggested_improvements": safe_suggestions,
                        "summary": str(summary).strip() or "Suggestions generated based on keyword analysis.",
                    }

        lines = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
        suggestions = [line for line in lines if len(line) > 20][:8]
        if not suggestions:
            return self._fallback_suggestions(missing_keywords)

        return {
            "suggested_improvements": suggestions,
            "summary": "Suggestions generated using Gemini based on detected keyword and experience gaps.",
        }
