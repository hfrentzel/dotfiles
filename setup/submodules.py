import re
import shlex
import subprocess

from .conf import conf, expand


def check_submodules():
    print("Fetcing submodules")
    subprocess.run(
        shlex.split("git submodule foreach git fetch"), capture_output=True
    )

    cmd = (
        "git submodule --quiet foreach "
        "'echo ${PWD##*/}; "
        "git show -s --format=%ci; "
        "git rev-list --count `git rev-parse --abbrev-ref HEAD`"
        "..`git rev-parse --abbrev-ref origin/HEAD`'"
    )

    result = subprocess.run(shlex.split(cmd), capture_output=True)

    lines = result.stdout.decode().split("\n")

    data = list(zip(*[iter(lines)] * 3))
    data.sort(key=lambda x: (int(x[2]) == 0, x[1]), reverse=True)

    max_len = max(len(d[0]) for d in data)

    for d in data:
        date = d[1].split(" ")[0]
        commits_behind = int(d[2])
        if commits_behind == 0:
            behind_statement = "Up to Date"
        else:
            behind_statement = f"{commits_behind: <3} commits_behind"

        print(f"{d[0]: <{max_len}}  Last Updated: {date}, {behind_statement}")


def submodule_diff():
    repo = conf.args.repo[0]
    with open(expand("DOT/.gitmodules"), encoding="utf-8") as f:
        data = f.read()
    match = re.search(rf'\[submodule "(.+/{repo})"\]', data)
    if not match:
        print(f"Submodule directory {repo} not found")
        return
    git_dir = expand(f"DOT/{match.group(1)}")
    cmd = f"git -C {git_dir} log --oneline --color=always HEAD..origin/HEAD"

    result = subprocess.run(shlex.split(cmd), capture_output=True)
    lines = result.stdout.decode().split("\n")[:-1]
    if len(lines) != 0:
        print("\n".join(lines))
        print(f"{repo} is behind {len(lines)} commit(s)")
    else:
        print(f"{repo} is up to date")


def submodule_pull():
    repo = conf.args.repo[0]
    with open(expand("DOT/.gitmodules"), encoding="utf-8") as f:
        data = f.read()
    match = re.search(rf'\[submodule "(.+/{repo})"\]', data)
    if not match:
        print(f"Submodule directory {repo} not found")
        return
    git_dir = expand(f"DOT/{match.group(1)}")
    cmd = f"git -C {git_dir} pull"
    subprocess.run(shlex.split(cmd))


if __name__ == "__main__":
    check_submodules()
