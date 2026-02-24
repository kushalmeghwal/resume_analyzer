"""PDF extraction tools for resume parsing."""

from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_pdf_text(filepath: str) -> str:
    """Extract plain text from all pages in a PDF file.

    Args:
        filepath: Absolute or relative path to the PDF file.

    Returns:
        A single string containing extracted text across all pages.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the input is not a PDF file or no text is found.
    """
    file_path = Path(filepath)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {filepath}")
    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a .pdf")

    pages: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text.strip())

    if not pages:
        raise ValueError("No readable text found in PDF")

    return "\n\n".join(pages)
