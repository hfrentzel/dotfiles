from logging import Logger
from os import chmod, makedirs, path
from typing import TYPE_CHECKING
from zipfile import ZipFile

from setup.conf import conf
from setup.job import Job
from setup.managers.package_types.archive import find_extract_path
from setup.output import green, red
from setup.process import fetch_file

if TYPE_CHECKING:
    from setup.managers.exe import Exe


def zip_builder(spec: "Exe", _: str = "") -> Job:
    async def inner(logger: Logger) -> bool:
        if conf.root_access:
            install_home = "/usr/local"
        else:
            install_home = path.expanduser("~/.local")

        logger.info(f"Installing {spec.name} from zip file...")
        archive_file = await fetch_file(spec.url, spec.version)
        with ZipFile(archive_file) as archive:
            all_files = [z for z in archive.infolist() if not z.is_dir()]
            extract_path = None

            if len(all_files) == 1 and all_files[0].external_attr & (
                0o111 << 16
            ):
                mode = (all_files[0].external_attr >> 16) & 0o777
                extract_path = f"{install_home}/bin"

                archive.extract(all_files[0], extract_path)
                chmod(f"{extract_path}/{all_files[0].filename}", mode)

                logger.info(green(f"{spec.name} has been installed successfully"))
                return True

            # Remove common prefix from all filenames
            # TODO Use removeprefix() when python3.9 is made min version
            commonpath = path.commonpath([z.filename for z in all_files])
            commonpath = commonpath + "/" if commonpath else commonpath

            for z in all_files:
                name = z.filename[len(commonpath) :]
                if not name:
                    continue

                if any(
                    name.startswith(p)
                    for p in ["bin", "lib", "share", "include"]
                ):
                    z.filename = name
                    archive.extract(z, install_home)
                    continue

                filename = path.split(name)[1]
                z.filename = filename
                mode = (z.external_attr >> 16) & 0o777

                extract_path = find_extract_path(
                    filename, mode, spec.command_name
                )
                if extract_path is None:
                    continue
                makedirs(extract_path, exist_ok=True)
                archive.extract(z, f"{install_home}/{extract_path}")
                if mode & 0o111:
                    chmod(extract_path, mode)

            logger.info(green(f"{spec.name} has been installed successfully"))
            return True

        logger.error(red(f"Failed to install {spec.name} from zip file"))
        return False

    return Job(
        name=spec.name,
        description=f"Install {spec.name} from zip file",
        job=inner,
    )
