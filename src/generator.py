
import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

client = genai.Client(api_key=api_key)


def generate_answer(question: str, passages: list[dict]) -> str:
    """Generate an answer grounded in retrieved document passages."""

    if not passages:
        return "I couldn't find relevant information in your documents."

    context_parts = []

    for i, passage in enumerate(passages, start=1):
        context_parts.append(
            f"[Source {i}: {passage['source']}, "
            f"chunk {passage['chunk_index']}]\n"
            f"{passage['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are DocuMind, a document question-answering assistant.

Answer the user's question using only the provided context.

Rules:
- Do not invent facts that are absent from the context.
- If the context does not contain enough information, say so.
- Explain the answer clearly in simple language.
- Cite supporting passages using labels such as [Source 1].
- If sources disagree, mention the disagreement.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = client.models.generate_content(
           model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        return response.text or "The model returned an empty response."

    except errors.APIError as error:
        print(f"Gemini API error: {error.code} - {error.message}")

        if error.code == 503:
            return (
                "DocuMind's AI service is temporarily busy. "
                "Your documents are still indexed. Please try again shortly."
            )

        if error.code == 429:
            return (
                "DocuMind has reached the API rate limit. "
                "Please wait a little and try again."
            )

        return (
            "DocuMind couldn't generate an answer because of an API error. "
            "Please check the terminal for details and try again."
        )

    except Exception as error:
        print(f"Unexpected generation error: {error}")
        return (
            "An unexpected error occurred while generating the answer. "
            "Please check the terminal for details."
        )
