#! /bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

# ln -s ${PWD}/vim/.vimrc ~/.vimrc
# ln -s ${PWD}/vim/.vim ~/.vim

add_symlink () {
    src_file=$1
    new_link=$2
    if [ -e "$new_link" ]; then
        if [ -L "$new_link" ]; then
            echo "$new_link already exists and is a link."
        else
            echo "Error. $new_link already exists"
                fi
    else
        echo "$new_link does not exist. Creating symlink..."
            ln -s $src_file $new_link
            fi
}

add_symlink ${PWD}/vim/.vimrc ~/.vimrc
add_symlink ${PWD}/vim/.vim ~/.vim
add_symlink ${PWD}/tmux/.tmux.conf ~/.tmux.conf
add_symlink ${PWD}/bash/.bashrc ~/.bashrc
add_symlink ${PWD}/bash/.bash ~/.bash
