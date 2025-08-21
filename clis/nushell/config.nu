$env.config.buffer_editor = "nvim"

alias ll = ^ls -hlAF --color=auto
alias g = git
alias v = nvim
alias :q = exit

$env.config.shell_integration.osc133 = false
$env.config.table.mode = "none"

if $nu.os-info.name == 'windows' {
    $env.XDG_CONFIG_HOME = $env.USERPROFILE + "/AppData/Roaming"
    $env.CARGO_HOME = $env.USERPROFILE + "/.local/share/cargo"
    $env.RUSTUP_HOME = $env.USERPROFILE + "/.local/share/rustup"
} else {
    $env.XDG_CONFIG_HOME = $env.HOME + "/.config"
    $env.CARGO_HOME = $env.HOME + "/.local/share/cargo"
    $env.RUSTUP_HOME = $env.HOME + "/.local/share/rustup"
}
$env.RIPGREP_CONFIG_PATH = $env.XDG_CONFIG_HOME + "/ripgrep/config"
$env.PYLINTRC = $env.XDG_CONFIG_HOME + "/pylint/pylintrc"
$env.PYTHONSTARTUP = $env.XDG_CONFIG_HOME + "/python/startup.py"

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

$env.PROMPT_COMMAND_RIGHT = {||
    # create a right prompt in magenta with green separators and am/pm underlined
    let time_segment = ([
        (ansi reset)
        (ansi magenta)
        (date now | format date '%D %H:%M:%S') # try to respect user's locale
    ] | str join | str replace --regex --all "([/:])" $"(ansi green)${1}(ansi magenta)")

    let last_exit_code = if ($env.LAST_EXIT_CODE != 0) {([
        (ansi rb)
        ($env.LAST_EXIT_CODE)
    ] | str join)
    } else { "" }

    ([$last_exit_code, (char space), $time_segment] | str join)
}

source ~/.cache/zoxide.nu
