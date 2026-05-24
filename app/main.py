from llm import ask_llm, MODEL
from memory import load_memory, save_memory
from rag import ingest_pdf, search_pdf
from agent import run_agent
from prompts import SYSTEM_PROMPT
from tools import (
    calculator,
    read_file,
    analyze_folder
)
from commands import show_help, clear_screen

from rich.console import Console
from rich.panel import Panel

console = Console()

messages = load_memory()

# Add system prompt if memory empty
if not messages:

    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })


def show_banner():

    console.print(
        Panel.fit(
            "[bold green]Local AI Assistant[/bold green]\n"
            "Type [cyan]/help[/cyan] for commands",
            title="AI Assistant",
            border_style="green"
        )
    )


show_banner()

while True:

    user_input = console.input(
        "\n[bold cyan]You:[/bold cyan] "
    )

    # -------------------------
    # COMMANDS
    # -------------------------

    if user_input == "/exit":

        console.print(
            "\n[bold red]Goodbye![/bold red]\n"
        )

        break

    elif user_input == "/help":

        show_help()

        continue

    elif user_input == "/clear":

        clear_screen()

        show_banner()

        continue

    elif user_input == "/model":

        console.print(
            f"\n[bold yellow]Current Model:[/bold yellow] {MODEL}"
        )

        continue

    elif user_input == "/history":

        console.print(
            Panel.fit(
                str(messages),
                title="Conversation History",
                border_style="blue"
            )
        )

        continue

    elif user_input == "/reset":

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        save_memory(messages)

        console.print(
            "\n[bold green]Memory reset successful.[/bold green]"
        )

        continue

    # -------------------------
    # CALCULATOR TOOL
    # -------------------------

    if user_input.lower().startswith("calc"):

        expression = user_input[4:].strip()

        result = calculator(expression)

        console.print(
            Panel.fit(
                str(result),
                title="Calculator",
                border_style="yellow"
            )
        )

        continue

    # -------------------------
    # FILE READER TOOL
    # -------------------------

    elif user_input.startswith("read "):

        file_path = user_input.replace("read ", "").strip()

        content, error = read_file(file_path)

        if error:

            console.print(
                f"\n[bold red]Error:[/bold red] {error}"
            )

            continue

        console.print(
            f"\n[bold yellow]Reading:[/bold yellow] {file_path}\n"
        )

        # Send file content to LLM
        file_prompt = f"""
        Analyze the following file.

        File Name:
        {file_path}

        File Content:
        {content}

        Explain what this file does.
        """
        temp_messages = agent_messages
        # temp_messages = [
        #     {
        #         "role": "system",
        #         "content": SYSTEM_PROMPT
        #     },
        #     {
        #         "role": "user",
        #         "content": file_prompt
        #     }
        # ]

        console.print(
            "[bold green]AI:[/bold green] ",
            end=""
        )

        stream = ask_llm(temp_messages)

        full_response = ""

        for chunk in stream:

            text = chunk["message"]["content"]

            full_response += text

            console.print(text, end="")

        print("\n")

        continue

    # -------------------------
    # FOLDER ANALYZER
    # -------------------------

    elif user_input.startswith("analyze "):

        folder_path = user_input.replace(
            "analyze ",
            ""
        ).strip()

        console.print(
            f"\n[bold yellow]Analyzing Folder:[/bold yellow] {folder_path}\n"
        )

        project_content, error = analyze_folder(folder_path)

        if error:

            console.print(
                f"\n[bold red]Error:[/bold red] {error}"
            )

            continue

        analysis_prompt = f"""
        Analyze this software project.

        Explain:

        1. Project purpose
        2. Folder structure
        3. Important components
        4. Technologies used
        5. Possible improvements

        PROJECT CONTENT:

        {project_content}
        """

        temp_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ]

        console.print(
            "[bold green]AI:[/bold green] ",
            end=""
        )

        stream = ask_llm(temp_messages)

        full_response = ""

        for chunk in stream:

            text = chunk["message"]["content"]

            full_response += text

            console.print(text, end="")

        print("\n")

        continue

    # -------------------------
    # INGEST PDF
    # -------------------------

    elif user_input.startswith("/ingest"):

        pdf_path = user_input.replace(
            "/ingest",
            ""
        ).strip()

        console.print(
            f"\n[bold yellow]Ingesting PDF:[/bold yellow] {pdf_path}"
        )

        try:

            chunks = ingest_pdf(pdf_path)

            console.print(
                f"\n[bold green]Success![/bold green] Added {chunks} chunks.\n"
            )

        except Exception as e:

            console.print(
                f"\n[bold red]Error:[/bold red] {str(e)}"
            )

        continue


    # -------------------------
    # ASK PDF
    # -------------------------

    elif user_input.startswith("/askpdf"):

        question = user_input.replace(
            "/askpdf",
            ""
        ).strip()

        docs = search_pdf(question)

        context = "\n".join(docs)

        pdf_prompt = f"""
        Answer the question using ONLY the provided context.

        CONTEXT:
        {context}

        QUESTION:
        {question}
        """

        temp_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": pdf_prompt
            }
        ]

        console.print(
            "\n[bold green]AI:[/bold green] ",
            end=""
        )

        stream = ask_llm(temp_messages)

        for chunk in stream:

            text = chunk["message"]["content"]

            console.print(text, end="")

        print("\n")

        continue

    # # -------------------------
    # # AI CHAT
    # # -------------------------

    # messages.append({
    #     "role": "user",
    #     "content": user_input
    # })

    # try:

    #     console.print(
    #         "\n[bold green]AI:[/bold green] ",
    #         end=""
    #     )

    #     stream = ask_llm(messages)

    #     full_response = ""

    #     for chunk in stream:

    #         content = chunk["message"]["content"]

    #         full_response += content

    #         console.print(content, end="")

    #     print("\n")

    #     messages.append({
    #         "role": "assistant",
    #         "content": full_response
    #     })

    #     save_memory(messages)

    # except Exception as e:

    #     console.print(
    #         f"\n[bold red]Error:[/bold red] {str(e)}"
    #     )





    # -------------------------
    # AI AGENT
    # -------------------------

    # agent_response = run_agent(user_input)
    agent_messages = run_agent(user_input)

    # if agent_response:
    if agent_messages:

        temp_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
                User Question:
                {user_input}

                Tool Result:
                {agent_messages}

                Generate a helpful response.
                """
            }
        ]

    else:

        messages.append({
            "role": "user",
            "content": user_input
        })

        temp_messages = messages

    try:

        console.print(
            "\n[bold green]AI:[/bold green] ",
            end=""
        )

        stream = ask_llm(temp_messages)

        full_response = ""

        for chunk in stream:

            text = chunk["message"]["content"]

            full_response += text

            console.print(text, end="")

        print("\n")

        messages.append({
            "role": "assistant",
            "content": full_response
        })

        save_memory(messages)

    except Exception as e:

        console.print(
            f"\n[bold red]Error:[/bold red] {str(e)}"
        )