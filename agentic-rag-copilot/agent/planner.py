import requests

def plan(query):
    prompt = f"""
Break this question into smaller steps:

{query}

Return each step on a new line.
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    text = res.json()["response"]

    steps = [s.strip() for s in text.split("\n") if s.strip()]
    return steps