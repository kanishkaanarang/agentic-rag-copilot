import requests

def generate_answer(query, context):
    prompt = f"""
You are a helpful assistant.

Explain clearly and simply.

RULES:
- 1–3 sentences only
- No technical jargon unless needed
- No repetition
- No mention of "context"

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
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