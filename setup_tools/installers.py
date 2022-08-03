import subprocess


def add_apt_repo(repo_name):
    repo_list = subprocess.run(['apt-cache', 'policy'], capture_output=True)
    grep = subprocess.run(['grep', repo_name], input=repo_list.stdout)

    if not grep.returncode:
        print(f'{repo_name} is already in the apt cache')
        return

    print(f'Adding {repo_name}')
    subprocess.run(['sudo', 'add-apt-repository', '--yes', repo_name], capture_output=True)
    print(f'{repo_name} successfully added')

    print('Running apt update')
    subprocess.run(['sudo', 'apt', 'update'], capture_output=True)


def install_linux_package(package_name, repo_name=None):
    print(f'Checking for installed package {package_name}')
    process = subprocess.run(['dpkg', '-s', package_name], capture_output=True)
    if not process.returncode:
        print(f'{package_name} is already installed')
        return False

    print(f'{package_name} is not installed')
    if repo_name:
        add_apt_repo(repo_name)

    print(f'Installing {package_name}...')
    process = subprocess.run(['sudo', 'apt', 'install', '--yes', package_name], capture_output=True)
    if not process.returncode:
        print(f'{package_name} successfully installed')
        return True
    print(f'Failed to install {package_name}')
    return False


def pip_install(package_name):
    freeze_list = subprocess.run(['python3', '-m', 'pip', 'freeze'], capture_output=True)
    grep = subprocess.run(['grep', package_name], input=freeze_list.stdout)

    if not grep.returncode:
        print(f'{package_name} is already installed to python')

    print(f'Installing python package {package_name}')
    subprocess.run(['python3', '-m', 'pip', 'install', package_name], capture_output=True)
