from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def cargo_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(f"Installing {resource.name} with cargo...")
        result = await async_proc(
            f"cargo install --version {resource.version} {resource.name}"
        )
        success = not result.returncode
        if success:
            logger.info(
                green(f"{resource.name} has been installed successfully")
            )
        else:
            logger.error(red(f"Failed to install {resource.name} with cargo"))
        return success

    return Job(
        name=resource.name,
        description=f"Install {resource.name} with cargo",
        depends_on=["cargo"],
        job=inner,
    )
