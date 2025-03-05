import tarfile
from logging import Logger
from os import makedirs, path
from typing import TYPE_CHECKING, Optional

from setup.conf import conf
from setup.job import Job
from setup.managers.package_types.archive import find_extract_path
from setup.output import green, red
from setup.process import fetch_file

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def tar_builder(resource: "Exe") -> Job:
    async def inner(logger: Logger) -> bool:
        logger.info(f"Installing {resource.name} from tarball...")
        archive_file = await fetch_file(resource.url, resource.version)

        success = extract_tar(
            archive_file, resource.extract_path, resource.command_name
        )

        if success:
            logger.info(
                green(f"{resource.name} has been installed successfully")
            )
        else:
            logger.error(red(f"Failed to install {resource.name} from tarball"))
        return success

    return Job(
        name=resource.name,
        description=f"Install {resource.name} from tarball",
        job=inner,
    )


def extract_tar(
    filename: str, init_extract_path: Optional[str], command_name: str
) -> bool:
    if conf.root_access:
        install_home = "/usr/local"
    else:
        install_home = path.expanduser("~/.local")

    with tarfile.open(filename) as tar:
        if init_extract_path:
            tar.extractall(path.expanduser(init_extract_path))
            return True

        all_files = [t for t in tar.getmembers() if not t.isdir()]
        extract_path = None

        if len(all_files) == 1 and all_files[0].mode & 0b001001001:
            all_files[0].path = all_files[0].name.split("/")[-1]
            extract_path = f"{install_home}/bin"
            tar.extract(all_files[0], extract_path)
            return True

        # Remove common prefix from all filenames
        # TODO Use removeprefix() when python3.9 is made min version
        commonpath = path.commonpath([t.name for t in all_files])
        commonpath = commonpath + "/" if commonpath else commonpath

        for t in all_files:
            name = t.name[len(commonpath) :]
            if not name:
                continue

            if any(
                name.startswith(p) for p in ["bin", "lib", "share", "include"]
            ):
                t.path = name
                tar.extract(t, path.expanduser(install_home))
                continue

            filename = path.split(name)[1]
            t.path = filename

            extract_path = find_extract_path(filename, t.mode, command_name)
            if extract_path is None:
                continue
            full_extract_path = f"{install_home}/{extract_path}"
            makedirs(full_extract_path, exist_ok=True)
            tar.extract(t, full_extract_path)

        return True

    return False
