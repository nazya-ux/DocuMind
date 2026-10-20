
from src.retriever import retrieve
from src.generator import generate_answer


question = input("Ask DocuMind a question: ").strip()

if not question:
    print("Please enter a question.")
else:
    passages = retrieve(question, top_k=5)

    if not passages:
        print("No relevant passages were found.")
    else:
        answer = generate_answer(question, passages)

        print("\n--- DOCUMIND'S ANSWER ---")
        print(answer)

        print("\n--- RETRIEVED SOURCES ---")

        for i, passage in enumerate(passages, start=1):
            print(
                f"{i}. {passage['source']} "
                f"(chunk {passage['chunk_index']})"
            )
