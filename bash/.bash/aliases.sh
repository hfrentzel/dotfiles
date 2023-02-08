
alias :q='exit'
alias ls='ls --color=auto'

alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'

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
alias jcurrent="jira issue list -a$(jira me) -s \"In Progress\""
