import logging
import re
from typing import Any, Dict, Optional

from .managers.package_types.github import Github, GithubApiError
from .managers.package_types.gitlab import Gitlab
from .output import green, red, yellow
from .process import filter_assets


async def search_assets(name: str, spec: Dict[str, Any]) -> Optional[str]:
    logger = logging.getLogger("search_assets")
    if spec.get("version") is None:
        print(f"{name} does not have a version specified")
        return None
    if spec.get("source_repo") is None:
        print(f"{name} does not have a repository specified")
        return None

    match = re.search(
        r"(?:https?://)?(github.com|gitlab.com)/(\S+)", spec["source_repo"]
    )
    if match:
        hostname = match.group(1)
        repo = match.group(2)
    else:
        print(f'Failed to parse the "source_repo" field of the {name} spec')
        return None

    version = spec["version"]
    if hostname == "github.com":
        try:
            release = await Github.get_release(repo, version, logger)
            assets = await Github.get_assets(repo, release, logger)
        except GithubApiError as e:
            logger.error(red(f"Github API call failed: {e.reason}"))
            return None
        selected_assets = filter_assets(assets, return_all=True)
    else:
        release = await Gitlab.get_release(repo, version, logger)
        assets = list((await Gitlab.get_assets(repo, release, logger)).keys())
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
