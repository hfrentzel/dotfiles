$env.config.buffer_editor = "nvim"

alias ll = ^ls -hlAF --color=auto
alias g = git
alias v = nvim

$env.config.shell_integration.osc133 = false

$env.XDG_CONFIG_HOME = $env.USERPROFILE + "/AppData/Roaming"
$env.RIPGREP_CONFIG_PATH = $env.XDG_CONFIG_HOME + "/ripgrep/config"
$env.PYLINTRC = $env.XDG_CONFIG_HOME + "/pylint/pylintrc"
$env.PYTHONSTARTUP = $env.XDG_CONFIG_HOME + "/python/startup.py"
$env.CARGO_HOME = $env.USERPROFILE + "/.local/share/cargo"
$env.RUSTUP_HOME = $env.USERPROFILE + "/.local/share/rustup"

$env.config.keybindings = [
    {
        name: insert_last_token
        modifier: alt
        keycode: char_.
        mode: emacs
        event: [
            { edit: InsertString, value: " !$" }
            { send: Enter }
        ]
    }
]

source ~/.cache/zoxide.nu
