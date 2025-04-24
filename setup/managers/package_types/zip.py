from logging import Logger
from os import chmod, makedirs, path
from typing import TYPE_CHECKING, Union
from zipfile import ZipFile

from setup.conf import conf
from setup.job import Job
from setup.managers.package_types.archive import find_extract_path
from setup.output import green, red
from setup.process import fetch_file, get_system

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def zip_builder(resource: "Exe") -> Union[bool, Job]:
    url = None
    for installer in resource.installers:
        if isinstance(installer, dict) and installer.get("installer") == "Zip":
            print(get_system())
            url = (installer.get("urls") or {}).get(get_system())
        elif installer == "Zip":
            url = resource.url
    if url is None:
        return False

    async def inner(logger: Logger) -> bool:
        logger.info(f"Installing {resource.name} from zip file...")
        archive_file = await fetch_file(url, resource.version)

        success = extract_zip(archive_file, resource.command_name)

        if success:
            logger.info(
                green(f"{resource.name} has been installed successfully")
            )
        else:
            logger.error(red(f"Failed to install {resource.name} from tarball"))
        return success

    return Job(
        name=resource.name,
        description=f"Install {resource.name} from zip file",
        job=inner,
    )


def extract_zip(filename: str, command_name: str) -> bool:
    if conf.root_access:
        install_home = "/usr/local"
    else:
        install_home = path.expanduser("~/.local")

    with ZipFile(filename) as archive:
        all_files = [z for z in archive.infolist() if not z.is_dir()]
        extract_path = None

        if len(all_files) == 1 and all_files[0].external_attr & (0o111 << 16):
            mode = (all_files[0].external_attr >> 16) & 0o777
            extract_path = f"{install_home}/bin"

            archive.extract(all_files[0], extract_path)
            chmod(f"{extract_path}/{all_files[0].filename}", mode)
            return True

        commonpath = path.commonpath([z.filename for z in all_files])
        commonpath = commonpath + "/" if commonpath else commonpath

        for z in all_files:
            name = z.filename.removeprefix(commonpath)
            if not name:
                continue

            if any(
                name.startswith(p) for p in ["bin", "lib", "share", "include"]
            ):
                z.filename = name
                archive.extract(z, install_home)
                continue

            filename = path.split(name)[1]
            z.filename = filename
            mode = (z.external_attr >> 16) & 0o777

            extract_path = find_extract_path(filename, mode, command_name)
            if extract_path is None:
                continue
            makedirs(extract_path, exist_ok=True)
            archive.extract(z, f"{install_home}/{extract_path}")
            if mode & 0o111:
                chmod(extract_path, mode)

        return True

    return False
