if [ ! -d ~/share/terminfo ]; then
    echo "Creating directory ~/share/terminfo"
    mkdir -p ~/share/terminfo
fi

tic -o ~/share/terminfo ~/dotfiles/terminfo/files/tmux.terminfo
tic -o ~/share/terminfo ~/dotfiles/terminfo/files/tmux-256color.terminfo
tic -o ~/share/terminfo ~/dotfiles/terminfo/files/xterm-256color.terminfo
