feedback_db = []

def store_feedback(query, answer, rating):
    feedback_db.append({
        "query": query,
        "answer": answer,
        "rating": rating
    })