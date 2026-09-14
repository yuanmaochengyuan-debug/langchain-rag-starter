"""
ingest.py — Incrementally load new or changed documents into ChromaDB.

Usage:
    python ingest.py

Supported files:
    .pdf
    .txt
"""

import hashlib
import json
from pathlib import Path

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from app.core.config import settings
from app.services.vectorstore import get_vectorstore


load_dotenv()

DOCS_PATH = Path("./data/sample_docs")
MANIFEST_PATH = Path(settings.chroma_db_path) / "ingestion_manifest.json"


def calculate_sha256(filepath: Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with filepath.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def load_manifest() -> dict:
    """Load previously ingested file hashes."""
    if not MANIFEST_PATH.exists():
        return {}

    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_manifest(manifest: dict) -> None:
    """Save file hashes used for incremental ingestion."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MANIFEST_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=2,
        )


def load_file(filepath: Path):
    """Load a PDF or TXT file."""
    suffix = filepath.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(filepath))

    elif suffix == ".txt":
        loader = TextLoader(
            str(filepath),
            encoding="utf-8",
        )

    else:
        return []

    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = filepath.name

    return documents


def ingest():
    print("Scanning documents...")

    DOCS_PATH.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()
    vectorstore = get_vectorstore()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    imported_files = 0
    skipped_files = 0
    error_files = 0

    for filepath in sorted(DOCS_PATH.iterdir()):
        if filepath.suffix.lower() not in {".pdf", ".txt"}:
            continue

        filename = filepath.name
        file_hash = calculate_sha256(filepath)
        previous = manifest.get(filename)

        # File contents have not changed
        if previous and previous.get("sha256") == file_hash:
            print(f"[SKIP] {filename} — unchanged")
            skipped_files += 1
            continue

        if previous:
            print(f"[UPDATE] {filename} — file changed")
        else:
            print(f"[NEW] {filename}")

        new_ids = []

        try:
            # First make sure the new file can be loaded successfully
            documents = load_file(filepath)

            chunks = splitter.split_documents(documents)

            if not chunks:
                print(f"[SKIP] {filename} — no content")
                skipped_files += 1
                continue

            for chunk in chunks:
                chunk.metadata["file_sha256"] = file_hash

            # Add the new version first
            new_ids = vectorstore.add_documents(chunks)

            # Only after successful insertion, remove the previous version
            if previous:
                old_hash = previous.get("sha256")

                if old_hash:
                    vectorstore.delete(
                        where={"file_sha256": old_hash}
                    )

            # Update local ingestion record
            manifest[filename] = {
                "sha256": file_hash,
            }

            imported_files += 1

            print(
                f"       {len(documents)} page(s), "
                f"{len(chunks)} chunk(s)"
            )

        except Exception as e:
            # Roll back newly inserted chunks if later processing fails
            if new_ids:
                try:
                    vectorstore.delete(ids=new_ids)
                except Exception:
                    pass

            print(f"[ERROR] {filename} — {e}")
            error_files += 1

    save_manifest(manifest)

    print()
    print("Ingestion complete.")
    print(f"Imported/updated: {imported_files}")
    print(f"Skipped: {skipped_files}")
    print(f"Errors: {error_files}")


if __name__ == "__main__":
    ingest()