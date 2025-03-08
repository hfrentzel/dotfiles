import asyncio
import logging
from asyncio import Future
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field


@dataclass
class Job:
    name: str
    job: Callable[[logging.Logger], Awaitable[bool]]
    description: str
    resources: list[str] = field(default_factory=list)
    needs_root_access: bool = False
    depends_on: list[str] = field(default_factory=list)
    children: list[Future] = field(default_factory=list)
    parents: list[Future] = field(default_factory=list)

    def __post_init__(self) -> None:
        if len(self.resources) == 0:
            self.resources = [self.name]

    async def run(self) -> bool:
        try:
            logger = logging.getLogger(self.name)

            if len(self.parents) != 0:
                parent_results = await asyncio.gather(*self.parents)
                if not all(p[1] for p in parent_results):
                    failures = [p[0] for p in parent_results if not p[1]]
                    logger.error(
                        f"Did not run job {self.name} because it had"
                        f"failed dependencies: {','.join(failures)}"
                    )
                    for f in self.children:
                        f.set_result((self.name, False))
                    return False

            result = await self.job(logger)
        except Exception as e:
            logger.error(e)
            result = False

        for f in self.children:
            f.set_result((self.name, result))
        return result

    def __repr__(self) -> str:
        return f"{self.resources}, {self.job}"
