import os


def add_symlink(src, dest):
    src = os.path.expanduser(src)
    dest = os.path.expanduser(dest)
    if os.path.isfile(dest) or os.path.isdir(dest):
        if os.path.islink(dest):
            print(f'{dest} already exists and is a link')
        else:
            print(f'Error. {dest} already exists')
        return False

    print(f'{dest} does not exist. Creating symlink...')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    os.symlink(src, dest)
    return True
