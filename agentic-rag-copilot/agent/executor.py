from rag.retrieve import retrieve
from rag.generate import generate_answer

def execute(query, steps):
    answers = []

    for step in steps:
        context_chunks = retrieve(step)

        context = "\n".join(context_chunks)

        ans = generate_answer(step, context)
        answers.append(ans)

    final_answer = "\n".join(answers)
    return final_answer