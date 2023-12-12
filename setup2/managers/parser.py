from dataclasses import dataclass
from typing import ClassVar, List, Tuple, Dict, Coroutine, Callable
import os

from setup2.conf import conf
from setup2.job import Job
from setup2.output import print_grid, red, green
from setup2.process import async_proc
from setup2.managers.manager import mark_resource


@dataclass
class Parser():
    desired: ClassVar[List['Parser']] = []
    name: str
    language: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)


check_results: List[Tuple[Parser, bool, str]] = []


def check_job(parser: Parser) -> Tuple[bool, str]:
    file = f'{parser.language}.so'
    parser_dir = os.path.expanduser('~/.local/share/nvim/site/parser')
    if os.path.exists(f'{parser_dir}/{file}'):
        return (True, green('INSTALLED'))
    return (False, red('MISSING'))


def desired_printout() -> str:
    lines = []
    for parser in sorted(Parser.desired, key=lambda p: p.language):
        lines.append((parser.language,))
    return print_grid(('TREESITTER LANGUAGES',), lines)


async def get_statuses() -> None:
    for parser in Parser.desired:
        check_results.append((parser, *check_job(parser)))


def status_printout(show_all: bool) -> str:
    lines = []
    for parser, complete, status in sorted(check_results, key=(lambda s: s[0].language)):
        if not show_all and complete:
            continue
        lines.append((parser.language, status))
    return print_grid(('TS PARSER', 'STATUS'), lines)


def create_jobs() -> Tuple[List[str], Dict[str, Job]]:
    no_action_needed = []
    jobs = {}
    for parser, complete, status in check_results:
        if complete:
            no_action_needed.append(parser.language)
        else:
            jobs[parser.name] = Job(
                names=[parser.name],
                description=f'Install TS parser for {parser.language}',
                depends_on='neovim',
                job=install_ts_parser(parser.language)
            )

    return no_action_needed, jobs


def install_ts_parser(language: str) -> Callable[[], Coroutine[None, None, bool]]:
    async def inner() -> bool:
        print(f'Installing Treesitter parser for {language}...')
        await async_proc(f'nvim --headless +"TSInstallSync {language}" +q')
        return True

    return inner
