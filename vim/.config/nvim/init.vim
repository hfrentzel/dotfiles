set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
let g:python3_host_prog = '/home/hfrentzel/.pyenv/shims/python'
source ~/.vimrc

packadd! nvim-lspconfig
