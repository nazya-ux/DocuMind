
from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF and return it as one string."""

    pdf_path = Path(file_path)
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(text)

        print(f"Read page {page_number}: {len(text)} characters")

    full_text = "\n".join(pages)

    if not full_text.strip():
        raise ValueError(
            "No text was extracted. This PDF may contain scanned images."
        )

    return full_text
