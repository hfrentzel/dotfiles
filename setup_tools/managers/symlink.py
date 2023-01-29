import os
from setup_tools.config import config
from setup_tools.managers.manager import Manager


class Symlink(Manager):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self._requested.add(self)

    @classmethod
    def _add_symlink(cls, src: str, dest: str) -> bool:
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

    @classmethod
    async def update(cls):
        if all(cls._add_symlink(sym.src.replace('DOTROOT', config.dotfiles_home),
                                sym.dest) for sym in cls._requested):
            print('All symlinks up to date')
        return True
