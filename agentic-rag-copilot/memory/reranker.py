def rerank(results, feedback_db):
    # naive: prioritize previously good chunks
    boosted = []

    for r in results:
        score = 0
        for f in feedback_db:
            if r in f["answer"] and f["rating"] > 3:
                score += 1
        boosted.append((r, score))

    boosted.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in boosted]