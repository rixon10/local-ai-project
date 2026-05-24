import json
from pathlib import Path

MEMORY_FILE = Path("data/chat_history.json")


def load_memory():

    # Create file if missing
    if not MEMORY_FILE.exists():

        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(MEMORY_FILE, "w") as file:
            json.dump([], file)

        return []

    try:

        with open(MEMORY_FILE, "r") as file:

            content = file.read().strip()

            # Empty file check
            if not content:
                return []

            return json.loads(content)

    except json.JSONDecodeError:

        print("Memory file corrupted. Resetting memory.")

        return []


def save_memory(messages):

    with open(MEMORY_FILE, "w") as file:
        json.dump(messages, file, indent=4)