import ollama

MODEL = "llama3"


def ask_llm(messages):

    stream = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True
    )

    return stream