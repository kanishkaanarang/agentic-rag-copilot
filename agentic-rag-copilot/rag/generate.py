import requests

def generate_answer(query, context):
    prompt = f"""
You are a helpful research assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return res.json()["response"]