
from src.retriever import retrieve

question = "Why do large language models produce hallucinations?"

results = retrieve(question, top_k=5)

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(f"Source: {result['source']}")
    print(f"Chunk: {result['chunk_index']}")
    print(f"Text: {result['text'][:300]}")
