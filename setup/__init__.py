import argparse
import asyncio
import datetime
import json
import logging
import os
import webbrowser
from typing import List, Type

from .available import lookup_releases
from .builder import (
    NoSpecError,
    build_resources,
    edit_config,
    get_resource,
    get_spec,
)
from .conf import conf
from .inspect import search_assets
from .job import print_job_tree
from .managers import (
    ALL_MANAGERS,
    Exe,
    Manager,
    all_desired,
    create_bonus_jobs,
    create_jobs,
)
from .output import green, red
from .process import OutputTracker
from .tree import build_tree


async def handle_jobs(
    resources: List[Manager], selected_types: List[Type[Manager]]
) -> None:
    logger = logging.getLogger("mysetup")
    if conf.args.stage == "desired":
        for t in selected_types:
            print(t.desired_printout(), end="")
        return

    all_complete = await asyncio.gather(*[r.get_status() for r in resources])
    complete = [r.name for r, c in zip(resources, all_complete) if c]
    if conf.args.stage in {None, "show_all"}:
        for t in selected_types:
            print(t.status_printout(bool(conf.args.stage)), end="")
        return

    jobs = create_jobs(resources)
    if len(jobs) == 0:
        logger.info("No jobs to run. All resources are setup")
        return

    if conf.args.stage == "jobs":
        for m in jobs.values():
            print(m.description)
        return

    root_jobs = await build_tree(jobs, complete)
    if conf.args.stage == "tree":
        print_job_tree(root_jobs)
        return

    filename = f"{datetime.datetime.now().isoformat()}_output.txt"
    filename = os.path.expanduser(f"~/.local/share/mysetup/log/{filename}")
    try:
        success = all(await asyncio.gather(*[job.run() for job in root_jobs]))
    except Exception as e:
        success = False
        raise e
    finally:
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

    if job.depends_on is not None:
        if not any(d.name in job.depends_on for d in all_desired()):
            dependency = get_resource(job.depends_on[0])
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
    resource = get_resource(conf.args.spec[0])
    if isinstance(resource, Exe):
        asyncio.run(search_assets(resource))


def config() -> None:
    edit_config()


def available() -> None:
    spec = get_spec(conf.args.spec[0])
    lookup_releases(spec)


def run() -> None:
    argparser = argparse.ArgumentParser(prog="EnvSetup")
    argparser.set_defaults(func=check)
    argparser.add_argument(
        "-l",
        "--log",
        choices=["debug", "info", "error", "warn"],
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

    os.environ["NPM_CONFIG_USERCONFIG"] = os.path.expanduser(
        "~/.config/npm/npmrc"
    )
    conf.dotfiles_home = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    local_bin = os.path.expanduser("~/.local/bin")
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] += ":" + local_bin

    conf.args = argparser.parse_args()
    loglevel = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }[conf.args.log]
    logging.basicConfig(
        level=loglevel, format="[%(levelname)s] %(name)s: %(message)s"
    )
    try:
        conf.args.func()
    except NoSpecError as e:
        print(f"Spec '{e.name}' not found")
