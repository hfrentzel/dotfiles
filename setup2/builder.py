import json
import os

from setup2 import Exe, Sym, Command, Dir, Lib, Parser


TYPE_MAP = {
    "command": Command,
    "directory": Dir,
    "exe": Exe,
    "library": Lib,
    "parser": Parser,
    "symlink": Sym
}


def build_resources() -> None:
    with open('main2.json', encoding='utf-8') as f:
        config = json.loads(f.read())

    choices = {}
    # TODO handle case where config file doesn't exist
    if os.path.exists(p := os.path.expanduser('~/.config/env_setup/config.json')):
        with open(p, encoding='utf-8') as f:
            choices = json.loads(f.read())['addons']

    addons = config['addons']
    specs = config['resources']

    for name, file in addons.items():
        if not choices.get(name, True):
            continue
        with open(file, encoding='utf-8') as f:
            specs.update(json.loads(f.read()))

    for name, spec in specs.items():
        resource_type = TYPE_MAP[spec.pop("type")]
        resource_type(name, **spec)
