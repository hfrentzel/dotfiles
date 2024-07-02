import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.conf import conf
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid
from setup.process import async_proc


@dataclass
class Parser(Manager):
    desired: ClassVar[List["Parser"]] = []
    name: str
    language: str
    state: Tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def set_status(self) -> None:
        self._set_status()

    def _set_status(self) -> None:
        file = f"{self.language}.so"
        if os.path.exists(f"{conf.parser_dir}/{file}"):
            self.state = (True, "INSTALLED")
            return
        self.state = (False, "MISSING")

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
            parser._set_status()
            if cls.state[0]:
                complete.append(parser.name)
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for parser in sorted(cls.desired, key=(lambda s: s.language)):
            if not show_all and parser.state[0]:
                continue
            lines.append((parser.language, (parser.state[1], parser.state[0])))
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
