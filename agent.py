"""Root orchestrator for the Smart Resume Analyzer multi-agent workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from sub_agents.extractor_agent import ResumeExtractionAgent
from sub_agents.improvement_agent import ImprovementSuggestionAgent
from sub_agents.keyword_agent import KeywordAnalysisAgent
from sub_agents.report_agent import ReportGeneratorAgent

try:
    # Google ADK integration (kept optional so local CLI still works without ADK runtime).
    from google.adk.agents import Agent  # type: ignore
    from google.adk.tools import google_search  # type: ignore

    root_agent = Agent(
        name="smart_resume_analyzer_root",
        model="gemini-1.5-flash",
        description="Orchestrates resume extraction, keyword analysis, improvement suggestions, and report generation.",
        instruction=(
            "Coordinate sub-agents sequentially. Use google_search when external context is needed "
            "for role expectations or skill relevance. Return structured output for report generation."
        ),
        tools=[google_search],
    )
except Exception:
    root_agent = None


class ResumeAnalyzerOrchestrator:
    """Coordinates all sub-agents in a fixed sequential pipeline."""

    def __init__(self) -> None:
        load_dotenv()
        self.extractor = ResumeExtractionAgent()
        self.keyword_agent = KeywordAnalysisAgent()
        self.improvement_agent = ImprovementSuggestionAgent()
        self.report_agent = ReportGeneratorAgent()

    def run(self, resume_path: str, job_description: str, output_path: str = "resume_report.md") -> dict[str, Any]:
        """Execute full analysis workflow and return report metadata."""
        extraction = self.extractor.run(resume_path=resume_path)
        keyword_analysis = self.keyword_agent.run(
            resume_text=extraction["resume_text"],
            job_description=job_description,
        )
        improvements = self.improvement_agent.run(
            resume_text=extraction["resume_text"],
            job_description=job_description,
            keyword_analysis=keyword_analysis,
        )

        merged: dict[str, Any] = {}
        merged.update(keyword_analysis)
        merged.update(improvements)

        report_meta = self.report_agent.run(data=merged, output_path=output_path)
        return {
            "report_path": report_meta["report_path"],
            "match_score": merged.get("match_score", 0),
            "matching_skills": merged.get("matching_skills", []),
            "missing_keywords": merged.get("missing_keywords", []),
        }


def _read_job_description(value: str) -> str:
    """Read job description text from file path or use raw inline text."""
    path = Path(value)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return value


def main() -> None:
    """CLI entrypoint for local sequential execution."""
    parser = argparse.ArgumentParser(description="Smart Resume Analyzer")
    parser.add_argument("--resume", required=True, help="Path to resume PDF")
    parser.add_argument(
        "--job",
        required=True,
        help="Path to job description text file or raw job description string",
    )
    parser.add_argument("--out", default="resume_report.md", help="Output markdown report path")
    args = parser.parse_args()

    orchestrator = ResumeAnalyzerOrchestrator()
    result = orchestrator.run(
        resume_path=args.resume,
        job_description=_read_job_description(args.job),
        output_path=args.out,
    )
    print(f"Report generated: {result['report_path']}")
    print(f"Match score: {result['match_score']}%")


if __name__ == "__main__":
    main()
