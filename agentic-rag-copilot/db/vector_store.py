import faiss
import numpy as np

dimension = 384  # IMPORTANT: matches sentence-transformer

index = faiss.IndexFlatL2(dimension)
documents = []


def add_embeddings(embeddings, texts):
    global documents
    index.add(np.array(embeddings).astype('float32'))
    documents.extend(texts)


def search(query_embedding, k=5):
    if len(documents) == 0:
        return ["No documents available. Please ingest data first."]

    D, I = index.search(np.array([query_embedding]).astype('float32'), k)

    results = []
    for i in I[0]:
        if i < len(documents):
            results.append(documents[i])

    return results