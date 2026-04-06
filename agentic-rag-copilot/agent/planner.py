from ollama import chat

def rewrite_query(query):
    prompt = f"""
You are an AI assistant helping with technical queries.

Rewrite the query to be specific to AI / machine learning context.

Query: {query}

Rewritten query:
"""

    response = chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def plan(query):
    improved_query = rewrite_query(query)
    return [improved_query]