rgl() {
    rg -p "$@" | less -RFXS
}

conf() {
    local TOOL=$1
    local DIR="$HOME/.config/$1"

    if [[ ! -d "$DIR" ]]; then
        echo "No config found for $1"
        return
    fi

    local FILES="$(find "$DIR" -follow -mindepth 1 -type f)"
    local NUM_FILES=$(echo "$FILES" | wc -l)
    if [[ $NUM_FILES -gt 1 ]]; then
        # nvim $(echo "$FILES" | fzf)
        echo "$FILES" | fzf --bind 'enter:become(nvim {}),ctrl-o:become(echo {}),ctrl-p:become(bat {})'
    else
        nvim $FILES
    fi
}

_fzf_conf_completion() {
    _fzf_complete -- "$@" < <(ls ~/.config/)
}
complete -F _fzf_conf_completion conf

bn() {
    local offset=${3:-5};
    bat --line-range $(($2-$offset)):$(($2+$offset)) --highlight-line $2 $1
}
