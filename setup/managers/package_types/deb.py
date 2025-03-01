from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc, fetch_file

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def deb_builder(spec: "Exe", _: str = "") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(f"Installing {spec.name} from debian archive...")
        archive_file = await fetch_file(spec.url, spec.version)
        result = await async_proc(f"sudo apt install {archive_file}")
        success = not result.returncode
        if success:
            logger.info(green(f"{spec.name} has been installed successfully"))
        else:
            logger.error(
                red(f"Failed to install {spec.name} from debian archive")
            )
        return success

    return Job(
        name=spec.name,
        description=f"Install {spec.name} from debian archive",
        job=inner,
    )
