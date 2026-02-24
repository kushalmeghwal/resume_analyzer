"""Keyword analysis tools for resume and job description matching."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
    "you",
    "your",
}


def _tokenize(text: str) -> list[str]:
    """Convert free text into normalized keyword tokens."""
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]*", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def analyze_keywords(resume_text: str, job_description: str) -> dict[str, Any]:
    """Compare resume text against job-description keywords.

    Args:
        resume_text: Extracted resume content.
        job_description: Target role description.

    Returns:
        Dict with matching skills, missing keywords, and match score.
    """
    resume_tokens = set(_tokenize(resume_text))
    jd_tokens = _tokenize(job_description)

    jd_counter = Counter(jd_tokens)
    ranked_jd_keywords = [kw for kw, _ in jd_counter.most_common(40)]

    matching = sorted([kw for kw in ranked_jd_keywords if kw in resume_tokens])
    missing = sorted([kw for kw in ranked_jd_keywords if kw not in resume_tokens])

    unique_jd = set(ranked_jd_keywords)
    score = int((len(matching) / max(len(unique_jd), 1)) * 100)

    return {
        "match_score": score,
        "matching_skills": matching[:20],
        "missing_keywords": missing[:20],
    }
