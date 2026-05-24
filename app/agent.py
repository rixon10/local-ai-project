from tools import (
    calculator,
    read_file
)

from rag import search_pdf


def decide_tool(user_input):

    user_input = user_input.lower()

    # Calculator
    math_symbols = ["+", "-", "*", "/"]

    if any(symbol in user_input for symbol in math_symbols):

        return "calculator"

    # File Reader
    if ".py" in user_input or ".txt" in user_input:

        return "file_reader"

    # PDF Questions
    pdf_keywords = [
    "pdf",
    "document",
    "paper",
    "neural",
    "machine learning",
    "deep learning",
    "ai"
]

    if any(keyword in user_input for keyword in pdf_keywords):

        return "pdf_search"

    return "chat"


def run_agent(user_input):

    tool = decide_tool(user_input)

    # -------------------------
    # CALCULATOR
    # -------------------------

    if tool == "calculator":

        try:

            result = calculator(user_input)

            return f"Calculation Result: {result}"

        except Exception:

            return "Could not calculate."

    # -------------------------
    # FILE READER
    # -------------------------

    elif tool == "file_reader":

        words = user_input.split()

        file_path = None

        for word in words:

            if "." in word:

                file_path = word

                break

        if not file_path:

            return "No valid file found."

        content, error = read_file(file_path)

        if error:

            return error

        return f"""
        FILE CONTENT:

        {content[:4000]}
        """

    # -------------------------
    # PDF SEARCH
    # -------------------------

    elif tool == "pdf_search":

        docs = search_pdf(user_input)

        context = "\n".join(docs)

        return f"""
        PDF CONTEXT:

        {context}
        """

    # -------------------------
    # NORMAL CHAT
    # -------------------------

    return None