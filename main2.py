#! /usr/bin/python
from os.path import expanduser

from setup2 import run, Exe, Sym, Dir, Command

Command('submodules', 'git submodule update', cwd='DOT') 
Command('cargo', 'curl https://sh.rustup.rs -sSf | sh -s -- -y --no-modify-path', 
        check_script='cargo --version',
        depends_on='cargoconfig',
        env={'CARGO_HOME': expanduser('~/.local/share/cargo'), 
             'RUSTUP_HOME': expanduser('~/.local/share/rustup')}) 
Exe('jq')
Exe('dos2unix')
Exe('node', '18.18.2', url='https://nodejs.org/dist/v{version}/node-v{version}-linux-x64.tar.xz',
    installers=['Tar'])
Exe('ripgrep', '13.0.0', command_name='rg', installers=['Cargo'])
Exe('tree', installers=['Apt'])
Exe('hehe', installers=['Apt'])
Exe('bat', '0.24.0', installers=['Tar', 'Cargo'], url='https://github.com/sharkdp/bat/releases/download/v{version}/bat-v{version}-x86_64-unknown-linux-musl.tar.gz')
Exe('delta', '0.15.1', installers=['Cargo'])
Exe('zoxide', '0.9.0', installers=['Cargo'])
Exe('fd-find', '8.7.0', command_name='fd', installers=['Cargo'])
Exe('eslint', '8.32.0', installers=['Npm'])
Exe('python3.9', '3.9.5', installers=['Apt'])
Exe('python-lsp-server', '1.7.1', command_name='pylsp', installers=['Pip'])
Sym('bashrc', 'DOT/bash/.bashrc', '~/.bashrc')
Sym('bash', 'DOT/bash/plugins', '~/.config/bash/plugins')
Sym('inputrc', 'DOT/bash/.inputrc', '~/.config/readline/inputrc')
Sym('tmux.conf', 'DOT/tmux/.tmux.conf', '~/.config/tmux/tmux.conf')
Sym('tmux_dir', 'DOT/tmux/.tmux', '~/.config/tmux/plugins')
Sym('rgconfig', 'DOT/configs/rgrc', '~/.config/ripgrep/config')
Sym('batconfig', 'DOT/configs/batconfig', '~/.config/bat/config')
Sym('startup.py', 'DOT/languages/python/gen_startup.py', '~/.config/python/startup.py')
Sym('gitconfig', 'DOT/git/gitconfig', '~/.config/git/config')
Sym('npmrc', 'DOT/configs/npmrc', '~/.config/npm/npmrc')
Sym('vimrc', 'DOT/vim/vimrc', '~/.config/vim/vimrc')
Sym('nvimconfig', 'DOT/vim/nvim', '~/.config/nvim')
Sym('cargoconfig', 'DOT/languages/rust/config.toml', '~/.local/share/cargo/config.toml')

Dir('python_data', '~/.local/share/python')
Dir('dne', '~/dne')
Dir('dotfiles_data', '~/.local/share/dotfiles')
Dir('python_data', '~/.local/share/python')
Dir('less_data', '~/.local/share/less')
Dir('bash_data', '~/.local/share/bash')

run()
