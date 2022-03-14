color() {
    theme=$1
    bash_dir=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
    base16_dir="${bash_dir}/base16-shell/scripts"

    script_file="${base16_dir}/base16-${theme}.sh"

    if ! [ -e $script_file ]; then
        echo "Theme doesn't exist"
        return
    fi
    _base16 $script_file $theme
    if [ -z $vscode_base16[$theme] ]; then
        return
    fi
    if [ -n $USERPROFILE ]; then
        settings_file="$USERPROFILE/AppData/Roaming/Code/User/settings.json"
        if [ -f $settings_file ]; then
            sed_scheme="s/(\"workbench.colorTheme\": ).*/\1\"${vscode_base16[$theme]}\",/" 
            sed -i -E "$sed_scheme" $settings_file
        fi
    fi
}

declare -A vscode_base16=(
    [ocean]="Base16 Dark Ocean"
    [tomorrow]="Base16 Light Tomorrow"
    [tomorrow-night]="Base16 Dark Tomorrow"
)
