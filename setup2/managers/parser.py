from dataclasses import dataclass
from typing import List, Tuple, Coroutine, Callable
import os

from setup2.job import Job
from setup2.output import print_grid
from setup2.process import async_proc
from setup2.managers.manager import mark_resource


@dataclass
class Resource:
    name: str
    language: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        desired.append(self)


desired: List[Resource] = []
check_results: List[Tuple[Resource, bool, str]] = []


def current_status(parser: Resource) -> Tuple[bool, str]:
    file = f"{parser.language}.so"
    parser_dir = os.path.expanduser("~/.local/share/nvim/site/parser")
    if os.path.exists(f"{parser_dir}/{file}"):
        return (True, "INSTALLED")
    return (False, "MISSING")


def desired_printout() -> str:
    lines = []
    for parser in sorted(desired, key=lambda p: p.language):
        lines.append((parser.language,))
    return print_grid(("TREESITTER LANGUAGES",), lines)


async def get_statuses() -> List[str]:
    complete = []
    for parser in desired:
        result = current_status(parser)
        if result[0]:
            complete.append(parser.name)
        check_results.append((parser, *result))
    return complete


def status_printout(show_all: bool) -> str:
    lines = []
    for parser, complete, status in sorted(check_results, key=(lambda s: s[0].language)):
        if not show_all and complete:
            continue
        lines.append((parser.language, (status, complete)))
    return print_grid(("TS PARSER", "STATUS"), lines)


def create_job(parser: Resource) -> Job:
    return Job(
        names=[parser.name],
        description=f"Install TS parser for {parser.language}",
        depends_on="neovim",
        job=install_ts_parser(parser.language),
    )


def install_ts_parser(language: str) -> Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        print(f"Installing Treesitter parser for {language}...")
        await async_proc(f'nvim --headless +"TSInstallSync {language}" +q')
        return True

    return inner
