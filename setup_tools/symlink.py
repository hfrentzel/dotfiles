import os
from setup_tools.config import config

_symlinks = []


def symlink(src, dest):
    _symlinks.append((src, dest))


def _add_symlink(src: str, dest: str) -> bool:
    src = os.path.expanduser(src)
    dest = os.path.expanduser(dest)
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            if config.verbose:
                print(f'{dest} already exists and is a link')
            return True
        print(f'Error. {dest} already exists')
        return False

    if config.dry_run:
        return False

    print(f'{dest} does not exist. Creating symlink...')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    os.symlink(src, dest)
    return False


def execute_symlinks(dotfiles_home):
    if all(_add_symlink(src.replace('DOTROOT', dotfiles_home), dest) for
           (src, dest) in _symlinks):
        print('All symlinks up to date')
