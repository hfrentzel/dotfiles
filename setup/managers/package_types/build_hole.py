import json
import platform
from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.managers.package_types.tar import tar_builder
from setup.output import green
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def build_hole_builder(spec: "Exe", _: str = "") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(green(f"Starting {spec.name} install with build-hole"))
        hole = await get_hole(logger)

        hardware = platform.uname().machine.lower()
        if hardware == "x86_64":
            env = "x86_64-linux-20.04"
        else:
            env = "aarch64-linux-22.04"
        spec.url = hole[spec.name][spec.version][env]

        return await tar_builder(spec).run()

    return Job(
        name=spec.name,
        description=f"Install {spec.name} from build-hole",
        job=inner,
    )


async def get_hole(logger: Logger):
    url = "https://raw.githubusercontent.com/hfrentzel/build-hole/master/hole.json"
    result = await async_proc(f"curl -L {url}", logger=logger)
    hole = json.loads(result.stdout)
    return hole
