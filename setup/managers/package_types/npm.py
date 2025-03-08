import json
import os
from logging import Logger
from typing import Optional

from setup.conf import expand
from setup.job import Job
from setup.managers.manager import Package
from setup.managers.package_types.versioning import check_install
from setup.output import green, red
from setup.process import async_proc


class Npm:
    all_packages: list[tuple[str, str]] = []

    @classmethod
    def npm_builder(cls, resource: Package) -> bool:
        cls.all_packages.append((resource.name, resource.version))
        return True

    @classmethod
    def npm_job(cls) -> Job:
        npm_string = " ".join([f"{p[0]}@{p[1]}" for p in cls.all_packages])

        async def inner(logger: Logger) -> bool:
            if len(cls.all_packages) == 0:
                return True
            resources_str = ",".join(p[0] for p in cls.all_packages)

            logger.info(f"Running npm install for resources: {resources_str}")
            result = await async_proc(
                f"npm install -g {npm_string}", logger=logger
            )
            success = not result.returncode
            if success:
                logger.info(
                    green(
                        "The following apps were successfully installed "
                        f"with npm: {resources_str}"
                    )
                )
            else:
                logger.error(red("npm installation failed"))
                # TODO try installing packages one at a time
            return success

        return Job(
            name="npm_install",
            resources=[p[0] for p in cls.all_packages],
            description=f"Install {','.join(p[0] for p in cls.all_packages)} "
            "with npm",
            depends_on=["node"],
            job=inner,
        )

    @classmethod
    def get_version(cls, package: Package) -> Optional[str]:
        path = os.path.join(
            expand("~/.local/lib/node_modules"),
            package.name,
            "package.json",
        )
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            if isinstance(version := json.loads(f.read()).get("version"), str):
                return version
        return None

    @classmethod
    def check_install(cls, package: Package) -> tuple[bool, str]:
        curr_ver = cls.get_version(package)
        return check_install(curr_ver, package)
