from typing import Type
from .manager import Manager
from .apt import Apt
from .pip import Pip
from .npm import Npm

all_managers: dict[str, Type[Manager]] = {
    'apt': Apt,
    'npm': Npm,
    'pip': Pip
}
