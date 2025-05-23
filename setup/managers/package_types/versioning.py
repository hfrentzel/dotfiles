from typing import Optional

from setup.managers.manager import Package
from setup.process import ver_greater_than


def check_install(
    curr_ver: Optional[str], package: Package
) -> tuple[bool, str]:
    if curr_ver is None:
        return (False, "MISSING")

    success = ver_greater_than(curr_ver, package.version)
    return (success, curr_ver)
