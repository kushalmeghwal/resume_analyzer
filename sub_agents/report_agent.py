"""Report Generator Agent."""

from __future__ import annotations

from typing import Any

from tools.report_tool import generate_markdown_report


class ReportGeneratorAgent:
    """Agent responsible for writing final markdown report to disk."""

    name = "report_generator_agent"

    def run(self, data: dict[str, Any], output_path: str = "resume_report.md") -> dict[str, Any]:
        """Generate markdown report and return output metadata."""
        path = generate_markdown_report(data=data, output_path=output_path)
        return {"report_path": path}
