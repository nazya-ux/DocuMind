
import hashlib
from pathlib import Path

import streamlit as st

from src.indexer import index_pdf
from src.retriever import retrieve
from src.generator import generate_answer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="DocuMind",
    page_icon="🧠",
    layout="wide",
)

UPLOAD_FOLDER = Path("data/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = {}

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 DocuMind")
st.caption("Your personal AI notebook for learning from documents.")

st.markdown(
    "Upload PDFs, ask questions, and explore answers grounded "
    "in your documents."
)


# --------------------------------------------------
# PDF upload and indexing
# --------------------------------------------------

st.sidebar.header("📚 Your Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
)

if st.sidebar.button("Index uploaded PDFs", use_container_width=True):
    if not uploaded_files:
        st.sidebar.warning("Please upload at least one PDF first.")
    else:
        for uploaded_file in uploaded_files:
            original_name = Path(uploaded_file.name).name
            file_bytes = uploaded_file.getvalue()

            file_hash = hashlib.sha256(file_bytes).hexdigest()

            # Keep the original filename alongside the content hash.
            saved_path = UPLOAD_FOLDER / f"{file_hash}_{original_name}"

            # Save the PDF only if it does not already exist.
            if not saved_path.exists():
                saved_path.write_bytes(file_bytes)

            if st.session_state.indexed_files.get(file_hash):
                st.sidebar.info(
                    f"Already indexed: {original_name}"
                )
                continue

            try:
                with st.spinner(f"Indexing {original_name}..."):
                    index_pdf(str(saved_path))

                st.session_state.indexed_files[file_hash] = original_name

                st.sidebar.success(
                    f"Indexed: {original_name}"
                )

            except Exception as error:
                st.sidebar.error(
                    f"Could not index {original_name}: {error}"
                )


# --------------------------------------------------
# Indexed documents
# --------------------------------------------------

if st.session_state.indexed_files:
    with st.sidebar.expander("Indexed this session", expanded=True):
        for filename in st.session_state.indexed_files.values():
            st.write(f"📄 {filename}")

st.sidebar.caption(
    "Embeddings run locally. Answer generation uses your configured Gemini API."
)


# --------------------------------------------------
# Chat history
# --------------------------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View retrieved sources"):
                for i, source in enumerate(message["sources"], start=1):
                    st.markdown(
                        f"**Source {i}:** {source['source']} "
                        f"(chunk {source['chunk_index']})"
                    )
                    st.write(source["text"])


# --------------------------------------------------
# Ask DocuMind
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about your documents..."
)

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching your documents..."):
                passages = retrieve(question, top_k=5)

            if not passages:
                answer = (
                    "I couldn't find relevant passages in your documents."
                )
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )
            else:
                with st.spinner("Generating an answer..."):
                    answer = generate_answer(question, passages)

                st.markdown(answer)

                with st.expander("View retrieved sources"):
                    for i, source in enumerate(passages, start=1):
                        st.markdown(
                            f"**Source {i}:** {source['source']} "
                            f"(chunk {source['chunk_index']})"
                        )
                        st.write(source["text"])

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": passages,
                    }
                )

        except Exception as error:
            error_message = f"Something went wrong: {error}"
            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )
