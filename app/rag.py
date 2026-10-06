from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import CHROMA_DIR, POLICY_DIR, EMBEDDING_MODEL

COLLECTION = "customer_support_policies"

def build_vector_store():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    store = Chroma(collection_name=COLLECTION, embedding_function=embeddings, persist_directory=str(CHROMA_DIR))
    pdfs = list(Path(POLICY_DIR).glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError(f"No PDF files found in {POLICY_DIR}")
    existing = store.get(include=[])
    existing_sources = set()
    for meta in store.get(include=["metadatas"]).get("metadatas", []):
        if meta and meta.get("source"):
            existing_sources.add(meta["source"])
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    added = 0
    for pdf in pdfs:
        source = pdf.name
        if source in existing_sources:
            continue
        docs = PyPDFLoader(str(pdf)).load()
        chunks = splitter.split_documents(docs)
        for d in chunks:
            d.metadata["source"] = source
        if chunks:
            store.add_documents(chunks)
            added += len(chunks)
    return store, added

def get_store():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(collection_name=COLLECTION, embedding_function=embeddings, persist_directory=str(CHROMA_DIR))

def retrieve_policy(query: str, k: int = 5):
    store = get_store()
    docs = store.similarity_search(query, k=k)
    return [{"content": d.page_content, "source": d.metadata.get("source", "unknown"), "page": d.metadata.get("page", "unknown")} for d in docs]
