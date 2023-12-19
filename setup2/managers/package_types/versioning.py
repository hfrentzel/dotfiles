from typing import Optional, Tuple

from setup2.process import ver_greater_than
from setup2.managers.manager import Package


def check_install(curr_ver: Optional[str], package: Package) -> Tuple[bool, str]:
    if curr_ver is None:
        return (False, 'MISSING')

    success = ver_greater_than(curr_ver, package.version)
    return (success, curr_ver)
