def conf [TOOL] {
    mut any_dir_exists = false
    mut files = ""

    let DIR = $"($env.USERPROFILE)/.config/($TOOL)"
    if ($DIR | path exists) {
        $any_dir_exists = true
        $files += ^fd . $DIR -L
    }

    if $nu.os-info.name == 'windows' {
        let DIRR = $"($env.USERPROFILE)/AppData/Roaming/($TOOL)"
        let DIRL = $"($env.USERPROFILE)/AppData/Local/($TOOL)"

        if ($DIRR | path exists) {
            $any_dir_exists = true
            $files += ^fd . $DIRR -L
        }
        if ($DIRL | path exists) {
            $any_dir_exists = true
            $files += ^fd . $DIRL -L
        }
    }

    if not $any_dir_exists {
        print $"No config found for ($TOOL)"
        return
    }

    let num_files = $files | split row "\n" | length
    if $num_files > 1 {
        $files | fzf --bind 'enter:become(nvim {}),ctrl-o:become(echo {}),ctrl-p:become(bat {})'
    } else {
        nvim $files
    }
}
