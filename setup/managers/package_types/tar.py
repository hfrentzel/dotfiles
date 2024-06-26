import tarfile
from os import makedirs, path

from setup.conf import conf
from setup.job import Job
from setup.managers.exe_class import Exe
from setup.managers.package_types.archive import find_extract_path
from setup.output import green, red
from setup.process import fetch_file


def tar_builder(spec: Exe, _: str = "") -> Job:
    async def inner() -> bool:
        if conf.root_access:
            install_home = "/usr/local"
        else:
            install_home = path.expanduser("~/.local")

        print(f"Installing {spec.name} from tarball...")
        archive_file = await fetch_file(spec.url, spec.version)
        with tarfile.open(archive_file) as tar:
            if spec.extract_path:
                tar.extractall(path.expanduser(spec.extract_path))
                print(green(f"{spec.name} has been installed successfully"))
                return True

            all_files = [t for t in tar.getmembers() if not t.isdir()]
            extract_path = None

            if len(all_files) == 1 and all_files[0].mode & 0b001001001:
                extract_path = f"{install_home}/bin"
                tar.extract(all_files[0], extract_path)
                print(green(f"{spec.name} has been installed successfully"))
                return True

            # Remove common prefix from all filenames
            # TODO Use removeprefix() when python3.9 is made min version
            commonpath = path.commonpath([t.name for t in all_files])
            commonpath = commonpath + "/" if commonpath else commonpath

            for t in all_files:
                name = t.name[len(commonpath) :]
                if not name:
                    continue

                if any(name.startswith(p) for p in ["bin", "lib", "share", "include"]):
                    t.path = name
                    tar.extract(t, path.expanduser(install_home))
                    continue

                filename = path.split(name)[1]
                t.path = filename

                extract_path = find_extract_path(filename, t.mode, spec.command_name)
                if extract_path is None:
                    continue
                full_extract_path = f"{install_home}/{extract_path}"
                makedirs(full_extract_path, exist_ok=True)
                tar.extract(t, full_extract_path)

            print(green(f"{spec.name} has been installed successfully"))
            return True

        print(red(f"Failed to install {spec.name} from tarball"))
        return False

    return Job(
        names=[spec.name],
        description=f"Install {spec.name} from tarball",
        on_demand=spec.on_demand,
        job=inner,
    )
