"""Resume Extraction Agent."""

from __future__ import annotations

from typing import Any

from tools.pdf_tool import extract_pdf_text


class ResumeExtractionAgent:
    """Agent responsible for extracting text from a resume PDF."""

    name = "resume_extraction_agent"

    def run(self, resume_path: str) -> dict[str, Any]:
        """Extract and return resume text from a PDF path."""
        text = extract_pdf_text(resume_path)
        return {"resume_path": resume_path, "resume_text": text}
