import atexit
import os
import sys
from pip._internal.operations.freeze import freeze
from pkg_resources import parse_version as parse

try:
    import readline
    try:
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass

    if hasattr(sys, '__interactivehook__'):
        del sys.__interactivehook__

    histfile = os.path.expanduser("~/.local/share/python/history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)
    atexit.register(os.makedirs, os.path.dirname(histfile), exist_ok=True)
except ImportError:
    pass

if prompt := os.getenv('PYPROMPT', None):
    sys.ps1 = prompt + '> '
else:
    sys.ps1 = f'py{sys.version_info[0]}.{sys.version_info[1]}> '
sys.ps2 = '.' * (len(sys.ps1) - 1) + ' '


class Quitter:
    def __init__(self, num=0):
        self.num = num

    def __repr__(self):
        sys.exit(self.num)


ch = Quitter(5)
q = Quitter()
exit = q


class Pip:

    @staticmethod
    def freeze():
        print(Pip.get_freeze())

    @staticmethod
    def get_freeze():
        # installed_packages = {(p := pv.split('=='))[0].lower(): p[1] for pv in freeze() if '==' in pv}
        installed_packages = {}
        for pv in freeze():
            if '==' in pv:
                p = pv.split('==')
                installed_packages[p[0].lower()] = p[1]

        return installed_packages


def get_requirements(filename, desired):
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('-r'):
                get_requirements(line[:-1].split(' ')[1], desired)
            elif line.startswith('git+'):
                continue
            else:
                parsed = line[:-1].split('==')
                if len(parsed) == 2:
                    desired[parsed[0]] = parsed[1]
                else:
                    desired[parsed[0]] = None


if 'venv' in sys.executable:
    os.chdir(os.path.join(os.path.dirname(sys.executable), '..', '..'))

    reqs: dict = {}
    if os.path.exists('requirements.txt'):
        get_requirements('requirements.txt', reqs)
        curr_installed = Pip.get_freeze()
        not_installed = []
        out_of_date = []
        for package, version in reqs.items():
            if package not in curr_installed:
                not_installed.append(package)
            elif version and parse(curr_installed[package]) < parse(version):
                out_of_date.append(package)

        if out_of_date:
            print('The following modules packages are out of date:')
            print(', '.join(out_of_date))
        if not_installed:
            print('The following modules are not installed')
            print(', '.join(not_installed))
        if not (out_of_date or not_installed):
            print('All packages are up to date.')
