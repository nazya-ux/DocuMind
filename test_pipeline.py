
from pathlib import Path

from src.document_loader import load_pdf
from src.text_splitter import split_text


pdf_folder = Path("data/documents")
pdf_files = list(pdf_folder.glob("*.pdf"))

if not pdf_files:
    print("Add a PDF to data/documents/ and run this test again.")
else:
    pdf_path = pdf_files[0]

    text = load_pdf(str(pdf_path))
    chunks = split_text(text)

    print("\n--- RESULTS ---")
    print("PDF:", pdf_path.name)
    print("Total characters:", len(text))
    print("Total chunks:", len(chunks))

    if chunks:
        print("\n--- FIRST CHUNK ---")
        print(chunks[0])
