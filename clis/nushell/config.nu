$env.config.buffer_editor = "nvim"

alias ll = ^ls -hlAF --color=auto
alias g = git
alias v = nvim

$env.XDG_CONFIG_HOME = $env.USERPROFILE + "/AppData/Roaming"
$env.RIPGREP_CONFIG_PATH = $env.XDG_CONFIG_HOME + "/ripgrep/config"
$env.PYLINTRC = $env.XDG_CONFIG_HOME + "/pylint/pylintrc"
$env.PYTHONSTARTUP = $env.XDG_CONFIG_HOME + "/python/startup.py"
$env.CARGO_HOME = $env.USERPROFILE + "/.local/share/cargo"
$env.RUSTUP_HOME = $env.USERPROFILE + "/.local/share/rustup"

source ~/.cache/zoxide.nu
