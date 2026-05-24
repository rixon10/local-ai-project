from pathlib import Path
from pypdf import PdfReader

import chromadb
from sentence_transformers import SentenceTransformer

# Embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ChromaDB client
client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_collection"
)


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        text += page.extract_text()

    return text


def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


def ingest_pdf(pdf_path):

    text = extract_text_from_pdf(pdf_path)

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk
        ).tolist()

        collection.add(
            ids=[f"{pdf_path}_{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    return len(chunks)


def search_pdf(query, top_k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]