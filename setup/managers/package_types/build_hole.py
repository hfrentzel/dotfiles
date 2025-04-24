import json
from logging import Logger
from typing import TYPE_CHECKING, Any

from setup.job import Job
from setup.managers.package_types.tar import tar_builder
from setup.output import green
from setup.process import async_req, get_system

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def build_hole_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(green(f"Starting {resource.name} install with build-hole"))
        hole = await get_hole(logger)

        env = get_system()
        resource.url = hole[resource.name][resource.version][env]
        resource.installers = ["Tar"]

        if isinstance(job := tar_builder(resource), Job):
            return await job.run()
        return False

    return Job(
        name=resource.name,
        description=f"Install {resource.name} from build-hole",
        job=inner,
    )


async def get_hole(logger: Logger) -> Any:
    url = "https://raw.githubusercontent.com/hfrentzel/build-hole/master/hole.json"
    result = await async_req(url, logger=logger)
    hole = json.loads(result.output)
    return hole
