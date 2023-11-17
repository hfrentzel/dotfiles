from zipfile import ZipFile
from os import path, makedirs, chmod

from .conf import conf
from .jobs import fetch_file
from .job import Job
from .output import red, green


class Zip():

    @classmethod
    def zip_builder(cls, spec):
        async def inner():
            if conf.root_access:
                install_home = '/usr/local'
            else:
                install_home = path.expanduser('~/.local')
            try:
                print(f'Installing {spec["name"]} from zip file...')
                archive_file = await fetch_file(spec['url'], spec['version'])

                zip = ZipFile(archive_file)
                all_files = [z for z in zip.infolist() if not z.is_dir()]

                if len(all_files) == 1 and all_files[0].external_attr & (0o111 << 16):
                    mode = (all_files[0].external_attr >> 16) & 0o777
                    dir = f'{install_home}/bin'

                    zip.extract(all_files[0], dir)
                    chmod(f'{dir}/{all_files[0].filename}', mode)

                    print(green(f'{spec["name"]} has been installed successfully'))
                    return True

                # Remove common prefix from all filenames
                # TODO Use removeprefix() when python3.9 is made min version
                commonpath = path.commonpath([z.filename for z in all_files])
                commonpath = commonpath + '/' if commonpath != '' else commonpath

                for z in all_files:
                    name = z.filename[len(commonpath):]
                    if name == '':
                        continue

                    if any(name.startswith(p) for p in ['bin', 'lib', 'share', 'include']):
                        z.filename = name
                        zip.extract(z, install_home)
                        continue

                    filename = path.split(name)[1]
                    extension = path.splitext(filename)[1]
                    z.filename = filename
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
                        filemode = (z.external_attr >> 16) & 0o777
                        if filemode & 0o111: 
                            dir = f'{install_home}/bin'
                            chmod(f'{dir}/{filename}', filemode)
                        else:
                            dir = f'{install_home}/share/doc/{spec["command_name"]}'
                    else:
                        continue
                    makedirs(dir, exist_ok=True)
                    zip.extract(z, dir)

            except Exception:
                print(red(f'Failed to install {spec["name"]} from zip file'))
                return False
            finally:
                zip.close()

            print(green(f'{spec["name"]} has been installed successfully'))
            return True

        return Job(names=[spec['name']],
                   description=f'Install {spec["name"]} from zip file',
                   job=inner)
