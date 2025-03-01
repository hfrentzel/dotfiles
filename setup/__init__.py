import argparse
import asyncio
import itertools
import json
import logging
import os
import webbrowser
from typing import List, Type

from .available import lookup_releases
from .builder import (
    build_resources,
    collect_specs,
    edit_config,
    generate_resource,
)
from .conf import conf
from .inspect import search_assets
from .job import build_tree, print_job_tree
from .managers import (
    ALL_MANAGERS,
    Manager,
    all_desired,
    create_bonus_jobs,
    create_jobs,
)
from .output import green, red


async def handle_jobs(selected_types: List[Type[Manager]]) -> None:
    logger = logging.getLogger("mysetup")
    if conf.args.stage == "desired":
        for t in selected_types:
            print(t.desired_printout(), end="")
        return

    all_complete = await asyncio.gather(*[
        t.get_statuses() for t in selected_types
    ])
    complete = list(itertools.chain.from_iterable(all_complete))
    if conf.args.stage in {None, "show_all"}:
        for t in selected_types:
            print(t.status_printout(bool(conf.args.stage)), end="")
        return

    jobs = create_jobs(selected_types)
    if len(jobs) == 0:
        logger.info("No jobs to run. All resources are setup")
        return

    if conf.args.stage == "jobs":
        for m in jobs.values():
            print(m.description)
        return

    root_jobs = build_tree(jobs, complete)
    if conf.args.stage == "tree":
        print_job_tree(root_jobs)
        return

    if all(await asyncio.gather(*[job.run() for job in root_jobs])):
        logger.info(green("All resources have been setup successfully"))
    else:
        logger.error(
            red("Not all jobs were successful. Check logs for details")
        )


async def handle_single_resource(resource: Manager, resource_type: str) -> None:
    await resource.set_status()
    if resource.state[0]:
        print(f"{resource.name} is already set up")
        return

    job = (
        ALL_MANAGERS[resource_type].create_job(resource)
        or list(create_bonus_jobs().values())[0]
    )

    if job.depends_on is not None:
        if not any(d.name == job.depends_on for d in all_desired()):
            build_resources(job.depends_on)
        all_complete = await asyncio.gather(*[
            t.get_statuses() for t in ALL_MANAGERS.values()
        ])
        complete = list(itertools.chain.from_iterable(all_complete))

        if remaining := {job.depends_on} - set(complete):
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
    resource = build_resources(conf.args.only)
    if resource:
        asyncio.run(handle_single_resource(*resource))
        return

    selected_types = []
    if conf.args.types is None:
        selected_types = list(ALL_MANAGERS.values())
    else:
        for t in conf.args.types:
            selected_types.append(ALL_MANAGERS[t])
    asyncio.run(handle_jobs(selected_types))


def show() -> None:
    specs = collect_specs(include_all=True)
    if (spec := conf.args.spec[0]) in specs:
        print(json.dumps({spec: specs[spec]}, indent=4))
    else:
        print(f"Spec '{spec}' not found")


def home() -> None:
    specs = collect_specs(include_all=True)
    spec = conf.args.spec[0]
    if spec not in specs:
        print(f"Spec '{spec}' not found")
        return

    if home_url := specs[spec].get("homepage"):
        webbrowser.open(home_url)
    elif source_url := specs[spec].get("source_repo"):
        webbrowser.open(source_url)
    else:
        print(f"No home page listed for '{spec}'")
        return


def source() -> None:
    specs = collect_specs(include_all=True)
    spec = conf.args.spec[0]
    if spec not in specs:
        print(f"Spec '{spec}' not found")
        return

    if source_url := specs[spec].get("source_repo"):
        webbrowser.open(source_url)
    else:
        print(f"No source repository listed for '{spec}'")
        return


def list_assets() -> None:
    specs = collect_specs(include_all=True)
    resource, _ = generate_resource(conf.args.spec[0], specs[conf.args.spec[0]])
    asyncio.run(search_assets(resource))


def config() -> None:
    edit_config()


def available() -> None:
    specs = collect_specs(include_all=True)
    spec = conf.args.spec[0]
    if spec not in specs:
        print(f"Spec '{spec}' not found")
        return

    lookup_releases(specs[spec])


def run() -> None:
    argparser = argparse.ArgumentParser(prog="EnvSetup")
    argparser.set_defaults(func=check)
    argparser.add_argument("-l", "--log", choices=['debug', 'info', 'error',
                                                   'warn'], default='info')

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

    conf.args = argparser.parse_args()
    loglevel = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
    }[conf.args.log]
    logging.basicConfig(
        level=loglevel, format="[%(levelname)s] %(name)s: %(message)s"
    )
    conf.args.func()
