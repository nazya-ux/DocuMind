
import hashlib
from pathlib import Path

import chromadb


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    folders = [
        Path("data/documents"),
        Path("data/uploads"),
    ]

    # Map PDF content hashes to their best available filenames.
    filenames_by_hash = {}

    for folder in folders:
        if not folder.exists():
            continue

        for pdf in folder.glob("*.pdf"):
            digest = sha256_file(pdf)
            current = filenames_by_hash.get(digest)

            # Prefer descriptive names over hash-only filenames.
            is_hash_only = (
                len(pdf.stem) == 64
                and all(c in "0123456789abcdef" for c in pdf.stem.lower())
            )

            if current is None:
                filenames_by_hash[digest] = (pdf.name, is_hash_only)
            elif current[1] and not is_hash_only:
                filenames_by_hash[digest] = (pdf.name, is_hash_only)

    client = chromadb.PersistentClient(path="data/vectorstore")
    collection = client.get_or_create_collection(
        name="documind_local"
    )

    records = collection.get(include=["metadatas"])
    updated = 0

    for record_id, metadata in zip(
        records["ids"],
        records["metadatas"],
    ):
        if not metadata:
            continue

        file_id = metadata.get("file_id")
        match = filenames_by_hash.get(file_id)

        if not match:
            continue

        original_name = match[0]

        if metadata.get("source") != original_name:
            metadata["source"] = original_name
            collection.update(
                ids=[record_id],
                metadatas=[metadata],
            )
            updated += 1

    print(f"PDF content hashes matched: {len(filenames_by_hash)}")
    print(f"Records updated: {updated}")
    print(f"Total records checked: {len(records['ids'])}")


if __name__ == "__main__":
    main()
