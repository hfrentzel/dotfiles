if command -v node &> /dev/null; then
    export NODE_REPL_HISTORY=""
    export NPM_CONFIG_USERCONFIG="$HOME/.config/npm/npmrc"
fi

export LESSHISTFILE="$HOME/.local/share/less/history"
export HISTFILE="$HOME/.local/share/bash/history"
export INPUTRC="$HOME/.config/readline/inputrc"

export PYTHONSTARTUP="$HOME/.config/python/startup.py"

export RUSTUP_HOME="$HOME/.local/share/rustup"
export CARGO_HOME="$HOME/.local/share/cargo"
