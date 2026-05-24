import json

from json_repair import repair_json

from llm import ask_llm
from prompts import SYSTEM_PROMPT

from tools import (
    calculator,
    read_file
)

from rag import search_pdf

from tool_registry import TOOLS


def get_tool_decision(user_input):

    tool_prompt = f"""
    You are an AI agent.

    Decide which tool should be used.

    Available tools:

    {json.dumps(TOOLS, indent=2)}

    Respond ONLY in valid JSON format.

    Example:
    {{
        "tool": "calculator",
        "input": "55 * 12"
    }}

    USER INPUT:
    {user_input}
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": tool_prompt
        }
    ]

    stream = ask_llm(messages)

    response_text = ""

    for chunk in stream:

        response_text += chunk["message"]["content"]

    try:

        repaired = repair_json(response_text)

        parsed = json.loads(repaired)

        return parsed

    except Exception:

        return {
            "tool": "chat",
            "input": user_input
        }


def execute_tool(tool_name, tool_input):

    # -------------------------
    # CALCULATOR
    # -------------------------

    if tool_name == "calculator":

        result = calculator(tool_input)

        return f"Calculation Result: {result}"

    # -------------------------
    # FILE READER
    # -------------------------

    elif tool_name == "file_reader":

        content, error = read_file(tool_input)

        if error:

            return error

        return f"""
        FILE CONTENT:

        {content[:4000]}
        """

    # -------------------------
    # PDF SEARCH
    # -------------------------

    elif tool_name == "pdf_search":

        docs = search_pdf(tool_input)

        context = "\n".join(docs)

        return f"""
        PDF CONTEXT:

        {context}
        """

    return None


def run_agent(user_input):

    decision = get_tool_decision(user_input)
    tool_name = decision.get("tool", "chat")

    tool_input = decision.get("input", user_input)

    # Fallback safety
    if not tool_input:

        tool_input = user_input

    # tool_name = decision.get("tool")

    # tool_input = decision.get("input")

    if tool_name == "chat":

        return None

    tool_result = execute_tool(
        tool_name,
        tool_input
    )

    final_prompt = f"""
    User Question:
    {user_input}

    Tool Used:
    {tool_name}

    Tool Result:
    {tool_result}

    Generate a helpful response.
    """

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": final_prompt
        }
    ]