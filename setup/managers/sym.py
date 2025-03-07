import os
from dataclasses import dataclass
from logging import Logger
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.conf import expand
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid, yellow


@dataclass
class Symlink(Manager):
    desired: ClassVar[List["Symlink"]] = []
    name: str
    source: str
    target: str
    state: Tuple[bool, str] = (False, "")

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    async def _set_status(self) -> None:
        dest = expand(self.target)
        if os.path.isfile(dest) or os.path.isdir(dest):
            if os.path.islink(dest):
                self.state = (True, "LINKED")
                return
            self.state = (False, "BLOCKED")
            return
        if os.path.islink(dest):
            self.state = (False, "STALE")
            return
        self.state = (False, "MISSING")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for sym in sorted(cls.desired, key=lambda s: s.target):
            lines.append((sym.target,))
        return print_grid(("SYMLINKED FILES",), lines)

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for sym in sorted(cls.desired, key=lambda s: s.name):
            if not show_all and sym.state[0]:
                continue
            lines.append((sym.name, (sym.state[1], sym.state[0])))
        return print_grid(("SYMLINK", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            name=self.name,
            description=f"Generate symlink at {self.target}",
            job=self.create_symlink(self.source, self.target),
        )

    @staticmethod
    def create_symlink(
        source: str, target: str
    ) -> Callable[[Logger], Coroutine[None, None, bool]]:
        async def inner(logger: Logger) -> bool:
            src = expand(source)
            dest = expand(target)

            # Handle files that are blocking symlink
            if os.path.isfile(dest):
                old_folder = expand("~/.local/share/mysetup/old_files")
                old_file = os.path.basename(dest)
                old_file = os.path.join(old_folder, old_file + ".old")
                os.makedirs(old_folder, exist_ok=True)
                logger.warning(
                    yellow(
                        f"NOTE: {dest} already exists. "
                        f"This existing file will be moved to {old_file} "
                        "before the symlink is created."
                    )
                )
                os.rename(dest, old_file)

            logger.info(f"Creating symlink at {dest}...")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if os.path.islink(dest):
                os.remove(dest)
            os.symlink(src, dest)

            return True

        return inner
