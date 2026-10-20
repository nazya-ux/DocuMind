
import os

from dotenv import load_dotenv
from google import genai

from src.embeddings import embed_texts

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

texts = [
    "Large language models can hallucinate.",
    "Retrieval helps language models use external information.",
    "A database stores structured information.",
]

vectors = embed_texts(client, texts)

print("Input texts:", len(texts))
print("Embedding vectors:", len(vectors))
print("Dimensions per vector:", [len(vector) for vector in vectors])

assert len(texts) == len(vectors), "Embedding count does not match text count!"
print("Embedding test passed!")
