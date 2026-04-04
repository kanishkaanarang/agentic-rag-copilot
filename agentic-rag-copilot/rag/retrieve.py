from sentence_transformers import SentenceTransformer
from db.vector_store import search
from db.vector_store import documents

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, k=5):
    if len(documents) == 0:
        return ["No documents loaded"]

    query_embedding = model.encode(query).tolist()
    results = search(query_embedding, k)
    return results