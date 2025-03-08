import json
import os
from logging import Logger
from typing import TYPE_CHECKING, Any, Optional

from setup.conf import expand
from setup.job import Job
from setup.managers.package_types.deb import deb_builder
from setup.managers.package_types.tar import tar_builder
from setup.managers.package_types.zip import zip_builder
from setup.output import red
from setup.process import async_req, filter_assets

if TYPE_CHECKING:
    from setup.managers.exe import Exe


class GithubApiError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


class Github:
    token = None

    @classmethod
    def github_builder(cls, resource: "Exe") -> Job:
        async def inner(logger: Logger) -> bool:
            logger.info(f"Installing {resource.name} from Github release")
            repo = resource.repo
            try:
                tag = await cls.get_release(repo, resource.version, logger)

                available_assets = await cls.get_assets(repo, tag, logger)
            except GithubApiError as e:
                logger.error(
                    red(
                        f"Failed to install {resource.name} from Github"
                        f"release: {e.reason}"
                    )
                )
                return False
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
    async def get_assets(cls, repo: str, tag: str, logger: Logger) -> list[str]:
        response = await cls.gh_api_call(
            f"repos/{repo}/releases/tags/{tag}", logger
        )
        return [a["name"].lower() for a in response["assets"]]

    @classmethod
    async def get_release(cls, repo: str, version: str, logger: Logger) -> str:
        response = await cls.get_releases(repo, logger)
        releases = [r["tag_name"] for r in response]
        return next(r for r in releases if version in r)

    @classmethod
    async def get_releases(
        cls, repo: str, logger: Logger
    ) -> list[dict[str, str]]:
        return await cls.gh_api_call(f"repos/{repo}/releases", logger)

    @classmethod
    async def gh_api_call(cls, path: str, logger: Logger) -> Any:
        url = f"https://api.github.com/{path}"
        auth: dict[str, str] = {}
        while True:
            result = await async_req(url, headers=auth, logger=logger)
            if result.statuscode == 404:
                raise GithubApiError("Not Found")

            resp = json.loads(result.output)
            mess = resp.get("message", "") if isinstance(resp, dict) else ""
            if mess.startswith("API rate limit exceeded") and not auth:
                logger.debug("Hit Github rate limit")
                token = cls.get_token()
                if token is None:
                    raise GithubApiError(
                        "Rate limit was hit and credentials don't exist"
                    )
                auth = {"Authorization": f"Bearer {token}"}
            elif mess.startswith("Bad credentials"):
                raise GithubApiError(
                    "Rate limit was hit and credentials are bad"
                )
            else:
                break

        return resp

    @classmethod
    def get_token(cls) -> Optional[str]:
        # TODO Store and retrieve token some other way
        if cls.token is None:
            token_file = expand("~/.gh_token")
            if os.path.isfile(token_file):
                with open(token_file, encoding="utf-8") as f:
                    cls.token = f.read().strip("\n")
            else:
                return None
        return cls.token
