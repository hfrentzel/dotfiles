from .managers.exe import Resource as Exe
from .managers.package_types.github import Github
from .managers.package_types.gitlab import Gitlab
from .process import filter_assets
from .output import green, yellow, red


async def search_assets(exe: Exe):
    if 'Github' not in exe.installers and 'Gitlab' not in exe.installers:
        print(f'{exe.name} is not installable by Github or Gitlab')
        return

    if 'Github' in exe.installers:
        release = await Github.get_release(exe.repo, exe.version)
        assets = await Github.get_assets(exe.repo, release)
        selected_assets = filter_assets(assets, return_all=True)
    else:
        release = await Gitlab.get_release(exe.repo, exe.version)
        assets = list((await Gitlab.get_assets(exe.repo, release)).keys())
        selected_assets = filter_assets(assets, return_all=True)

    color = green
    if len(selected_assets) == 0:
        print(red('No assets remained after filtering'))
    if len(selected_assets) > 1:
        print(yellow('More than one asset remains after filtering'))
        color = yellow
    for asset in assets:
        if asset in selected_assets:
            print(f'* {color(asset)}')
        else:
            print(f'  {asset}')
