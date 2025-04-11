[ -z "$PS1" ] && return

export HISTSIZE=100000

export EDITOR=nvim
export VISUAL=nvim 
export PAGER='less --mouse --wheel-lines=3 -RF'
export RIPGREP_CONFIG_PATH=$HOME/.config/ripgrep/config
export FZF_DEFAULT_OPTS='--height 20% --layout=reverse'

# This should normally be set by terminal, I'm setting it manually because
# it's not. May need to change this if I ever start using terminals that
# don't support 24-bit color
export COLORTERM=truecolor

export IS_WSL=$(uname -a | grep WSL)
export GIT_COMPLETION_CHECKOUT_NO_GUESS=1

if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # Color prompt
    if [[ -n "$SSH_TTY" || ! -n $TMUX ]]; then
        USER_NAME="\u@\h:"
    fi
    PS1='\[\033[01;96m\]$(__git_ps1 "[%s] ")\[\033[01;32m\]'$USER_NAME'\[\033[01;34m\]\w\[\033[00m\]$ '
else
    PS1='\w\$ '
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

[ -n "$TMUX" ] && \
    tmux show-environment | grep ^USERPROFILE > /dev/null && \
    export $(tmux show-environment | grep ^USERPROFILE) && \
    export $(tmux show-environment | grep ^WSLENV)

test -f ~/variables && source $HOME/.config/bash/plugins/var_setup.sh
test -f ~/workspaces && source $HOME/.config/bash/plugins/workspace_setup.sh
test -f ~/.secrets && source ~/.secrets

source $HOME/.local/shell/fzf.sh 2> /dev/null
source $HOME/.config/bash/plugins/path.sh
source $HOME/.config/bash/plugins/completions.sh
source $HOME/.config/bash/plugins/utilities.sh
source $HOME/.config/bash/plugins/aliases.sh
source $HOME/.config/bash/plugins/env.sh

BASE16_CONFIG="$HOME/.local/share/mysetup/base16"
test -f $BASE16_CONFIG && color $(cat $BASE16_CONFIG)

if command -v bat &> /dev/null; then
    export MANPAGER="sh -c 'col -bx | bat -l man -p'"
fi

if command -v zoxide &> /dev/null; then
    eval "$(zoxide init bash)"
    export _ZO_FZF_OPTS='--height 40% --layout=reverse'
fi

LOCAL_RC=$HOME/.config/bash/bashrc.local
test -f $LOCAL_RC && source $LOCAL_RC
