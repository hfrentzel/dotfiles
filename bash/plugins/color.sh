BASE16_CONFIG="$HOME/.local/share/dotfiles/base16"

color() {
    theme=$1
    bash_dir=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
    base16_dir="$bash_dir/base16-shell/scripts"

    script_file="$base16_dir/base16-$theme.sh"

    if ! [[ -e "$script_file" ]]; then
        echo "$theme not found in $base16_dir"
        return
    fi

    echo "$theme" > "$BASE16_CONFIG"
    sh "$script_file"

    if [ -n "$TMUX" ]; then
        local bg=$(grep color_background= "$script_file" | cut -d \" -f2 | sed -e 's#/##g')
        local ws=$(grep color18= "$script_file" | cut -d \" -f2 | sed -e 's#/##g')
        command tmux set -a window-active-style "bg=#$bg"
        command tmux set -a window-style "bg=#$ws"
        command tmux set -a pane-active-border-style "bg=#$ws"
        command tmux set -a pane-border-style "bg=#$ws"
    fi
}

test -f $BASE16_CONFIG && color $(cat $BASE16_CONFIG)
