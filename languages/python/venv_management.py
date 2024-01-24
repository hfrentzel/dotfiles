#! /usr/bin/python
"""
A collection of utility functions to help manage venvs and python
interpreters
"""
import os
import subprocess
import sys
import venv
import shutil

from itertools import zip_longest

venv_file = os.path.expanduser('~/.local/share/python/python_venvs')


def _get_existing() -> dict:
    if not os.path.isfile(venv_file):
        return {}

    existing_venvs = {}
    with open(venv_file, encoding='utf-8') as f:
        for line in f.readlines():
            name, location = line.strip().split(' ')
            existing_venvs[name] = location

    return existing_venvs


def pymake(new_venv, directory):
    """
    Create a new venv and add it to the list
    """
    existing_venvs = _get_existing()

    if new_venv in existing_venvs:
        print(f'Venv named {new_venv} already exists')
        return

    if directory in existing_venvs.values():
        print('Venv already exists in this directory and is tracked')
        return

    if os.path.isdir(directory):
        print('Venv exists in this directory, but is not tracked.')
        print('Adding venv to ~/.python_venvs')

    venv.create(directory, prompt=new_venv, with_pip=True)
    existing_venvs[new_venv] = directory

    with open(venv_file, 'w', encoding='utf-8') as f:
        for name, location in existing_venvs.items():
            f.write(f'{name} {location}\n')


def pyrun(venv_name=None):
    """
    Run a venv
    """
    existing_venvs = _get_existing()
    if not existing_venvs:
        print('No available python environments')
        return

    if venv_name is not None:
        if venv_name not in existing_venvs:
            print(f'No venv named {venv_name} found')
        cmd = existing_venvs[venv_name]
        prompt = venv_name
    else:
        options = [(f'{idx}. {name}   ', location)
                   for idx, (name, location)
                   in enumerate(existing_venvs.items(), 1)]

        col_length = max(len(x[0]) for x in options)
        num_columns = int(80 / col_length)

        for column in zip_longest(*[iter(options)] * num_columns):
            for row in column:
                if row:
                    print(row[0], end='')
            print()

        choice = input('Please select a venv: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Error, input was not a number')
            return

        if choice > len(options) or choice < 1:
            print('Error, invalid option')
            return

        cmd = location = options[choice - 1][1]
        prompt = [a for a, b in existing_venvs.items()
                  if b == location][0]

    if 'venv' in cmd:
        cmd = os.path.join(cmd, 'bin', 'python')

    os.environ['PYPROMPT'] = prompt
    subprocess.run(cmd, check=False)


def pykill(name):
    """
    Delete an existing venv
    """
    existing_venvs = _get_existing()
    if name not in existing_venvs:
        print(f"Could not find venv '{name}'")
        return

    shutil.rmtree(existing_venvs[name])
    del existing_venvs[name]

    with open(venv_file, 'w', encoding='utf-8') as f:
        for n, location in existing_venvs.items():
            f.write(f'{n} {location}\n')

    print(f"'{name}' deleted")


def main():
    """
    Main
    """
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None

    os.makedirs(os.path.expanduser('~/.local/share/python'), exist_ok=True)
    if cmd == 'pymake':
        if arg is None:
            print('Please enter a name for the new venv')
            return
        pymake(sys.argv[2], os.path.join(os.getcwd(), 'venv'))
    elif cmd == 'pyrun':
        pyrun(arg)
    elif cmd == 'pykill':
        if arg is None:
            print('Please enter a venv to be deleted')
            return
        pykill(sys.argv[2])


if __name__ == '__main__':
    main()
