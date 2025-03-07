import json
import platform
from logging import Logger
from typing import TYPE_CHECKING, Any

from setup.job import Job
from setup.managers.package_types.tar import tar_builder
from setup.output import green
from setup.process import async_req

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def build_hole_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(green(f"Starting {resource.name} install with build-hole"))
        hole = await get_hole(logger)

        hardware = platform.uname().machine.lower()
        if hardware == "x86_64":
            env = "x86_64-linux-22.04"
        else:
            env = "aarch64-linux-22.04"
        resource.url = hole[resource.name][resource.version][env]

        return await tar_builder(resource).run()

    return Job(
        name=resource.name,
        description=f"Install {resource.name} from build-hole",
        job=inner,
    )


async def get_hole(logger: Logger) -> Any:
    url = "https://raw.githubusercontent.com/hfrentzel/build-hole/master/hole.json"
    result = await async_req(url, logger=logger)
    hole = json.loads(result)
    return hole
