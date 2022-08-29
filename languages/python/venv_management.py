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

venv_file = os.path.expanduser('~/.python_venvs')


def _get_existing() -> dict:
    if not os.path.isfile(venv_file):
        return {}

    existing_venvs = {}
    with open(venv_file, encoding='utf-8') as f:
        for line in f.readlines():
            name, location = line.split(' ')
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
            f.write(f'{name} {location}')


def pyrun():
    """
    Run a venv
    """
    existing_venvs = _get_existing()
    if not existing_venvs:
        print('No available python environments')
        return

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
    if 'venv' in cmd:
        cmd = os.path.join(cmd, 'bin', 'python')

    prompt = [a for a, b in existing_venvs.items() if b == location][0]

    os.environ['PYPROMPT'] = prompt
    os.environ['PYTHONSTARTUP'] = \
        os.path.expanduser('~/dotfiles/languages/python/startup.py')

    subprocess.run(cmd, check=False)


def pykill(name):
    """
    Delete an existing venv
    """
    existing_venvs = _get_existing()
    if name not in existing_venvs:
        print("Could not find venv '{name}'")
        return

    shutil.rmtree(existing_venvs[name])
    del existing_venvs[name]

    with open(venv_file, 'w', encoding='utf-8') as f:
        for name, location in existing_venvs.items():
            f.write(f'{name} {location}')

    print(f"'{name}' deleted")


def main():
    """
    Main
    """
    cmd = sys.argv[1]

    if cmd == 'pymake':
        if len(sys.argv) < 3:
            print('Please enter a name for the new venv')
            return
        pymake(sys.argv[2], os.path.join(os.getcwd(), 'venv'))
    elif cmd == 'pyrun':
        pyrun()
    elif cmd == 'pykill':
        if len(sys.argv) < 3:
            print('Please enter a venv to be deleted')
            return
        pykill(sys.argv[2])


if __name__ == '__main__':
    main()