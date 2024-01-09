import json
import os
from typing import Dict, Any, Optional, Tuple, Type

from setup2.managers import Exe, Sym, Command, Dir, Lib, Parser, Spec
from setup2.conf import conf
from setup2.menu import show

USER_CONFIG = os.path.expanduser('~/.config/env_setup/config.json')
TYPE_MAP: Dict[str, Type[Spec]] = {
    "command": Command,
    "directory": Dir,
    "exe": Exe,
    "library": Lib,
    "parser": Parser,
    "symlink": Sym
}


def build_resources(resource: Optional[str]) -> Optional[Tuple[Any, str]]:
    with open(os.path.join(conf.dotfiles_home, 'main2.json'), encoding='utf-8') as f:
        base_spec = json.loads(f.read())
    addons = base_spec['addons']
    specs = base_spec['resources']

    choices = {}
    if os.path.exists(USER_CONFIG):
        with open(USER_CONFIG, encoding='utf-8') as f:
            choices = json.loads(f.read())['addons']
        if missing_addons := set(addons) - set(choices):
            print('There are new addons that are not tracked on this machine')
            for addon in missing_addons:
                choices[addon] = input(f'Do you want to manage addon "{addon}"'
                                       f' [y/n]?: ').lower().startswith('y')
            write_config(choices)
    else:
        print('No env config file found. Creating one...')
        choices = select_addons(addons)
        os.makedirs(os.path.dirname(USER_CONFIG), exist_ok=True)
        write_config(choices)

    for name, file in addons.items():
        if not choices[name]:
            continue
        with open(os.path.join(conf.dotfiles_home, file), encoding='utf-8') as f:
            specs.update(json.loads(f.read()))

    single_spec = None
    for name, spec in specs.items():
        if spec.get('override'):
            del spec['override']
            old_value = next(e for e in TYPE_MAP[spec.pop("type")].desired
                             if e.name == name)
            for key, value in spec.items():
                setattr(old_value, key, value)
            continue

        resource_type = spec.pop("type")
        new_item = TYPE_MAP[resource_type](name, **spec)
        if name == resource:
            single_spec = new_item, resource_type

    return single_spec


def write_config(choices: Dict[str, bool]) -> None:
    with open(USER_CONFIG, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'addons': choices}, indent=4))


def select_addons(addons: Dict[str, str]) -> Dict[str, bool]:
    print('Select which addons should be tracked on this machine')
    items = show(list(addons.keys()))
    return {i[0]: i[1] for i in items}
