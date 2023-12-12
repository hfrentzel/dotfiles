import json
import os
from typing import Dict

from setup2.managers import Exe, Sym, Command, Dir, Lib, Parser
from setup2.conf import conf
from setup2.menu import show


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
    addons = config['addons']
    specs = config['resources']

    choices = {}
    config_file = os.path.expanduser('~/.config/env_setup/config.json')
    if os.path.exists(config_file):
        with open(config_file, encoding='utf-8') as f:
            choices = json.loads(f.read())['addons']
        if missing_addons := set(addons) - set(choices):
            print('There are new addons that are not tracked on this machine')
            for addon in missing_addons:
                response = input(f'Do you want to manage addon "{addon}" [y/n]?: ')
                choices[addon] = response.lower().startswith('y')
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps({'addons': choices}, indent=4))
    else:
        print('No env config file found. Creating one...')
        choices = select_addons(addons)
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps({'addons': choices}, indent=4))

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


def select_addons(addons: Dict[str, str]) -> Dict[str, bool]:
    print('Select which addons should be tracked on this machine')
    items = show(list(addons.keys()))
    return {i[0]: i[1] for i in items}
