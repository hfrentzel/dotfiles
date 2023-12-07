import json
import os

from setup2.managers import Exe, Sym, Command, Dir, Lib, Parser
from setup2.conf import conf


TYPE_MAP = {
    "command": Command,
    "directory": Dir,
    "exe": Exe,
    "library": Lib,
    "parser": Parser,
    "symlink": Sym
}


def build_resources() -> None:
    with open(os.path.join(conf.dotfiles_home, 'main2.json'), encoding='utf-8') as f:
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
        with open(os.path.join(conf.dotfiles_home, file), encoding='utf-8') as f:
            specs.update(json.loads(f.read()))

    for name, spec in specs.items():
        if spec.get('override'):
            del spec['override']
            old_value = next(e for e in TYPE_MAP[spec.pop("type")].desired
                             if e.name == name)
            for key, value in spec.items():
                setattr(old_value, key, value)
            continue
        resource_type = TYPE_MAP[spec.pop("type")]
        resource_type(name, **spec)
