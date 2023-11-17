from typing import Tuple, List


def print_grid(header: Tuple[str, ...], rows: List[Tuple[str, ...]]) -> str:
    if len(rows) == 0:
        return ""
    max_lengths = [0] * len(header)
    for row in [header, *rows]:
        for i, length in enumerate(max_lengths):
            max_lengths[i] = max(length, len(row[i]))

    line = ''
    for row in [header, *rows]:
        line += ' '.join([f'{r: <{max(13, max_lengths[i])}}'
                          for i, r in enumerate(row)]) + '\n'
    line += '\n'
    return line


def red(text: str) -> str:
    return f'\033[91m{text}\033[0m'


def green(text: str) -> str:
    return f'\033[92m{text}\033[0m'
