from sentence_transformers import SentenceTransformer
from db.vector_store import search, documents
from memory.reranker import rerank

# optional: import feedback DB
try:
    from memory.feedback import feedback_db
except:
    feedback_db = []

model = SentenceTransformer("all-MiniLM-L6-v2")


def keyword_score(query, text):
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    return len(query_words & text_words)


def retrieve(query, k=5):
    if len(documents) == 0:
        return []

    # 🔹 Step 1: embedding search
    query_embedding = model.encode(query).tolist()
    vector_results = search(query_embedding, k=10)

    # 🔹 Step 2: hybrid scoring (keyword boost)
    hybrid_scored = []

    for item in vector_results:
        # 🔥 SAFETY FIX
        if not isinstance(item, tuple) or len(item) < 2:
            continue

        idx, chunk = item[0], item[1]

        k_score = keyword_score(query, chunk)
        hybrid_scored.append((idx, chunk, k_score))

    # sort by keyword relevance
    hybrid_scored.sort(key=lambda x: x[2], reverse=True)

    # 🔥 IMPORTANT: remove score before rerank
    results = [(idx, chunk) for idx, chunk, _ in hybrid_scored]

    # 🔹 Step 3: rerank (feedback + keyword)
    results = rerank(query, results, feedback_db)

    # 🔹 Step 4: return top k
    return results[:k]