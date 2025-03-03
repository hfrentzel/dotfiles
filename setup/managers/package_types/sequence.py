from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def sequence_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(f"Beginning steps to install {resource.name}")
        for step_template in resource.steps:
            step = step_template.format(version=resource.version)
            result = await async_proc(step, logger=logger)
            if result.returncode != 0:
                logger.error(
                    f"{resource.name} installation failed on step: {step}"
                )
                return False

        return True

    return Job(
        name=resource.name,
        description=f"Execute {resource.name} installation sequence",
        depends_on=resource.depends_on,
        job=inner,
    )
