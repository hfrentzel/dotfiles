import logging
import os
import re
import tarfile
from typing import Any, Dict, List, Optional

from .managers.package_types.github import Github, GithubApiError
from .managers.package_types.gitlab import Gitlab
from .managers.package_types.tar import extract_tar
from .menu import MenuPiece, show
from .output import green, red, yellow
from .process import fetch_file, filter_assets


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


class Picker(MenuPiece):
    def __init__(self, items: List[str]):
        self.items = items
        self.index = -1

    def get(self, index: int) -> str:
        return self.items[index]

    def len(self) -> int:
        return len(self.items)

    @staticmethod
    def keys() -> List[str]:
        return ["enter"]

    def action(self, key, index: int) -> bool:
        self.index = index
        return True


async def get_asset(repo: str) -> None:
    logger = logging.getLogger("get_asset")
    match = re.search(r"(?:https?://)?(github.com|gitlab.com)/(\S+)", repo)
    if match:
        repo = match.group(2)

    try:
        releases = await Github.get_releases(repo, logger)
    except GithubApiError as e:
        if e.reason == "Not Found":
            print(f"Repo {repo} not found")
            return
        raise e
    release_names = [release["name"] for release in releases[0:10]]

    i = show(Picker(release_names))
    if i == -1:
        return
    print(f"Listing assets for {repo} release {release_names[i]}")
    tag = releases[i]["tag_name"]
    assets = await Github.get_assets(repo, tag, logger)
    i = show(Picker(assets))
    if i == -1:
        return
    print(f"Downloading {assets[i]}...")
    download_url = (
        f"https://github.com/{repo}/releases/download/{tag}/{assets[i]}"
    )
    filename = await fetch_file(download_url)
    print(f"Downloaded asset to {filename}")
    resp = input("What do you want to now: [L]ist, [E]xtract, [N]othing: ")

    if not resp or resp[0].lower() not in {"l", "e"}:
        return

    if (letter := resp[0].lower()) == "e":
        extract_path = os.path.dirname(filename)
        extract_tar(filename, extract_path, "")
        print(f"Tarball extracted to {os.path.splitext(filename)[0]}")
    elif letter == "l":
        with tarfile.open(filename) as tar:
            files = tar.getnames()
            for i in range(0, min(20, len(files))):
                print(files[i])
            if len(files) > 20:
                print(f"...and {len(files) - 20} more")
