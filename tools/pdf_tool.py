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
    if not filepath.strip():
        raise ValueError("filepath cannot be empty")
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {filepath}")
    if not file_path.is_file():
        raise ValueError(f"Expected a file path, got: {filepath}")
    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a .pdf")

    pages: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            cleaned = text.strip()
            if cleaned:
                pages.append(cleaned)
            elif page_index == 1 and len(pdf.pages) == 1:
                # Common with image-only resumes; surfacing a clear message helps debugging.
                continue

    if not pages:
        raise ValueError(
            "No readable text found in PDF. The file may be image-based/scanned; "
            "OCR is required for such resumes."
        )

    return "\n\n".join(pages)
