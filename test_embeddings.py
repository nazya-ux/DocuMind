import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

client = genai.Client(api_key=api_key)

text = "Large language models can produce factually incorrect answers."

response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=text,
)

embedding = response.embeddings[0].values

print("Original text:", text)
print("Embedding dimensions:", len(embedding))
print("First five values:", embedding[:5])