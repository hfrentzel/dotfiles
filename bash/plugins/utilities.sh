rgl() {
    rg -p "$@" | less -RFXS
}

conf() {
    TOOL=$1
    DIR="$HOME/.config/$1"

    if [[ ! -d "$DIR" ]]; then
        echo "No config found for $1"
        return
    fi

    FILES="$(find "$DIR" -mindepth 1)"
    NUM_FILES=$(echo "$FILES" | wc -l)
    if [[ $NUM_FILES -gt 1 ]]; then
        # nvim $(echo "$FILES" | fzf)
        echo "$FILES" | fzf --bind 'enter:become(nvim {}),ctrl-o:become(bat {})'
    else
        nvim $FILES
    fi
}

_fzf_conf_completion() {
    _fzf_complete -- "$@" < <(ls ~/.config/)
}
complete -F _fzf_conf_completion conf
