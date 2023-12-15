import json
from typing import Any

from setup2.job import Job
from setup2.output import red
from setup2.process import async_proc, filter_assets
from setup2.managers.exe_class import Exe
from setup2.managers.package_types.deb import deb_builder
from setup2.managers.package_types.tar import tar_builder
from setup2.managers.package_types.zip import zip_builder


class Gitlab():

    @classmethod
    def gitlab_builder(cls, spec: Exe) -> Job:
        async def inner() -> bool:
            repo = spec.repo
            tag = await cls.get_release(repo, spec.version)

            response = await cls.glab_api_call(f'{repo.replace("/", "%2F")}/releases/{tag}')
            available_assets = {a['name'].lower(): a['name'] for a in response['assets']['links']}

            asset = filter_assets(list(available_assets.keys()))
            if asset is None:
                print(red(f'Failed to install {spec.name} from Gitlab release'))
                return False

            spec.url = f'https://gitlab.com/{repo}/-' + \
                       f'/releases/{tag}/downloads/{available_assets[asset]}'

            if asset.endswith('.deb'):
                return await deb_builder(spec).run()
            if asset.endswith('.zip'):
                return await zip_builder(spec).run()
            if '.tar.' in asset:
                return await tar_builder(spec).run()

            return False

        return Job(names=[spec.name],
                   description=f'Install {spec.name} from Github release',
                   job=inner)

    @classmethod
    async def get_release(cls, repo: str, version: str) -> str:
        response = await cls.glab_api_call(f'{repo.replace("/", "%2F")}/releases')
        releases = [r['tag_name'] for r in response]
        return next(r for r in releases if version in r)

    @classmethod
    async def glab_api_call(cls, path: str) -> Any:
        url = f'https://gitlab.com/api/v4/projects/{path}'
        result = await async_proc(f'curl {url}')
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
