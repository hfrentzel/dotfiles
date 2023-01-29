from typing import Type
from .manager import Manager
from .apt import Apt
from .pip import Pip
from .npm import Npm
from .deb import Deb
from .symlink import Symlink

all_managers: dict[str, Type[Manager]] = {
    'apt': Apt,
    'deb': Deb,
    'npm': Npm,
    'pip': Pip,
    'symlink': Symlink
}
