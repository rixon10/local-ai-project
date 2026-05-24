from pathlib import Path


def calculator(expression):

    try:

        result = eval(expression)

        return result

    except Exception:

        return "Invalid mathematical expression."


def read_file(file_path):

    try:

        path = Path(file_path)

        if not path.exists():

            return None, "File does not exist."

        with open(path, "r", encoding="utf-8") as file:

            content = file.read()

        return content, None

    except Exception as e:

        return None, str(e)


def analyze_folder(folder_path):

    try:

        path = Path(folder_path)

        if not path.exists():

            return None, "Folder does not exist."

        project_content = ""

        # File types to include
        allowed_extensions = [
            ".py",
            ".md",
            ".txt",
            ".json"
        ]

        for file in path.rglob("*"):

            # Skip directories
            if file.is_dir():
                continue

            # Skip virtual environment
            if ".venv" in str(file):
                continue

            # Skip cache folders
            if "__pycache__" in str(file):
                continue

            # Only include allowed files
            if file.suffix not in allowed_extensions:
                continue

            try:

                with open(file, "r", encoding="utf-8") as f:

                    content = f.read()

                project_content += f"""

FILE: {file}

CONTENT:
{content}

==================================================
"""

            except Exception:
                continue

        return project_content, None

    except Exception as e:

        return None, str(e)