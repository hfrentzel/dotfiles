import json
import os
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
    def github_builder(cls, spec: "Exe", _: str = "") -> Job:
        async def inner() -> bool:
            repo = spec.repo
            tag = await cls.get_release(repo, spec.version)

            available_assets = await cls.get_assets(repo, tag)
            asset = filter_assets(available_assets)
            spec.url = f"https://github.com/{repo}/releases/download/{tag}/{asset}"

            if asset is None:
                print(red(f"Failed to install {spec.name} from Github release"))
                return False

            if asset.endswith(".deb"):
                await deb_builder(spec).run()
            elif asset.endswith(".zip"):
                await zip_builder(spec).run()
            elif ".tar." in asset:
                await tar_builder(spec).run()

            return True

        return Job(
            names=[spec.name], description=f"Install {spec.name} from Github release", job=inner
        )

    @classmethod
    async def get_assets(cls, repo: str, tag: str) -> List[str]:
        response = await cls.gh_api_call(f"repos/{repo}/releases/tags/{tag}")
        return [a["name"].lower() for a in response["assets"]]

    @classmethod
    async def get_release(cls, repo: str, version: str) -> str:
        response: List[Dict[str, str]] = await cls.gh_api_call(f"repos/{repo}/releases")
        releases = [r["tag_name"] for r in response]
        return next(r for r in releases if version in r)

    @classmethod
    async def gh_api_call(cls, path: str) -> Any:
        token = cls.get_token()
        url = f"https://api.github.com/{path}"
        result = await async_proc(f'curl -L -H "Authorization: Bearer {token}" {url}')
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
