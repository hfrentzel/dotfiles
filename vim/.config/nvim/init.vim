set runtimepath^=~/.vim runtimepath+=~/.vim/after
let &packpath = &runtimepath
let g:python3_host_prog = trim(system('which python'))
source ~/.vimrc

set completeopt=menu,menuone,noselect
let g:CommandTPreferredImplementation='lua'
set guicursor=n-v-c-sm:block-blinkon500-blinkwait200,i-ci-ve:ver25-blinkon500,r-cr-o:hor20-blinkon500

packadd! nvim-cmp
packadd! nvim-lspconfig
packadd! nvim-treesitter
packadd! cmp-nvim-lsp
packadd! cmp-nvim-lua
packadd! cmp-path
packadd! cmp-buffer
packadd! gitsigns.nvim
packadd! playground
packadd! plenary.nvim
packadd! LuaSnip
packadd! cmp_luasnip

set foldmethod=expr
set foldexpr=nvim_treesitter#foldexpr()
