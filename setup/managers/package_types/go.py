import os
from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def go_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        os.environ["GOBIN"] = os.path.expanduser("~/.local/bin")
        os.environ["GOMODCACHE"] = os.path.expanduser("~/.cache/go/mod")
        os.environ["GOPATH"] = os.path.expanduser("~/.local/share/go")

        logger.info(f"Installing {resource.name} with go...")
        result = await async_proc(
            f"go install {resource.url}@v{resource.version}", logger=logger
        )
        success = not result.returncode
        if success:
            logger.info(
                green(f"{resource.name} has been installed successfully")
            )
        else:
            logger.error(red(f"Failed to install {resource.name} with go"))
        return success

    return Job(
        name=resource.name,
        description=f"Install {resource.name} with go",
        depends_on=["go"],
        job=inner,
    )
