from os import path
from typing import Optional


def find_extract_path(filename: str, mode: int, command_name: str) -> Optional[str]:
    extension = path.splitext(filename)[1]
    if extension in {".ps1", ".zsh", ".fish"}:
        return None

    if extension == ".bash":
        extract_path = "share/bash-completion/completions"
    elif extension in {".1", ".5"}:
        man = extension.replace(".", "man")
        extract_path = f"share/man/{man}"
    elif extension in {".md", ".txt"}:
        extract_path = f"share/doc/{command_name}"
    elif not extension:
        if mode & 0o111:
            extract_path = "bin"
        else:
            extract_path = f"share/doc/{command_name}"
    else:
        return None
    return extract_path
