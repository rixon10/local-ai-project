import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_help():

    help_text = """
[bold cyan]/help[/bold cyan]     → Show available commands
[bold cyan]/clear[/bold cyan]    → Clear terminal
[bold cyan]/reset[/bold cyan]    → Reset chat memory
[bold cyan]/history[/bold cyan]  → Show conversation history
[bold cyan]/model[/bold cyan]    → Show current model
[bold cyan]/exit[/bold cyan]     → Exit assistant
[bold cyan]/ingest[/bold cyan]   → Load PDF into memory
[bold cyan]/askpdf[/bold cyan]   → Ask questions from PDFs
"""

    console.print(
        Panel.fit(
            help_text,
            title="Commands",
            border_style="green"
        )
    )


def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")