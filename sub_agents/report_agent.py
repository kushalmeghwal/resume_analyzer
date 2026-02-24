"""Report Generator Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from ..tools.report_tool import generate_markdown_report
except ImportError:
    from tools.report_tool import generate_markdown_report

try:
    from google.adk.agents import Agent  # type: ignore

    report_adk_agent = Agent(
        name="report_generator_agent",
        model="gemini-1.5-flash",
        description="Generates a final markdown report from aggregated analysis data.",
        instruction=(
            "Produce a clean, structured markdown report containing match score, matching skills, "
            "missing keywords, suggested improvements, and a short summary."
        ),
    )
except Exception:
    report_adk_agent = None


class ReportGeneratorAgent:
    """Agent responsible for writing final markdown report to disk."""

    name = "report_generator_agent"

    def run(self, data: dict[str, Any], output_path: str = "resume_report.md") -> dict[str, Any]:
        """Generate markdown report and return output metadata.

        Args:
            data: Aggregated analysis payload.
            output_path: Desired markdown output path.

        Returns:
            Dict containing resolved report path.
        """
        if not data:
            raise ValueError("Cannot generate report with empty data payload")

        target = Path(output_path)
        if not target.suffix:
            target = target.with_suffix(".md")

        path = generate_markdown_report(data=data, output_path=str(target))
        return {"report_path": str(Path(path).resolve())}
