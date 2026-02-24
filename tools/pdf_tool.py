import pdfplumber

def extract_pdf_text(filepath: str) -> str:
    """Extract text from a PDF resume."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text