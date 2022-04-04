import os
import sys
from pip._internal.operations.freeze import freeze
from pkg_resources import parse_version as parse

prompt = os.getenv('PYPROMPT', '>>')
sys.ps1 = prompt + '> '


def ch():
    sys.exit(5)


class Pip(object):

    @staticmethod
    def freeze():
        print(Pip.get_freeze())

    @staticmethod
    def get_freeze():
        curr_installed = {(p := pv.split('=='))[0].lower(): p[1]
                          for pv in freeze() if '==' in pv}
        return curr_installed


if 'venv' in sys.executable:
    os.chdir(f'{sys.executable}\\..\\..\\..')


def get_requirements(filename, reqs):
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('-r'):
                get_requirements(line[:-1].split('  ')[1], reqs)
            elif line.startswith('git+'):
                continue
            else:
                parsed = line[:-1].split('==')
                if len(parsed) == 2:
                    reqs[parsed[0]] = parsed[1]
                else:
                    reqs[parsed[0]] = None


reqs = {}
if os.path.exists('requirements.txt'):
    get_requirements('requirements.txt', reqs)
    curr_installed = Pip.get_freeze()
    not_installed = []
    out_of_date = []
    for package, version in reqs.items():
        if package not in curr_installed.keys():
            not_installed.append(package)
        elif version and parse(curr_installed[package]) < parse(version):
            out_of_date.append(package)

    if out_of_date:
        print('The following modules packages are out of date:')
        print(', '.join(out_of_date))
    if not_installed:
        print('The following modules are not installed')
        print(', '.join(not_installed))
