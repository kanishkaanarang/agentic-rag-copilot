from rag.retrieve import retrieve
from rag.generate import generate_answer


def execute(query, steps):
    # 🔹 Step 1: Retrieve
    search_query = steps[0] if steps else query
    retrieved = retrieve(search_query)

    # 🔹 Step 2: Filter bad chunks FIRST
    cleaned = []
    for _, chunk in retrieved:
        text = chunk.strip()

        # remove very short chunks
        if len(text) < 50:
            continue

        # remove numeric-heavy chunks (tables, metrics)
        digit_ratio = sum(c.isdigit() for c in text) / len(text)
        if digit_ratio > 0.3:
            continue

        cleaned.append(text)
    # 🔹 Step 3: Keep top 3 clean chunks
    cleaned = cleaned[:3]

    # 🔹 Step 4: Build context from CLEAN data
    context = "\n".join(cleaned)

    # 🔹 Step 5: Generate answer
    answer = generate_answer(query, context)

    # 🔹 Step 6: Format sources
    def clean_chunk(text):
        text = " ".join(text.split())

        # remove numeric-heavy lines
        words = text.split()
        words = [w for w in words if not any(char.isdigit() for char in w)]

        text = " ".join(words)

        # cut at first sentence
        if "." in text:
            text = text.split(".")[0] + "."

        return text[:150]

    sources = "\n".join(
        [f"- {clean_chunk(chunk)}" for chunk in cleaned]
    )

    # 🔹 Step 7: Final output and get every source in next line
    final_answer = f"""{answer}
    \n📚 **Sources**
    {sources}
    """
    return final_answer