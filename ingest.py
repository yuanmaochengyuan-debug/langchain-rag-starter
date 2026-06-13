"""
ingest.py — Run this script to load documents into ChromaDB.
Usage: python ingest.py
Drop your PDFs or .txt files into data/sample_docs/ first.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.vectorstore import get_vectorstore
from app.core.config import settings

load_dotenv()

DOCS_PATH = "./data/sample_docs"

def load_documents():
    docs = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        elif filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
        else:
            continue
        docs.extend(loader.load())
    return docs

def ingest():
    print("Loading documents...")
    docs = load_documents()
    print(f"  Found {len(docs)} page(s)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(docs)
    print(f"  Split into {len(chunks)} chunks")

    print("Storing in ChromaDB...")
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)
    print("Done! Documents ingested successfully.")

if __name__ == "__main__":
    ingest()