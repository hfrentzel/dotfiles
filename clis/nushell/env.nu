$env.Path ++= ["~/.local/bin"]
$env.Path ++= ["~/.local/share/node"]

zoxide init nushell | save -f ~/.cache/zoxide.nu
