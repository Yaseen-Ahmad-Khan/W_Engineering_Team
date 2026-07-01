from crewai.tools import tool
from typing import Type
from pathlib import Path
PROJECT_ROOT = Path.cwd().resolve()


def safe_path(relative_path: str) -> Path:
    path = (PROJECT_ROOT / relative_path).resolve()

    if not str(path).startswith(str(PROJECT_ROOT)):
        raise ValueError("Access outside project directory is not allowed.")

    return path


@tool("Write File")
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file inside the project folder.
    Creates parent folders automatically.

    Example file_path:
    generated/frontend/src/App.jsx
    """
    path = safe_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"File written successfully: {file_path}"


@tool("Read File")
def read_file(file_path: str) -> str:
    """
    Read a file from the project folder.

    Example file_path:
    generated/backend/app.py
    """
    path = safe_path(file_path)

    if not path.exists():
        return f"File not found: {file_path}"

    return path.read_text(encoding="utf-8")


@tool("List Directory")
def list_directory(directory_path: str) -> str:
    """
    List all files and folders inside a directory.

    Example directory_path:
    generated
    """
    path = safe_path(directory_path)

    if not path.exists():
        return f"Directory not found: {directory_path}"

    if not path.is_dir():
        return f"Not a directory: {directory_path}"

    items = [str(item.relative_to(PROJECT_ROOT)) for item in path.rglob("*")]

    return "\n".join(items) if items else "Directory is empty."


@tool("Create Folder")
def create_folder(folder_path: str) -> str:
    """
    Create a folder inside the project directory.

    Example folder_path:
    generated/frontend/src
    """
    path = safe_path(folder_path)
    path.mkdir(parents=True, exist_ok=True)
    return f"Folder created successfully: {folder_path}"


@tool("Run Command")
def run_command(command: str) -> str:
    """
    Run a terminal command inside the project directory.
    This can be used to run commands like 'npm install', 'npm run build', 'pytest', or check if services are running.
    Always returns the stdout and stderr of the command.
    """
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            return f"Command failed with exit code {result.returncode}.\n{output}"
        return f"Command succeeded.\n{output}"
    except Exception as e:
        return f"Error executing command: {str(e)}"
