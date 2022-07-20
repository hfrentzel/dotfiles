BASE16_CONFIG="$HOME/.base16"

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
}
