from logging import Logger
from typing import TYPE_CHECKING

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


class Apt:
    resources: list[str] = []
    all_apts: set[str] = set()
    apt_repos: list[str] = []
    scripts: list[list[str]] = []

    @classmethod
    def apt_builder(cls, resource: "Exe") -> bool:
        for installer in resource.installers:
            if (
                isinstance(installer, dict)
                and installer.get("installer") == "Apt"
            ):
                if (apt_repo := installer.get("apt_repo")) is not None:
                    cls.apt_repos.append(apt_repo)
                if packages := installer.get("package_name"):
                    if isinstance(packages, str):
                        cls.all_apts.add(packages)
                    else:
                        cls.all_apts.update(packages)
                if script := installer.get("post_script"):
                    cls.scripts.append(script)
                break
            if installer == "Apt":
                cls.all_apts.add(resource.name)
                break
        cls.resources.append(resource.name)
        return True

    @classmethod
    def apt_job(cls) -> Job:
        async def inner(logger: Logger) -> bool:
            if len(cls.all_apts) == 0:
                return True
            apt_string = ",".join(cls.all_apts)
            logger.info(
                "Running apt install to install the following "
                f"packages: {apt_string}"
            )

            for repo in cls.apt_repos:
                result = await async_proc(
                    f"sudo add-apt-repository {repo} --yes", logger=logger
                )

            await async_proc("sudo apt update")
            result = await async_proc(
                f"sudo apt install --yes {' '.join(cls.all_apts)}",
                logger=logger,
            )
            success = not result.returncode
            if success:
                logger.info(
                    green(
                        "The following app(s) were successfully installed "
                        f"with apt: {apt_string}"
                    )
                )
                for script in cls.scripts:
                    for step in script:
                        result = await async_proc(step, logger=logger)
            else:
                logger.error(red("apt installation failed"))
                # TODO try installing packages one at a time
            return success

        return Job(
            name="apt_install",
            resources=cls.resources,
            description=f"Install {', '.join(cls.all_apts)} with Apt",
            needs_root_access=True,
            job=inner,
        )
