
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load the model once and reuse it.
model = SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate text embeddings locally without an API request."""

    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    return vectors.tolist()
