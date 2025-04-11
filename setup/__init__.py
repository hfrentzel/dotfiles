import argparse
import asyncio
import datetime
import json
import logging
import os
import webbrowser

from .available import lookup_releases
from .builder import (
    NoSpecError,
    build_resources,
    edit_config,
    get_resource,
    get_spec,
)
from .conf import conf, expand
from .inspect import get_asset, search_assets
from .managers import (
    ALL_MANAGERS,
    Manager,
    all_desired,
    create_bonus_jobs,
)
from .output import green, red
from .process import OutputTracker, async_proc
from .submodules import check_submodules, submodule_diff, submodule_pull
from .tree import build_tree, create_jobs, print_job_tree

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


async def handle_jobs(
    resources: list[Manager], selected_types: list[type[Manager]]
) -> None:
    logger = logging.getLogger("mysetup")
    if conf.args.stage == "desired":
        for t in selected_types:
            print(t.desired_printout(), end="")
        return

    all_complete = await asyncio.gather(*[r.get_status() for r in resources])
    complete = {r.name for r, c in zip(resources, all_complete) if c}
    if conf.args.stage in {None, "show_all"}:
        for t in selected_types:
            print(t.status_printout(bool(conf.args.stage)), end="")
        return

    jobs = await create_jobs(resources, complete)
    if len(jobs) == 0:
        logger.info("No jobs to run. All resources are setup")
        return

    if conf.args.stage == "jobs":
        for m in jobs:
            print(m.description)
        return

    ready_jobs, tree = await build_tree(jobs)
    if conf.args.stage == "tree":
        print_job_tree(tree)
        return

    timestamp = (
        f"{datetime.datetime.now().isoformat().replace(':', '/')}_output.txt"
    )
    try:
        need_root_access = any(j.needs_root_access for j in ready_jobs)
        if need_root_access:
            await async_proc("sudo echo")
        success = all(await asyncio.gather(*[job.run() for job in ready_jobs]))
    except Exception as e:
        success = False
        raise e
    finally:
        filename = expand(f"~/.local/share/mysetup/log/{timestamp}")
        OutputTracker.write_logs(filename)
        if success:
            logger.info(green("All resources have been setup successfully"))
        else:
            logger.error(
                red(
                    "Not all jobs were successful. "
                    f"Check logs at {filename} for details"
                )
            )


async def handle_single_resource(resource: Manager) -> None:
    if await resource.get_status():
        print(f"{resource.name} is already set up")
        return

    job = resource.create_job() or list(create_bonus_jobs().values())[0]

    if len(job.depends_on) != 0:
        if not any(d.name in job.depends_on for d in all_desired()):
            dependency = get_resource(job.depends_on[0])
            if dependency is None:
                raise ValueError(
                    f"{job.name} is dependent on {job.depends_on[0]}, "
                    "which is not managed on this OS"
                )
            complete = (
                [dependency.name] if await dependency.get_status() else []
            )
        else:
            complete = []

        if remaining := set(job.depends_on) - set(complete):
            print(
                f"Can't set up {resource.name} because it has "
                f"unsatisfied dependencies: {remaining}"
            )
            return

    if conf.args.stage != "run":
        print(f"{resource.name} can be set up. Rerun with -r to run the job")
        return

    if await job.run():
        print(green(f"{resource.name} set up successfully"))
    else:
        print(red(f"Failed to set up {resource.name}"))


def check() -> None:
    if conf.args.only is not None:
        resource = get_resource(conf.args.only)
        if resource is None:
            print(f"{conf.args.only} can not be set up on this OS")
            return
        asyncio.run(handle_single_resource(resource))
        return

    types = conf.args.types or list(ALL_MANAGERS.keys())
    managers = [ALL_MANAGERS[t] for t in types]

    resources = build_resources(types)
    asyncio.run(handle_jobs(resources, managers))


def show() -> None:
    name = conf.args.spec[0]
    spec = get_spec(name)
    print(json.dumps({name: spec}, indent=4))


def home() -> None:
    name = conf.args.spec[0]
    spec = get_spec(name)

    if home_url := spec.get("homepage"):
        webbrowser.open(home_url)
    elif source_url := spec.get("source_repo"):
        webbrowser.open(source_url)
    else:
        print(f"No home page listed for '{name}'")


def source() -> None:
    name = conf.args.spec[0]
    spec = get_spec(name)

    if source_url := spec.get("source_repo"):
        webbrowser.open(source_url)
    else:
        print(f"No source repository listed for '{name}'")


