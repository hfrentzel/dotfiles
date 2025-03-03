import json
from logging import Logger
from typing import TYPE_CHECKING, Any, Dict, List

from setup.job import Job
from setup.managers.package_types.deb import deb_builder
from setup.managers.package_types.tar import tar_builder
from setup.managers.package_types.zip import zip_builder
from setup.output import red
from setup.process import async_proc, filter_assets

if TYPE_CHECKING:
    from setup.managers.exe import Exe


class Gitlab:
    @classmethod
    def gitlab_builder(cls, resource: "Exe") -> Job:
        async def inner(logger: Logger) -> bool:
            logger.info(f"Installing {resource.name} from Gitlab release")
            repo = resource.repo
            tag = await cls.get_release(repo, resource.version, logger)

            available_assets = await cls.get_assets(repo, tag, logger)
            asset = filter_assets(list(available_assets.keys()))
            if asset is None:
                logger.error(
                    red(
                        f"Failed to install {resource.name} from Gitlab release"
                    )
                )
                return False

            resource.url = (
                f"https://gitlab.com/{repo}/-"
                + f"/releases/{tag}/downloads/{available_assets[asset]}"
            )

            if asset.endswith(".deb"):
                return await deb_builder(resource).run()
            if asset.endswith(".zip"):
                return await zip_builder(resource).run()
            if ".tar." in asset:
                return await tar_builder(resource).run()

            return False

        return Job(
            name=resource.name,
            description=f"Install {resource.name} from Gitlab release",
            job=inner,
        )

    @classmethod
    async def get_assets(
        cls, repo: str, tag: str, logger: Logger
    ) -> Dict[str, str]:
        response = await cls.glab_api_call(
            f"{repo.replace('/', '%2F')}/releases/{tag}", logger
        )
        return {
            a["name"].lower(): a["name"] for a in response["assets"]["links"]
        }

    @classmethod
    async def get_release(cls, repo: str, version: str, logger: Logger) -> str:
        response = await cls.glab_api_call(
            f"{repo.replace('/', '%2F')}/releases", logger
        )
        releases: List[str] = [r["tag_name"] for r in response]
        return next(r for r in releases if version in r)

    @classmethod
    async def glab_api_call(cls, path: str, logger: Logger) -> Any:
        url = f"https://gitlab.com/api/v4/projects/{path}"
        result = await async_proc(f"curl {url}", logger=logger)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
