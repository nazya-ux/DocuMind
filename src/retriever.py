
import chromadb

from src.embeddings import embed_texts


chroma = chromadb.PersistentClient(path="data/vectorstore")
collection = chroma.get_or_create_collection(
    name="documind_local"
)


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Find relevant chunks using local embeddings."""

    if collection.count() == 0:
        raise ValueError(
            "No documents indexed yet. Upload and index a PDF first."
        )

    query_vector = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    passages = []

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        passages.append({
            "text": document,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": results["distances"][0][i],
        })

    return passages
