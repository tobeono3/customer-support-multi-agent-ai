from app.rag import build_vector_store
store, added = build_vector_store()
print(f"Policy index ready. Added {added} chunks.")
