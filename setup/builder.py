import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from setup.conf import conf
from setup.managers import ALL_MANAGERS, Manager
from setup.menu import MenuPiece, show
from setup.output import green, red

USER_CONFIG = os.path.expanduser("~/.config/env_setup/config.json")


class NoSpecError(Exception):
    def __init__(self, name: str) -> None:
        self.name = name


def build_resources(types: List[str]) -> List[Manager]:
    specs = collect_specs()
    all_resources = []
    for name, spec in specs.items():
        if spec.get("type") not in types:
            continue
        all_resources.append(generate_resource(name, spec))

    return all_resources


def get_resource(name: str) -> Manager:
    return generate_resource(name, get_spec(name))


def generate_resource(name: str, spec: Dict[str, Any]) -> Manager:
    resource_type = spec.pop("type")

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
    specs, addons = get_base_specs()

    choices, external_addons = load_settings(addons)
    for name, file in addons.items():
        if not include_all and not choices[name]:
            continue
        specs.update(get_addon_specs(file))

    for e_addon in external_addons:
        specs.update(get_addon_specs(e_addon))

    return specs


def get_spec(name: str) -> Dict[str, Any]:
    specs, addons = get_base_specs()
    if name in specs:
        return specs[name]

    for file in addons.values():
        addons_specs = get_addon_specs(file)
        if name in addons_specs:
            return addons_specs[name]
    raise NoSpecError(name)


def get_base_specs() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    with open(
        os.path.join(conf.dotfiles_home, "main.json"), encoding="utf-8"
    ) as f:
        base_spec = json.loads(f.read())
    addons = base_spec["addons"]
    specs = base_spec["resources"]

    return specs, addons


def get_addon_specs(addon: str) -> Dict[str, Dict[str, Any]]:
    with open(os.path.join(conf.dotfiles_home, addon), encoding="utf-8") as f:
        return json.loads(f.read())


def load_settings(
    addons: Dict[str, str],
) -> Tuple[Dict[str, bool], List[str]]:
    choices, external_addons = read_config()
    if choices is not None:
        if missing_addons := set(addons) - set(choices):
            print("There are new addons that are not tracked on this machine")
            for addon in missing_addons:
                choices[addon] = (
                    input(f'Do you want to manage addon "{addon}" [y/n]?: ')
                    .lower()
                    .startswith("y")
                )
            write_config(choices, external_addons)
        return choices, external_addons

    print("No config file found. Creating one...")
    choices = select_addons([(a, True) for a in addons])
    os.makedirs(os.path.dirname(USER_CONFIG), exist_ok=True)
    write_config(choices)

    return choices, []


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


def read_config() -> Tuple[Optional[Dict[str, bool]], List[str]]:
    if not os.path.exists(USER_CONFIG):
        return None, []
    with open(USER_CONFIG, encoding="utf-8") as f:
        config_options = json.loads(f.read())
        choices = config_options["addons"]
        external_addons = config_options.get("external") or []
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


class ConfigEditor(MenuPiece):
    def __init__(self, addons: List[Tuple[str, bool]]):
        self.addons = addons

    def get(self, index: int) -> str:
        item = self.addons[index]
        state = green("INCLUDE") if item[1] else red("EXCLUDE")
        return f"{item[0]: <15}{state}"

    def len(self) -> int:
        return len(self.addons)

    @staticmethod
    def keys() -> List[str]:
        return ["enter"]

    def action(self, key: str, index: int) -> bool:
        self.addons[index] = (self.addons[index][0], not self.addons[index][1])
        return False


def select_addons(preferences: List[Tuple[str, bool]]) -> Dict[str, bool]:
    print("Select which addons should be tracked on this machine")
    prefs = ConfigEditor(preferences)
    show(prefs)
    return {i[0]: i[1] for i in prefs.addons}
