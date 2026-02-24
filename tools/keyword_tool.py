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

CANONICAL_SKILLS = [
    "python",
    "django",
    "fastapi",
    "flask",
    "rest api",
    "postgresql",
    "mysql",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "azure",
    "microservices",
    "ci/cd",
    "unit testing",
    "pytest",
    "git",
    "sql",
    "redis",
    "celery",
]


def _tokenize(text: str) -> list[str]:
    """Convert free text into normalized keyword tokens."""
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]*", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def _normalize_text(text: str) -> str:
    """Normalize text for phrase-based matching."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def _extract_skill_mentions(text: str) -> set[str]:
    """Extract canonical skill mentions from free text."""
    normalized = _normalize_text(text)
    found: set[str] = set()
    for skill in CANONICAL_SKILLS:
        if skill in normalized:
            found.add(skill)
    return found


def analyze_keywords(resume_text: str, job_description: str) -> dict[str, Any]:
    """Compare resume text against job-description keywords.

    Args:
        resume_text: Extracted resume content.
        job_description: Target role description.

    Returns:
        Dict with matching skills, missing keywords, and match score.
    """
    if not resume_text.strip():
        raise ValueError("resume_text cannot be empty")
    if not job_description.strip():
        raise ValueError("job_description cannot be empty")

    resume_tokens = set(_tokenize(resume_text))
    jd_tokens = _tokenize(job_description)

    jd_counter = Counter(jd_tokens)
    ranked_jd_keywords = [kw for kw, _ in jd_counter.most_common(40)]

    token_matching = {kw for kw in ranked_jd_keywords if kw in resume_tokens}
    token_missing = {kw for kw in ranked_jd_keywords if kw not in resume_tokens}

    jd_skills = _extract_skill_mentions(job_description)
    resume_skills = _extract_skill_mentions(resume_text)
    skill_matching = jd_skills.intersection(resume_skills)
    skill_missing = jd_skills.difference(resume_skills)

    matching = sorted(token_matching.union(skill_matching))
    missing = sorted(token_missing.union(skill_missing))

    unique_jd = set(ranked_jd_keywords).union(jd_skills)
    score = int((len(matching) / max(len(unique_jd), 1)) * 100)

    return {
        "match_score": score,
        "matching_skills": matching[:20],
        "missing_keywords": missing[:20],
    }
