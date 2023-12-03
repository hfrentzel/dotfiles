import json
import os
from typing import List, Optional, Any, Dict

from setup2.job import Job
from setup2.output import red
from setup2.process import async_proc
from setup2.managers.exe_class import Exe
from setup2.managers.package_types.deb import deb_builder
from setup2.managers.package_types.tar import tar_builder
from setup2.managers.package_types.zip import zip_builder


class Github():
    token = None

    @classmethod
    def github_builder(cls, spec: Exe) -> Job:
        async def inner() -> bool:
            repo = spec.repo
            tag = await cls.get_release(repo, spec.version)

            response = await cls.gh_api_call(f'repos/{repo}/releases/tags/{tag}')
            available_assets = [a['name'].lower() for a in response['assets']]

            asset = cls.filter_assets(available_assets)
            spec.url = f'https://github.com/{repo}/releases/download/{tag}/{asset}'

            if asset is None:
                print(red(f'Failed to install {spec.name} from Github release'))
                return False

            if asset.endswith('.deb'):
                await deb_builder(spec).run()
            elif asset.endswith('.zip'):
                await zip_builder(spec).run()
            elif '.tar.' in asset:
                await tar_builder(spec).run()

            return True

        return Job(names=[spec.name],
                   description=f'Install {spec.name} from Github release',
                   job=inner)

    @classmethod
    async def get_release(cls, repo: str, version: str) -> str:
        response: List[Dict[str, str]] = await cls.gh_api_call(f'repos/{repo}/releases')
        releases = [r['tag_name'] for r in response]
        return next(r for r in releases if version in r)

    @staticmethod
    def filter_assets(asset_list: List[str]) -> Optional[str]:
        # TODO Infer these values from environment and handle other
        # possibilities
        system_os = 'linux'
        hardware = 'x86_64'
        hardware_alt = 'amd64'
        if False and any(a.endwiths('.deb') for a in asset_list):
            # TODO handle deb files when sudo permissions are available
            pass

        if any(system_os in a for a in asset_list):
            asset_list = [a for a in asset_list if system_os in a]
        if any(hardware in a for a in asset_list):
            asset_list = [a for a in asset_list if hardware in a]
        if any(hardware_alt in a for a in asset_list):
            asset_list = [a for a in asset_list if hardware_alt in a]

        if system_os == 'linux' and hardware == 'x86_64' and len(asset_list) == 2:
            asset_list = [a for a in asset_list if 'musl' in a]

        if len(asset_list) == 1:
            return asset_list[0]
        return None

    @classmethod
    async def gh_api_call(cls, path: str) -> Any:
        token = cls.get_token()
        url = f'https://api.github.com/{path}'
        result = await async_proc(f'curl -L -H "Authorization: Bearer {token}" {url}')
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)

    @classmethod
    def get_token(cls) -> str:
        # TODO Store and retrieve token some other way
        if cls.token is None:
            with open(os.path.expanduser('~/.gh_token'), encoding='utf-8') as f:
                cls.token = f.read().strip('\n')
        return cls.token