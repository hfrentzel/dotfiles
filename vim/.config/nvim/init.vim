set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
let g:python3_host_prog = trim(system('which python3'))
source ~/.vimrc

set completeopt=menu,menuone,noselect

packadd! nvim-lspconfig
packadd! nvim-cmp
packadd! cmp-nvim-lsp
packadd! cmp-nvim-lua
packadd! cmp-path
packadd! cmp-buffer
