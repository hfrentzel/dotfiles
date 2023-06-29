[ -z "PS1" ] && return

export HISTSIZE=100000

export EDITOR=vim
export VISUAL=vim 
export PAGER='less --mouse --wheel-lines=3 -RF'
export RIPGREP_CONFIG_PATH=$HOME/.rgrc

# This should normally be set by terminal, I'm setting it manually because
# it's not. May need to change this if I ever start using terminals that
# don't support 24-bit color
export COLORTERM=truecolor

export IS_WSL=$(uname -a | grep WSL)
export GIT_COMPLETION_CHECKOUT_NO_GUESS=1

if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # Color prompt
    PS1='\[\033[01;96m\]$(__git_ps1 "[%s]") \[\033[01;34m\]\w\[\033[00m\]$ '
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

# Base16 Shell
BASE16_SHELL="$HOME/.bash/base16-shell/"
[ -n "$PS1" ] && \
    [ -s "$BASE16_SHELL/profile_helper.sh" ] && \
        eval "$("$BASE16_SHELL/profile_helper.sh")"
source ~/.bash/color.sh

[ -n "$TMUX" ] && \
    tmux show-environment | grep ^USERPROFILE > /dev/null && \
    export $(tmux show-environment | grep ^USERPROFILE) && \
    export $(tmux show-environment | grep ^WSLENV)

test -f ~/dotfiles/git/git_stage.sh && source $HOME/dotfiles/git/git_stage.sh
    
test -f ~/variables && source $HOME/.bash/var_setup.sh
test -f ~/workspaces && source $HOME/.bash/workspace_setup.sh
test -f ~/.secrets && source ~/.secrets

source $HOME/.bash/path.sh
source $HOME/.bash/completions.sh
source $HOME/.bash/utilities.sh
source $HOME/.config/fzf/fzf.bash
source $HOME/.bash/aliases.sh

eval "$(zoxide init bash)"
export _ZO_FZF_OPTS='--height 40% --layout=reverse'

LOCAL_RC=$HOME/.bashrc.local
test -f $LOCAL_RC && source $LOCAL_RC
