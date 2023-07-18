if command -v node &> /dev/null; then
    export NODE_REPL_HISTORY=""
    export NPM_CONFIG_CACHE=~/.local/cache/npm
fi

export LESSHISTFILE=~/.local/share/less/history
export HISTFILE=~/.local/share/bash/history
export INPUTRC=~/.config/readline/config
bind -f $INPUTRC

export PYTHONSTARTUP=~/.config/python/startup.py
