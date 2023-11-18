from typing import Optional, Tuple

from setup2.output import red, green
from setup2.process import ver_greater_than
from setup2.managers.manager import Package


def check_install(curr_ver: Optional[str], package: Package) -> Tuple[bool, str]:
    if curr_ver is None:
        return (False, red('MISSING'))

    success = ver_greater_than(curr_ver, package.version)
    color = green if success else red
    return (success, color(curr_ver))
