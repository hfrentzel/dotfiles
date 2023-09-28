compalias() {
    alias=$1
    cmd=$2
    if [[ -z "$alias" || -z "$cmd" ]]; then
        echo "compalias args not set"
        return
    fi

    alias "$alias"="$cmd"

    existing_completion=$(complete -p $cmd 2> /dev/null | sed 's/ [^ ]*$//')
    if [[ ! -z "$existing_completion" ]]; then
        eval "$existing_completion $alias"
    fi

    # Dynamic completion file already exists, no need to go further
    if [[ -f "$HOME/.local/share/bash-completion/completions/$alias" ]]; then
        return
    fi

    local -a dirs=( $HOME/.local/share/bash-completion/completions )
    local OIFS=$IFS IFS=: dir compfile
    for dir in ${XDG_DATA_DIRS:-/usr/local/share:/usr/share}; do
        dirs+=( $dir/bash-completion/completions )
    done
    IFS=$OIFS

    for dir in "${dirs[@]}"; do
        [[ -d "$dir" ]] || continue
        for compfile in "$cmd" "$cmd.bash" "_$cmd"; do
            compfile="$dir/$compfile"

            if [[ -f "$compfile" ]]; then
                mkdir -p "$HOME/.local/share/bash-completion/completions/"
                cat <<EOF > "$HOME/.local/share/bash-completion/completions/$alias"
main_command_completion=\$(complete -p $cmd)

_completion_loader $cmd
alias_completion="\$(complete -p $cmd | sed 's/ [^ ]*\$//') $alias"
eval "\$alias_completion"

eval "\$main_command_completion"
EOF
                return
            fi
        done
    done
}


alias :q='exit'
alias ls='ls --color=auto'

alias l='ls -hCF'
alias la='ls -AF'
alias ll='ls -hlAF'

compalias g git
compalias b bat
alias t='tmux'
compalias v nvim
compalias kb kubectl
compalias tf 'terraform'

alias activate=". ./venv/bin/activate"
alias cddot='cd ~/dotfiles'
alias grep='grep --color=auto'
alias pytree="tree -I 'venv|__pycache__'"
alias tmuxl='tmux list-sessions'
alias path='echo $PATH | tr : "\n"'

# Use git-delta side-by-side iff the terminal is at least 160 characters wide
alias git='$([ $(tput cols) -gt 160 ] && echo "git -c delta.side-by-side=true" || echo "git")'

# Python venv management
alias pymake="python ~/dotfiles/languages/python/venv_management.py pymake"
alias pyrun="python ~/dotfiles/languages/python/venv_management.py pyrun"
alias pykill="python ~/dotfiles/languages/python/venv_management.py pykill"

# JIRA
alias jcurrent="jira issue list -a$(which jira && jira me) -s \"In Progress\""

compalias gl glab
