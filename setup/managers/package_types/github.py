import json
import os
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


class Github:
    token = None

    @classmethod
    def github_builder(cls, resource: "Exe") -> Job:
        async def inner(logger: Logger) -> bool:
            logger.info(f"Installing {resource.name} from Github release")
            repo = resource.repo
            tag = await cls.get_release(repo, resource.version, logger)

            available_assets = await cls.get_assets(repo, tag, logger)
            asset = filter_assets(available_assets)
            resource.url = (
                f"https://github.com/{repo}/releases/download/{tag}/{asset}"
            )

            if asset is None:
                logger.error(
                    red(
                        f"Failed to install {resource.name} from Github release"
                    )
                )
                return False

            if asset.endswith(".deb"):
                await deb_builder(resource).run()
            elif asset.endswith(".zip"):
                await zip_builder(resource).run()
            elif ".tar." in asset:
                await tar_builder(resource).run()

            return True

        return Job(
            name=resource.name,
            description=f"Install {resource.name} from Github release",
            job=inner,
        )

    @classmethod
    async def get_assets(cls, repo: str, tag: str, logger: Logger) -> List[str]:
        response = await cls.gh_api_call(
            f"repos/{repo}/releases/tags/{tag}", logger
        )
        return [a["name"].lower() for a in response["assets"]]

    @classmethod
    async def get_release(cls, repo: str, version: str, logger: Logger) -> str:
        response: List[Dict[str, str]] = await cls.gh_api_call(
            f"repos/{repo}/releases", logger
        )
        releases = [r["tag_name"] for r in response]
        return next(r for r in releases if version in r)

    @classmethod
    async def gh_api_call(cls, path: str, logger: Logger) -> Any:
        token = cls.get_token()
        url = f"https://api.github.com/{path}"
        result = await async_proc(
            f'curl -L -H "Authorization: Bearer {token}" {url}', logger=logger
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)

    @classmethod
    def get_token(cls) -> str:
        # TODO Store and retrieve token some other way
        if cls.token is None:
            with open(os.path.expanduser("~/.gh_token"), encoding="utf-8") as f:
                cls.token = f.read().strip("\n")
        return cls.token