def list_assets() -> None:
    resource = get_spec(conf.args.spec[0])
    asyncio.run(search_assets(conf.args.spec[0], resource))


def config() -> None:
    edit_config()


def available() -> None:
    spec = get_spec(conf.args.spec[0])
    lookup_releases(spec)


def download() -> None:
    asyncio.run(get_asset(conf.args.repo[0]))


def run() -> None:
    argparser = argparse.ArgumentParser(prog="EnvSetup")
    argparser.set_defaults(func=check)
    argparser.add_argument(
        "-l",
        "--log",
        choices=list(LOG_LEVELS.keys()),
        default="info",
    )

    resources = argparser.add_mutually_exclusive_group()
    resources.add_argument(
        "-t", "--types", choices=ALL_MANAGERS.keys(), nargs="+"
    )
    resources.add_argument("-o", "--only")
    resources.add_argument("--force")

    stages = argparser.add_mutually_exclusive_group()
    stages.add_argument(
        "-s",
        "--stage",
        choices=["desired", "show_all", "jobs", "tree", "run"],
        default=None,
    )
    stages.add_argument(
        "-d", "--desired", action="store_const", const="desired", dest="stage"
    )
    stages.add_argument(
        "-r", "--run", action="store_const", const="run", dest="stage"
    )

    subparsers = argparser.add_subparsers(title="subcommands")
    show_cmd = subparsers.add_parser("show", help="show json spec")
    show_cmd.set_defaults(func=show)
    show_cmd.add_argument("spec", type=str, nargs=1)

    home_cmd = subparsers.add_parser("home", help="Go to tool's homepage")
    home_cmd.set_defaults(func=home)
    home_cmd.add_argument("spec", type=str, nargs=1)

    source_cmd = subparsers.add_parser(
        "source", help="Go to tool's source code"
    )
    source_cmd.set_defaults(func=source)
    source_cmd.add_argument("spec", type=str, nargs=1)

    download_cmd = subparsers.add_parser(
        "dl", help="Download Github release asset"
    )
    download_cmd.set_defaults(func=download)
    download_cmd.add_argument("repo", type=str, nargs=1)

    available_cmd = subparsers.add_parser(
        "available", help="Lookup up releases of resource"
    )
    available_cmd.set_defaults(func=available)
    available_cmd.add_argument("spec", type=str, nargs=1)

    assets_cmd = subparsers.add_parser(
        "list-assets", help="List the Github assets for a spec"
    )
    assets_cmd.set_defaults(func=list_assets)
    assets_cmd.add_argument("spec", type=str, nargs=1)

    config_cmd = subparsers.add_parser(
        "config", help="Modify the set of resources to manage on this machine"
    )
    config_cmd.set_defaults(func=config)

    subm_cmds = subparsers.add_parser(
        "subm", help="Manage git submodules"
    ).add_subparsers(title="submodule management", required=True)
    subm_cmds.add_parser("status").set_defaults(func=check_submodules)
    pull_cmd = subm_cmds.add_parser("pull")
    pull_cmd.add_argument("repo", type=str, nargs=1)
    pull_cmd.set_defaults(func=submodule_pull)
    diff_cmd = subm_cmds.add_parser("diff")
    diff_cmd.add_argument("repo", type=str, nargs=1)
    diff_cmd.set_defaults(func=submodule_diff)

    os.environ["NPM_CONFIG_USERCONFIG"] = expand("~/.config/npm/npmrc")
    os.environ["CARGO_HOME"] = expand("~/.local/share/cargo")
    os.environ["RUSTUP_HOME"] = expand("~/.local/share/rustup")
    conf.dotfiles_home = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    local_bin = expand("~/.local/bin")
    if local_bin not in os.environ["PATH"]:
        cargo_bin = expand("~/.local/share/cargo/bin")
        go_bin = expand("~/.local/go/bin")
        os.environ["PATH"] = (
            f"{local_bin}:{go_bin}:{cargo_bin}:{os.environ['PATH']}"
        )

    conf.args = argparser.parse_args()
    loglevel = LOG_LEVELS[conf.args.log]
    logging.basicConfig(
        level=loglevel, format="[%(levelname)s] %(name)s: %(message)s"
    )
    try:
        conf.args.func()
    except NoSpecError as e:
        print(f"Spec '{e.name}' not found")
