from typing import Sequence, Tuple, Union


def print_grid(
    header: Tuple[str, ...], rows: Sequence[Tuple[Union[str, Tuple[str, bool]], ...]]
) -> str:
    if len(rows) == 0:
        return ""
    max_lengths = [0] * len(header)
    for row in [header, *rows]:
        for i, length in enumerate(max_lengths):
            if isinstance(row[i], str):
                item_len = len(row[i])
            else:
                item_len = len(row[i][0])
            max_lengths[i] = max(length, item_len)

    line = ""
    for row in [header, *rows]:
        line += (
            " ".join([
                f"{r if isinstance(r, str) else (green if r[1] else red)(r[0]): <{max(13, max_lengths[i])}}"
                for i, r in enumerate(row)
            ])
            + "\n"
        )
    line += "\n"
    return line


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"


def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"
