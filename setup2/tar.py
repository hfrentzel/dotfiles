import tarfile
from os import path, makedirs

from .jobs import fetch_file
from .job import Job
from .output import red, green


class Tar():

    @classmethod
    def tar_builder(cls, spec):
        async def inner():
            if conf.root_access:
                install_home = '/usr/local'
            else:
                install_home = path.expanduser('~/.local')
            try:
                print(f'Installing {spec["name"]} from tarball...' )
                archive_file = await fetch_file(spec['url'], spec['version'])

                tar = tarfile.open(archive_file)
                all_files = [t for t in tar.getmembers() if not t.isdir()]

                if len(all_files) == 1 and all_files[0].mode & 0b001001001:
                    dir = f'{install_home}/bin'
                    tar.extract(all_files[0], dir)
                    print(green(f'{spec["name"]} has been installed successfully'))
                    return True

                # Remove common prefix from all filenames
                # TODO Use removeprefix() when python3.9 is made min version
                commonpath = path.commonpath([t.name for t in all_files])
                commonpath = commonpath + '/' if commonpath != '' else commonpath

                for t in all_files:
                    name = t.name[len(commonpath):]
                    if name == '':
                        continue

                    if any(name.startswith(p) for p in ['bin', 'lib', 'share', 'include']):
                        t.path = name
                        tar.extract(t, path.expanduser(install_home))
                        continue

                    filename = path.split(name)[1]
                    extension = path.splitext(filename)[1]
                    t.path = filename
                    if extension in ['.ps1', '.zsh', '.fish']:
                        continue

                    if extension == '.bash':
                        dir = f'{install_home}/share/bash-completion/completions'
                    elif extension in ['.1', '.5']:
                        man = extension.replace('.', 'man')
                        dir = f'{install_home}/share/man/{man}'
                    elif extension in ['.md', '.txt']:
                        dir = f'{install_home}/share/doc/{spec["command_name"]}'
                    elif extension == '':
                        if t.mode & 0b001001001:
                            dir = f'{install_home}/bin'
                        else:
                            dir = f'{install_home}/share/doc/{spec["command_name"]}'
                    else:
                        continue
                    makedirs(dir, exist_ok=True)
                    tar.extract(t, dir)

            except Exception:
                print(red(f'Failed to install {spec["name"]} from tarball'))
                return False
            finally:
                tar.close()

            print(green(f'{spec["name"]} has been installed successfully'))
            return True

        return Job(names=[spec['name']],
                   description=f'Install {spec["name"]} from tarball',
                   job=inner)
