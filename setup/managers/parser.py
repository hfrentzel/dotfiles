import os
from dataclasses import dataclass
from logging import Logger
from typing import ClassVar

from setup.conf import conf
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid
from setup.process import async_proc


@dataclass
class Parser(Manager):
    desired: ClassVar[list["Parser"]] = []
    missing: ClassVar[list["Parser"]] = []
    name: str
    language: str
    state: tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def _set_status(self) -> None:
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
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for parser in sorted(cls.desired, key=lambda s: s.language):
            if not show_all and parser.state[0]:
                continue
            lines.append((parser.language, (parser.state[1], parser.state[0])))
        return print_grid(("TS PARSER", "STATUS"), lines)

    def create_job(self) -> None:
        self.missing.append(self)

    @classmethod
    def parser_job(cls) -> Job:
        language_string = ",".join([f"'{p.language}'" for p in cls.missing])

        async def inner(logger: Logger) -> bool:
            logger.info(
                f"Installing Treesitter parsers for {language_string}..."
            )
            await async_proc(
                f"nvim --headless +\"lua require('nvim-treesitter')."
                f'install({{{language_string}}}):wait(300000)" +q',
                logger=logger,
            )
            return True

        return Job(
            name="ts_parser_install",
            resources=[p.name for p in cls.missing],
            description=f"Install treesitter parsers for {language_string}",
            depends_on=[
                "neovim",
                "submodules",
                "vimrc",
                "nvimconfig",
                "gcc",
                "tree-sitter-cli",
                "tree-sitter-config",
            ],
            job=inner,
        )
