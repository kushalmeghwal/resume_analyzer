"""Resume Extraction Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from ..tools.pdf_tool import extract_pdf_text
except ImportError:
    from tools.pdf_tool import extract_pdf_text

try:
    from google.adk.agents import Agent  # type: ignore

    extractor_adk_agent = Agent(
        name="resume_extraction_agent",
        model="gemini-1.5-flash",
        description="Extracts clean text from resume PDFs for downstream analysis.",
        instruction=(
            "Use the PDF extraction tool to read the resume file and return plain text. "
            "If extraction fails, return a concise error message."
        ),
    )
except Exception:
    extractor_adk_agent = None


class ResumeExtractionAgent:
    """Agent responsible for extracting text from a resume PDF."""

    name = "resume_extraction_agent"

    def run(self, resume_path: str) -> dict[str, Any]:
        """Extract and return resume text from a PDF path.

        Args:
            resume_path: Path to input PDF.

        Returns:
            Dict with `resume_path` and extracted `resume_text`.
        """
        path = Path(resume_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {resume_path}")

        text = extract_pdf_text(resume_path)
        return {"resume_path": resume_path, "resume_text": text}
