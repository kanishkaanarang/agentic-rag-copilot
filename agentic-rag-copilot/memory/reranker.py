# memory/reranker.py

def keyword_score(query, text):
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    return len(query_words & text_words)


def feedback_score(chunk, feedback_db):
    score = 0
    for f in feedback_db:
        answer = f.get("answer", "")
        rating = f.get("rating", 0)

        if chunk in answer:
            if rating >= 4:
                score += 2
            elif rating == 3:
                score += 1

    return score


def rerank(query, results, feedback_db):
    """
    results: [(idx, chunk)]
    """

    scored = []

    for item in results:
        # 🔥 SAFETY FIX (prevents unpacking errors)
        if not isinstance(item, tuple) or len(item) < 2:
            continue

        idx, chunk = item[0], item[1]

        k_score = keyword_score(query, chunk)
        f_score = feedback_score(chunk, feedback_db)

        total_score = k_score + f_score

        scored.append((idx, chunk, total_score))

    scored.sort(key=lambda x: x[2], reverse=True)

    return [(idx, chunk) for idx, chunk, _ in scored]