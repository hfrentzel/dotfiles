export HISTSIZE=100000

export EDITOR=vim
export VISUAL=vim 
export RIPGREP_CONFIG_PATH=$HOME/.rgrc

export IS_WSL=$(uname -a | grep WSL)

if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # Color prompt
    PS1='\[\033[01;96m\]$(__git_ps1 "[%s]") \[\033[01;34m\]\w\[\033[00m\]$ '
else
    PS1='\w\$ '
fi

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
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
    export $(tmux show-environment | grep ^USERPROFILE) && \
    export $(tmux show-environment | grep ^WSLENV)

export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.bin:$PATH"

test -f ~/dotfiles/git/git_stage.sh && source $HOME/dotfiles/git/git_stage.sh
    
test -f ~/variables && source $HOME/.bash/var_setup.sh
test -f ~/workspaces && source $HOME/.bash/workspace_setup.sh

source $HOME/.bash/python.sh
source $HOME/.bash/utilities.sh

LOCAL_RC=$HOME/.bashrc.local
test -f $LOCAL_RC && source $LOCAL_RC

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
