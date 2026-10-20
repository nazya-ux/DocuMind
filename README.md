# 📚 DocuMind

**A personal AI learning notebook.** Turn PDFs into searchable knowledge, ask questions in natural language, and get answers grounded in your documents.

DocuMind is a privacy-conscious, PDF-based AI assistant built with Retrieval-Augmented Generation (RAG). It combines local semantic search with an LLM to help you understand and explore learning materials without manually searching through pages.

## ✨ Features

- **📄 PDF ingestion:** Extract text from PDF documents.
- **✂️ Intelligent chunking:** Split documents into smaller passages for retrieval.
- **🧠 Local embeddings:** Generate semantic embeddings using Sentence Transformers.
- **🔎 Semantic search:** Retrieve relevant passages using ChromaDB.
- **💬 AI-powered Q&A:** Ask questions about your documents and receive context-grounded answers.
- **📌 Source passages:** Inspect retrieved passages to understand where answers come from.
- **🔒 Local document processing:** Keep document storage, embeddings, and vector search on your machine. Answer generation uses the configured Gemini API.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| PyPDF | PDF text extraction |
| Sentence Transformers | Local text embeddings |
| ChromaDB | Persistent vector storage and similarity search |
| Google Gemini API | Answer generation |
| python-dotenv | Environment variable configuration |

## 🧠 How It Works

DocuMind uses a Retrieval-Augmented Generation pipeline:

1. **Upload:** Provide a PDF document.
2. **Extract:** Extract readable text from the PDF.
3. **Chunk:** Divide the text into smaller passages.
4. **Embed:** Convert passages into numerical vectors using a local embedding model.
5. **Index:** Store vectors, passages, and metadata in ChromaDB.
6. **Retrieve:** Convert your question into an embedding and find relevant passages.
7. **Generate:** Send the question and retrieved context to Gemini to generate an answer.
8. **Inspect:** Review the answer and retrieved source passages.

```text
PDF Documents
      |
      v
  Text Extraction
      |
      v
  Text Chunking
      |
      v
 Local Embeddings
      |
      v
    ChromaDB
      |
      v
 User Question
      |
      v
 Semantic Retrieval
      |
      v
 Relevant Context + Question
      |
      v
   Gemini API
      |
      v
 Answer + Source Passages
```

## 📂 Project Structure

```text
DocuMind/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── src/
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── indexer.py
│   ├── retriever.py
│   └── generator.py
├── data/
│   ├── documents/
│   ├── uploads/
│   └── vectorstore/
└── test_pipeline.py
```

The `.env` file and local data directories should remain private and are excluded from version control.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or newer, subject to compatibility with the installed dependencies
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/nazya-ux/DocuMind.git
cd DocuMind
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly using `.\.venv\Scripts\python.exe`.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key. **Never commit your `.env` file or expose your API key publicly.**

### 5. Run DocuMind

```powershell
streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open it in your browser to use the application.

The first embedding-model load may take longer because the model needs to be downloaded.

## 🔐 Privacy and Data Handling

- PDF text embeddings are generated locally using Sentence Transformers.
- ChromaDB stores the local vector index on your machine.
- Answer generation sends the question and retrieved document passages to the configured Gemini API.
- API credentials are stored in environment variables rather than source code.

**Important:** Do not upload confidential or sensitive documents unless you are comfortable sending the retrieved passages to the configured AI provider.

## 🧪 Testing

The repository includes scripts for testing parts of the embedding and retrieval pipeline.

Run an individual test script from the project root, for example:

```powershell
python test_embeddings.py
```

Some tests may require the embedding model to be downloaded and the relevant dependencies installed.

## 🗺️ Roadmap

- [ ] Improve citation accuracy and connect answers to exact document passages.
- [ ] Add answer-grounding and retrieval-quality evaluation.
- [ ] Save useful answers as organized learning notes.
- [ ] Add document collections and topic-based organization.
- [ ] Support exporting saved notes.
- [ ] Improve document management and duplicate detection.

## 🎯 Project Goal

DocuMind aims to make learning from long documents less tedious by turning static PDFs into an interactive, searchable knowledge base.

Instead of repeatedly searching through pages or rewriting notes manually, learners can ask questions, explore relevant passages, and build toward a personal knowledge library.

## 👩‍💻 Author

**Nazia Ahmed**

GitHub: [@nazya-ux](https://github.com/nazya-ux)

---

*Built with Python, local semantic search, and Retrieval-Augmented Generation.*
