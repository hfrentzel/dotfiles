import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from setup.conf import conf
from setup.managers import ALL_MANAGERS, Manager
from setup.menu import show

USER_CONFIG = os.path.expanduser("~/.config/env_setup/config.json")


def build_resources(resource: Optional[str], types: List[str]) -> List[Manager]:
    specs = collect_specs()

    if resource is not None:
        return [generate_resource(resource, specs[resource])]

    all_resources = []
    for name, spec in specs.items():
        if spec.get("type") not in types:
            continue
        all_resources.append(generate_resource(name, spec))

    return all_resources


def generate_resource(name: str, spec: Dict[str, Any]) -> Manager:
    resource_type = spec.pop("type")

    if spec.get("override"):
        del spec["override"]
        old_value = next(
            e for e in ALL_MANAGERS[resource_type].desired if e.name == name
        )
        for key, value in spec.items():
            setattr(old_value, key, value)
        return old_value

    args = {}
    for key, value in spec.items():
        if key == "source_repo":
            if "github.com" in value and "Github" in spec.get("installers", []):
                match = re.search(r"(?:https?://)?github.com/(\S+)", value)
                if match:
                    args["repo"] = match.group(1)
            elif "gitlab.com" in value and "Gitlab" in spec.get(
                "installers", []
            ):
                match = re.search(r"(?:https?://)?gitlab.com/(\S+)", value)
                if match:
                    args["repo"] = match.group(1)
        elif key == "homepage":
            continue
        else:
            args[key] = value

    return ALL_MANAGERS[resource_type](name, **args)


def collect_specs(include_all: bool = False) -> Dict[str, Dict[str, Any]]:
    with open(
        os.path.join(conf.dotfiles_home, "main.json"), encoding="utf-8"
    ) as f:
        base_spec = json.loads(f.read())
    addons = base_spec["addons"]
    specs: Dict[str, Dict[str, Any]] = base_spec["resources"]

    choices, external_addons = load_settings(addons)

    for name, file in addons.items():
        if not include_all and not choices[name]:
            continue
        specs.update(get_addon_specs(file))

    for e_addon in external_addons or []:
        with open(os.path.expanduser(e_addon), encoding="utf-8") as f:
            specs.update(json.loads(f.read()))

    return specs


def load_settings(
    addons: Dict[str, str],
) -> Tuple[Dict[str, bool], Optional[List[str]]]:
    choices, external_addons = read_config()
    if choices is not None:
        if missing_addons := set(addons) - set(choices):
            print("There are new addons that are not tracked on this machine")
            for addon in missing_addons:
                choices[addon] = (
                    input(f'Do you want to manage addon "{addon}"' f" [y/n]?: ")
                    .lower()
                    .startswith("y")
                )
            write_config(choices, external_addons)
        return choices, external_addons

    print("No config file found. Creating one...")
    choices = select_addons([(a, True) for a in addons])
    os.makedirs(os.path.dirname(USER_CONFIG), exist_ok=True)
    write_config(choices)

    return choices, None


def edit_config() -> None:
    with open(
        os.path.join(conf.dotfiles_home, "main.json"), encoding="utf-8"
    ) as f:
        base_spec = json.loads(f.read())
    addons = base_spec["addons"]

    choices, external = read_config()
    if choices is None:
        choices = addons.fromkeys(addons, True)
    elif missing_addons := set(addons) - set(choices):
        for addon in missing_addons:
            choices[addon] = True

    choices = select_addons(list(choices.items()))
    os.makedirs(os.path.dirname(USER_CONFIG), exist_ok=True)
    write_config(choices, external)


def read_config() -> Tuple[Optional[Dict[str, bool]], Optional[List[str]]]:
    if not os.path.exists(USER_CONFIG):
        return None, None
    with open(USER_CONFIG, encoding="utf-8") as f:
        config_options = json.loads(f.read())
        choices = config_options["addons"]
        external_addons = config_options.get("external")
    return choices, external_addons


def write_config(
    choices: Dict[str, bool], external_addons: Optional[List[str]] = None
) -> None:
    with open(USER_CONFIG, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {"addons": choices, "external": external_addons}, indent=4
            )
        )


def select_addons(preferences: List[Tuple[str, bool]]) -> Dict[str, bool]:
    print("Select which addons should be tracked on this machine")
    items = show(preferences)
    return {i[0]: i[1] for i in items}
