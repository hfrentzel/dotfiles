import os
from dataclasses import dataclass
from typing import Callable, ClassVar, Coroutine, List, Tuple

from setup.conf import conf
from setup.job import Job
from setup.managers.manager import Manager, mark_resource
from setup.output import print_grid


@dataclass
class Symlink(Manager):
    desired: ClassVar[List["Symlink"]] = []
    check_results: ClassVar[List[Tuple["Symlink", bool, str]]] = []
    name: str
    source: str
    target: str

    def __post_init__(self) -> None:
        mark_resource(self.name)
        self.desired.append(self)

    def current_status(self) -> Tuple[bool, str]:
        dest = os.path.expanduser(self.target)
        if os.path.isfile(dest) or os.path.isdir(dest):
            if os.path.islink(dest):
                return (True, "LINKED")
            return (False, "BLOCKED")
        if os.path.islink(dest):
            return (False, "STALE")
        return (False, "MISSING")

    @classmethod
    def desired_printout(cls) -> str:
        lines = []
        for sym in sorted(cls.desired, key=lambda s: s.target):
            lines.append((sym.target,))
        return print_grid(("SYMLINKED FILES",), lines)

    @classmethod
    async def get_statuses(cls) -> List[str]:
        complete = []
        for sym in cls.desired:
            result = cls.current_status(sym)
            if result[0]:
                complete.append(sym.name)
            cls.check_results.append((sym, *result))
        return complete

    @classmethod
    def status_printout(cls, show_all: bool) -> str:
        lines = []
        for sym, complete, status in sorted(cls.check_results, key=(lambda s: s[0].name)):
            if not show_all and complete:
                continue
            lines.append((sym.name, (status, complete)))
        return print_grid(("SYMLINK", "STATUS"), lines)

    def create_job(self) -> Job:
        return Job(
            names=[self.name],
            description=f"Generate symlink at {self.target}",
            job=self.create_symlink(self.source, self.target),
        )

    @staticmethod
    def create_symlink(source: str, target: str) -> Callable[[], Coroutine[None, None, bool]]:
        async def inner() -> bool:
            src = source.replace("DOT", conf.dotfiles_home)
            src = os.path.expanduser(src)
            dest = os.path.expanduser(target)
            print(f"Creating symlink at {dest}...")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if os.path.islink(dest):
                os.remove(dest)
            os.symlink(src, dest)

            return True

        return inner
