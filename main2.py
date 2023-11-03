#! /usr/bin/python
from setup2 import run, Exe, Sym, Dir

Exe('jq')
Exe('dos2unix')
Exe('rg', '13.0.0')
Exe('bat', '0.23.0')
Exe('delta', '0.15.1')
Exe('zoxide', '0.9.0')
Sym('bashrc', 'DOT/bash/.bashrc', '~/.bashrc')
Sym('bash', 'DOT/bash/plugins', '~/.config/bash/plugins')
Sym('inputrc', 'DOT/bash/.inputrc', '~/.config/readline/inputrc')
Sym('tmux.conf', 'DOT/tmux/.tmux.conf', '~/.config/tmux/tmux.conf')
Sym('tmux_dir', 'DOT/tmux/.tmux', '~/.config/tmux/plugins')
Sym('rgconfig', 'DOT/configs/rgrc', '~/.config/ripgrep/config')
Sym('batconfig', 'DOT/configs/batconfig', '~/.config/bat/config')
Sym('startup.py', 'DOT/languages/python/gen_startup.py', '~/.config/python/startup.py')
Sym('gitconfig', 'DOT/git/gitconfig', '~/.config/git/config')
Sym('vimrc', 'DOT/vim/vimrc', '~/.config/vim/vimrc')
Sym('nvimconfig', 'DOT/vim/nvim', '~/.config/nvim')

Dir('dotfiles_data', '~/.local/share/dotfiles')
Dir('python_data', '~/.local/share/python')
Dir('less_data', '~/.local/share/less')
Dir('bash_data', '~/.local/share/bash')

run()
