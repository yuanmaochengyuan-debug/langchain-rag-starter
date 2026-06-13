# 🔍 LangChain RAG Starter

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-1C3C3C?logo=langchain)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5.3-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A clean, production-ready **Retrieval-Augmented Generation (RAG)** pipeline starter template built with LangChain, ChromaDB, FastAPI, and Streamlit — powered by Google Gemini AI.

Upload your documents, ask questions, and get AI-generated answers grounded in your own data.

---

## ✨ Features

| Feature             | Details                                    |
| ------------------- | ------------------------------------------ |
| 🤖 LLM              | Google Gemini 2.5 Flash Lite               |
| 🗄️ Vector Store     | ChromaDB (persistent local storage)        |
| 📄 Document Support | PDF and TXT files                          |
| ⚡ API              | FastAPI REST API with auto Swagger docs    |
| 🖥️ UI               | Streamlit interactive demo interface       |
| 🔐 Config           | Environment-based configuration via `.env` |
| 🧩 Modular          | Clean service-based architecture           |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Streamlit UI ──► FastAPI /api/v1/query
                        │
                        ▼
                  LangChain RAG Chain
                  ┌─────────────────┐
                  │  Retriever      │◄── ChromaDB Vector Store
                  │  Gemini LLM     │◄── Google AI
                  │  Prompt Template│
                  └─────────────────┘
                        │
                        ▼
                  Answer + Sources
```

---

## 📁 Project Structure

```
langchain-rag-starter/
├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI endpoints
│   ├── core/
│   │   ├── config.py          # Settings via .env
│   │   └── prompts.py         # Prompt templates
│   └── services/
│       ├── embedder.py        # Gemini embedding logic
│       ├── vectorstore.py     # ChromaDB setup
│       └── rag_chain.py       # LangChain RAG chain
├── streamlit_ui/
│   └── app.py                 # Streamlit demo UI
├── data/
│   └── sample_docs/           # Drop your PDFs/TXTs here
├── tests/
│   └── test_rag.py
├── main.py                    # FastAPI entry point
├── ingest.py                  # Document ingestion script
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/pubudini-rathnayake/langchain-rag-starter.git
cd langchain-rag-starter
```

### 2. Create and activate a virtual environment

```bash
py -3.11 -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_key_here
```

Get your free key at: **https://aistudio.google.com/apikey**

### 5. Add your documents

Drop any `.pdf` or `.txt` files into the `data/sample_docs/` folder.

### 6. Ingest documents into ChromaDB

```bash
python ingest.py
```

### 7. Start the FastAPI server

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive API explorer.

### 8. Start the Streamlit UI (new terminal)

```bash
streamlit run streamlit_ui/app.py
```

Visit **http://localhost:8501**

---

## 🔌 API Usage

### Query endpoint

```http
POST /api/v1/query
Content-Type: application/json

{
  "question": "What is this document about?"
}
```

### Response

```json
{
  "answer": "The document is about...",
  "sources": ["data/sample_docs/my_file.pdf"]
}
```

---

## ⚙️ Configuration

All settings are managed via the `.env` file:

| Variable          | Default          | Description                       |
| ----------------- | ---------------- | --------------------------------- |
| `GEMINI_API_KEY`  | —                | Your Google Gemini API key        |
| `CHROMA_DB_PATH`  | `./chroma_db`    | Where ChromaDB stores vectors     |
| `COLLECTION_NAME` | `rag_collection` | ChromaDB collection name          |
| `CHUNK_SIZE`      | `500`            | Document chunk size in characters |
| `CHUNK_OVERLAP`   | `50`             | Overlap between chunks            |

---

## 🗺️ Roadmap

- [ ] JWT authentication for the API
- [ ] Multi-collection support
- [ ] File upload endpoint (no manual ingestion needed)
- [ ] Docker support
- [ ] Deploy to cloud (Railway / Render)

---

## 🛠️ Built With

- [LangChain](https://www.langchain.com/) — LLM orchestration framework
- [Google Gemini](https://aistudio.google.com/) — Large language model
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [Streamlit](https://streamlit.io/) — Demo UI framework

---

## 👩‍💻 Author

**Pubudini Rathnayake**

- GitHub: [@pubudini-rathnayake](https://github.com/pubudini-rathnayake)
- LinkedIn: [linkedin.com/in/pubudini-rathnayake](https://linkedin.com/in/pubudini-rathnayake)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

⭐ If you found this useful, please consider giving it a star!
