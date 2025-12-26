if command -v node &> /dev/null; then
    export NODE_REPL_HISTORY=""
    export NPM_CONFIG_USERCONFIG="$HOME/.config/npm/npmrc"
fi

export TF_CLI_CONFIG_FILE="$HOME/.config/terraform/config.tf"

export LESSHISTFILE="$HOME/.local/share/less/history"
export HISTFILE="$HOME/.local/share/bash/history"
export INPUTRC="$HOME/.config/readline/inputrc"

export PYTHONSTARTUP="$HOME/.config/python/startup.py"
export PYLINTRC="$HOME/.config/pylint/pylintrc"
export MYPY_CACHE_DIR="$HOME/.cache/mypy"

export RUSTUP_HOME="$HOME/.local/share/rustup"
export CARGO_HOME="$HOME/.local/share/cargo"

export SQLITE_HISTORY="$HOME/.local/share/sqlite_history"
