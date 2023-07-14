#! /usr/bin/python
from setup2 import run, Exe, Sym

Exe('jq')
Exe('dos2unix')
Exe('rg', '13.0.0')
Exe('bat', '0.23.0')
Sym('bashrc', 'DOT/bash/.bashrc', '~/.bashrc')
Sym('inputrc', 'DOT/bash/.inputrc', '~/.inputrc')
Sym('tmux.conf', 'DOT/tmux/.tmux.conf', '~/.tmux.conf')

run()
