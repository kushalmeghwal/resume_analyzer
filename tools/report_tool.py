"""Markdown report generation tools for resume analysis output."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_markdown_report(data: dict[str, Any], output_path: str = "resume_report.md") -> str:
    """Generate and save a structured markdown resume analysis report.

    Args:
        data: Aggregated analysis dictionary.
        output_path: Output markdown filename/path.

    Returns:
        The output path where the report was saved.
    """
    match_score = data.get("match_score", 0)
    matching_skills = data.get("matching_skills", [])
    missing_keywords = data.get("missing_keywords", [])
    suggestions = data.get("suggested_improvements", [])
    summary = data.get("summary", "No summary generated.")

    lines: list[str] = [
        "# Resume Analysis Report",
        "",
        "## Match Score",
        f"{match_score}%",
        "",
        "## Matching Skills",
    ]

    if matching_skills:
        lines.extend([f"- {skill}" for skill in matching_skills])
    else:
        lines.append("- None identified")

    lines.extend(["", "## Missing Keywords"])
    if missing_keywords:
        lines.extend([f"- {kw}" for kw in missing_keywords])
    else:
        lines.append("- None")

    lines.extend(["", "## Suggested Improvements"])
    if suggestions:
        lines.extend([f"- {item}" for item in suggestions])
    else:
        lines.append("- Add more role-specific project impact statements")

    lines.extend(["", "## Summary", summary, ""])

    report_text = "\n".join(lines)
    report_file = Path(output_path)
    report_file.write_text(report_text, encoding="utf-8")
    return str(report_file)
