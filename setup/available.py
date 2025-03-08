# This code handle the `mysetup available` subcommand, which looks up the most
# recent releases of an executable on github to see if it is up to date
import json
import urllib.request

from .output import green


def get_releases(repo: str) -> list[dict]:
    url = f"https://api.github.com/repos/{repo}/releases"

    results = None
    with urllib.request.urlopen(url) as response:
        releases = json.loads(response.read())
        if len(releases) != 0:
            results = [{"name": r["tag_name"]} for r in releases]
    if results is None:
        url = f"https://api.github.com/repos/{repo}/tags"
        with urllib.request.urlopen(url) as response:
            tags = json.loads(response.read())
            results = [{"name": t["name"]} for t in tags]

    return results


def lookup_releases(spec: dict) -> None:
    repo = "/".join(spec["source_repo"].split("/")[-2:])
    releases = get_releases(repo)
    version = spec["version"]
    index = None
    for i, r in enumerate(releases):
        if version in r["name"]:
            index = i
            break
    if index is None:
        print(
            "No releases found matching the currently set "
            f"version '{spec['version']}'"
        )
        print(f"Most current version is {releases[0]['name']}")
        return

    if index == 0:
        print("Using the most-current version")

    for i in range(0, 4):
        if i == index:
            print(f"* {green(releases[i]['name'])}")
        else:
            print(f"  {releases[i]['name']}")
    if 0 <= index < 4:
        print(f"...{len(releases[4:])} other releases")
        return

    gap = index - 4
    if gap > 0:
        if gap > 2:
            print(f"...{gap - 2} other release(s)")
        if gap > 1:
            print(f"  {releases[index - 2]['name']}")
        print(f"  {releases[index - 1]['name']}")

    print(f"* {green(releases[index]['name'])}")
    print(f"  {releases[index + 1]['name']}")
    print(f"  {releases[index + 2]['name']}")
    print(f"...{len(releases) - (index + 2)} other release(s)")
