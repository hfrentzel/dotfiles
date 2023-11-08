import tarfile
from os import path

from .conf import conf
from .jobs import async_proc
from .job import Job
from .output import red, green

class Tar():

    @classmethod
    def tar_builder(cls, spec):
        async def inner():
            try:
                print(f'Installing {spec["name"]} from tarball...' )
                filename = await fetch_file(spec['url'], spec['version'])

                tar = tarfile.open(filename)
                all_files = [t for t in tar.getmembers() if not t.isdir()]
                # TODO handle when there's just one file

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
                        tar.extract(t, path.expanduser('~/.local'))
                    else:
                        pass
                        # TODO handle cases where files are organized in standard
            except:
                print(red(f'Failed to install {spec["name"]} from tarball'))
                return False

            print(green(f'{spec["name"]} has been installed successfully'))
            return True

        return Job(names=[spec['name']],
                   description=f'Install {spec["name"]} from tarball',
                   job=inner)


async def fetch_file(url, version):
    full_url = url.format(version=version)
    _, file = path.split(full_url)

    filename = f'{conf.sources_dir}/{file}'
    await async_proc(f'curl -L {full_url} -o {filename}')

    return filename
