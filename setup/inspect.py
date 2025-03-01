import logging
from typing import Optional

from .managers.exe import Exe
from .managers.package_types.github import Github
from .managers.package_types.gitlab import Gitlab
from .output import green, red, yellow
from .process import filter_assets


async def search_assets(exe: Exe) -> Optional[str]:
    logger = logging.getLogger("search_assets")
    if "Github" not in exe.installers and "Gitlab" not in exe.installers:
        print(f"{exe.name} is not installable by Github or Gitlab")
        return None

    if "Github" in exe.installers:
        release = await Github.get_release(exe.repo, exe.version, logger)
        assets = await Github.get_assets(exe.repo, release, logger)
        selected_assets = filter_assets(assets, return_all=True)
    else:
        release = await Gitlab.get_release(exe.repo, exe.version, logger)
        assets = list(
            (await Gitlab.get_assets(exe.repo, release, logger)).keys()
        )
        selected_assets = filter_assets(assets, return_all=True)

    color = green
    if len(selected_assets) == 0:
        print(red("No assets remained after filtering"))
    if len(selected_assets) > 1:
        print(yellow("More than one asset remains after filtering"))
        color = yellow
    for asset in assets:
        if asset in selected_assets:
            print(f"* {color(asset)}")
        else:
            print(f"  {asset}")
    return None
