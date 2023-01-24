import os

from setup_tools.config import config

_symlinks = []


def add_symlink(src, dest):
    src = os.path.expanduser(src)
    dest = os.path.expanduser(dest)
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            print(f'{dest} already exists and is a link')
        else:
            print(f'Error. {dest} already exists')
        return

    if config['dry_run']:
        return

    print(f'{dest} does not exist. Creating symlink...')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    os.symlink(src, dest)


def symlink(src, dest):
    _symlinks.append((src, dest))


def execute_symlinks(dotfiles_home):
    for src, dest in _symlinks:
        add_symlink(src.replace('DOTROOT', dotfiles_home), dest)
