from typing import TYPE_CHECKING, List

from setup.job import Job
from setup.output import green, red
from setup.process import async_proc

if TYPE_CHECKING:
    from setup.managers.exe import Exe


class Apt:
    all_apts: List[str] = []
    apt_repos: List[str] = []
    scripts: List[List[str]] = []

    @classmethod
    def apt_builder(cls, spec: "Exe", package: str) -> bool:
        for installer in spec.installers:
            if (
                isinstance(installer, dict)
                and installer.get("installer") == "Apt"
            ):
                if (apt_repo := installer.get("apt_repo")) is not None:
                    cls.apt_repos.append(apt_repo)
                if packages := installer.get("package_name"):
                    if isinstance(packages, str):
                        cls.all_apts.append(packages)
                    else:
                        cls.all_apts.extend(packages)
                if script := installer.get("post_script"):
                    cls.scripts.append(script)
                break
            if installer == "Apt":
                cls.all_apts.append(package)
                break
        return True

    @classmethod
    def apt_job(cls) -> Job:
        async def inner() -> bool:
            if len(cls.all_apts) == 0:
                return True
            print("Running apt install...")

            for repo in cls.apt_repos:
                result = await async_proc(
                    f"sudo add-apt-repository {repo} --yes"
                )

            await async_proc("sudo apt update")
            result = await async_proc(
                f"sudo apt install --yes {' '.join(cls.all_apts)}"
            )
            success = not result.returncode
            if success:
                print(
                    green(
                        "The following app(s) were successfully installed "
                        f"with apt: {','.join(cls.all_apts)}"
                    )
                )
                for script in cls.scripts:
                    for step in script:
                        result = await async_proc(step)
            else:
                print(red("apt installation failed"))
                # TODO try installing packages one at a time
            return success

        return Job(
            names=cls.all_apts,
            description=f"Install {', '.join(cls.all_apts)} with Apt",
            job=inner,
        )
