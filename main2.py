#! /usr/bin/python
from setup2 import run, Exe, Sym, Dir
from vim import install_neovim

# Basic tools for working in the terminal
Sym('bashrc', 'DOT/bash/.bashrc', '~/.bashrc')
Sym('bash', 'DOT/bash/plugins', '~/.config/bash/plugins')
Sym('inputrc', 'DOT/bash/.inputrc', '~/.config/readline/inputrc')
Dir('bash_data', '~/.local/share/bash')
Dir('dotfiles_data', '~/.local/share/dotfiles')

Sym('tmux.conf', 'DOT/tmux/.tmux.conf', '~/.config/tmux/tmux.conf')
Sym('tmux_dir', 'DOT/tmux/.tmux', '~/.config/tmux/plugins')

Exe('jq', installers=['Apt'])
Exe('dos2unix', installers=['Apt'])
Exe('zoxide', '0.9.0', installers=['Github'], repo='ajeetdsouza/zoxide')
Dir('less_data', '~/.local/share/less')

Exe('delta', '0.15.1', installers=['Github'], repo='dandavision/delta')
Sym('gitconfig', 'DOT/git/gitconfig', '~/.config/git/config')

Exe('ripgrep', '13.0.0', installers=['Github'], repo='BurntSushi/ripgrep', 
    command_name='rg')
Sym('rgconfig', 'DOT/configs/rgrc', '~/.config/ripgrep/config')

Exe('bat', '0.23.0', installers=['Github'], repo='sharkdp/bat')
Sym('batconfig', 'DOT/configs/batconfig', '~/.config/bat/config')

Sym('startup.py', 'DOT/languages/python/gen_startup.py', '~/.config/python/startup.py')
Sym('npmrc', 'DOT/configs/npmrc', '~/.config/npm/npmrc')
Sym('cargoconfig', 'DOT/languages/rust/config.toml', '~/.local/share/cargo/config.toml')
Dir('python_data', '~/.local/share/python')

install_neovim()

run()
