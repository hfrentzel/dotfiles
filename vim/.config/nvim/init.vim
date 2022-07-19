set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
let g:python3_host_prog = trim(system('which python3'))
source ~/.vimrc

packadd! nvim-lspconfig
