#! /bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

# ln -s ${PWD}/vim/.vimrc ~/.vimrc
# ln -s ${PWD}/vim/.vim ~/.vim

vimrc=~/.vimrc
if [ -e "$vimrc" ]; then
    if [ -L "$vimrc" ]; then
        echo "$vimrc already exists and is a link."
    else
        echo "Error. $vimrc already exists"
    fi
else
    echo "$vimrc does not exist. Creating symlink..."
    ln -s ${PWD}/vim/.vimrc ~/.vimrc
fi


vim=~/.vim
if [ -e "$vim" ]; then
    if [ -L "$vim" ]; then
        echo "$vim already exists and is a link."
    else
        echo "Error. $vim already exists"
    fi
else
    echo "$vim does not exist. Creating symlink..."
    ln -s ${PWD}/vim/.vim ~/.vim
fi
