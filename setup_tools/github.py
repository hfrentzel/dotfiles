import json
import urllib.request
from json import JSONDecodeError
from setup_tools.managers import Deb, Tar
# Use standard version checking method to see if installed and up to date


# To Install
    # Query GH for the release and get a list of available assets

    # Filter through the asset for the appropriate type (tar.gz, tar.xz, .deb,
    # correct OS, etc.)

    # Install the asset accordingly
def github(repo, version, name=None):
    full_url = f'https://api.github.com/repos/{repo}/releases/tags/{version}'
    download_url = f'https://github.com/{repo}/releases/download/{version}'

    req = urllib.request.Request(url=full_url, method='GET')
    with urllib.request.urlopen(req) as f:
        response = f.read().decode('utf-8')
        try:
            response = json.loads(response)
        except JSONDecodeError:
            print(response)
            return

    available_assets = [a['name'] for a in response['assets']]

    asset = _filter_assets(available_assets)
    version = version.strip('v')
    command = name or repo.split('/')[1]

    if asset is None:
        print(f'No satisfactory asset found for {repo}')
    elif asset.endswith('.deb'):
        Deb(command=command, version=version,
            url=f'{download_url}/{asset}')
    elif '.tar.' in asset:
        Tar(command=command, version=version,
            url=f'{download_url}/{asset}')


def _filter_assets(assets):
    using_deb = False

    deb_assets = [a for a in assets if
        a.endswith('.deb')]
    if len(deb_assets) == 1:
        return deb_assets[0]
    if len(deb_assets) != 0:
        using_deb = True
        assets = deb_assets

    # Filter for 64-bit architectures
    assets = [a for a in assets if 
        'x86_64' in a or 'amd64' in a or 'x64' in a]
    if len(assets) == 1:
        return assets[0]
    if len(assets) == 0:
        return None

    if not using_deb:
        assets = [a for a in assets if 'linux' in a]
        if len(assets) == 1:
            return assets[0]
        if len(assets) == 0:
            return None

    assets = [a for a in assets if 'musl' in a]
    if len(assets) == 1:
        return assets[0]
    if len(assets) == 0:
        return None
    return None

if __name__ == '__main__':
    github('BurntSushi/ripgrep', '13.0.0')
    github('neovim/neovim', 'v0.8.2')
    github('sharkdp/bat', 'v0.23.0')
