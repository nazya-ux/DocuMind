
import hashlib
from pathlib import Path

import chromadb

from src.document_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings import embed_texts


def get_original_filename(filename: str) -> str:
    """Remove a 64-character SHA256 prefix from an uploaded filename."""
    name = Path(filename).name

    if "_" in name:
        prefix, remainder = name.split("_", 1)

        if len(prefix) == 64 and all(
            character in "0123456789abcdef"
            for character in prefix.lower()
        ):
            return remainder

    return name


def index_pdf(pdf_path: str) -> int:
    """Extract, chunk, embed locally, and index a PDF."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    original_name = get_original_filename(pdf_path.name)

    print(f"\nLoading PDF: {original_name}")

    text = load_pdf(str(pdf_path))
    chunks = split_text(text)

    if not chunks:
        raise ValueError(
            f"No text chunks extracted from {original_name}."
        )

    print(f"Created {len(chunks)} chunks.")

    # Identify the document by its actual contents.
    file_id = hashlib.sha256(pdf_path.read_bytes()).hexdigest()

    db_path = Path("data/vectorstore")
    db_path.mkdir(parents=True, exist_ok=True)

    chroma = chromadb.PersistentClient(path=str(db_path))

    # Local MiniLM embeddings use a separate collection.
    collection = chroma.get_or_create_collection(
        name="documind_local"
    )

    batch_size = 20

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        end = start + len(batch)

        ids = [
            f"{file_id}_chunk_{i}"
            for i in range(start, end)
        ]

        # Skip chunks already indexed.
        existing = collection.get(ids=ids)
        existing_ids = set(existing["ids"])

        missing = [
            (i, chunk, chunk_id)
            for i, (chunk, chunk_id) in enumerate(
                zip(batch, ids), start=start
            )
            if chunk_id not in existing_ids
        ]

        if not missing:
            print(
                f"Skipped existing chunks through {end}/{len(chunks)}"
            )
            continue

        missing_texts = [item[1] for item in missing]
        vectors = embed_texts(missing_texts)

        collection.upsert(
            ids=[item[2] for item in missing],
            documents=missing_texts,
            embeddings=vectors,
            metadatas=[
                {
                    "source": original_name,
                    "file_id": file_id,
                    "chunk_index": i,
                }
                for i, _, _ in missing
            ],
        )

        print(f"Indexed through {end}/{len(chunks)} chunks")

    print(f"Finished indexing: {original_name}")
    print(f"Total chunks in this PDF: {len(chunks)}")
    print(f"Total chunks in local database: {collection.count()}")

    return len(chunks)


if __name__ == "__main__":
    pdf_folder = Path("data/documents")
    pdf_files = list(pdf_folder.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDFs found in data/documents/"
        )

    for pdf_file in pdf_files:
        try:
            index_pdf(str(pdf_file))
        except Exception as error:
            print(f"Failed to index {pdf_file.name}: {error}")
