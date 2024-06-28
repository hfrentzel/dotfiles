import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid
from setup.process import async_proc


@dataclass
class Parser(Manager):
    desired: ClassVar[List["Parser"]] = []
    check_results: ClassVar[List[Tuple["Parser", bool, str]]] = []
    name: str
    language: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    def current_status(self) -> Tuple[bool, str]:
        file = f"{self.language}.so"
        parser_dir = os.path.expanduser("~/.local/share/nvim/site/self")
        if os.path.exists(f"{parser_dir}/{file}"):
            return (True, "INSTALLED")
        return (False, "MISSING")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for parser in sorted(cls.desired, key=lambda p: p.language):
            lines.append((parser.language,))
        return print_grid(("TREESITTER LANGUAGES",), lines)

    @classmethod
    async def get_statuses(cls) -> List[str]:
        complete = []
        for parser in cls.desired:
            result = cls.current_status(parser)
            if result[0]:
                complete.append(parser.name)
            cls.check_results.append((parser, *result))
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for parser, complete, status in sorted(cls.check_results, key=(lambda s: s[0].language)):
            if not show_all and complete:
                continue
            lines.append((parser.language, (status, complete)))
        return print_grid(("TS PARSER", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            names=[self.name],
            description=f"Install TS self for {self.language}",
            depends_on="neovim",
            job=self.install_ts_parser(self.language),
        )

    @staticmethod
    def install_ts_parser(language: str) -> Callable[[], Coroutine[None, None, bool]]:
        async def inner() -> bool:
            print(f"Installing Treesitter parser for {language}...")
            await async_proc(f'nvim --headless +"TSInstallSync {language}" +q')
            return True

        return inner
