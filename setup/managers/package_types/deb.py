from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc, fetch_file

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def deb_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(f"Installing {resource.name} from debian archive...")
        archive_file = await fetch_file(resource.url, resource.version)
        result = await async_proc(f"sudo apt install {archive_file}")
        success = not result.returncode
        if success:
            logger.info(
                green(f"{resource.name} has been installed successfully")
            )
        else:
            logger.error(
                red(f"Failed to install {resource.name} from debian archive")
            )
        return success

    return Job(
        name=resource.name,
        description=f"Install {resource.name} from debian archive",
        job=inner,
    )
