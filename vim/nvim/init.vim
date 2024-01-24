let &packpath = &runtimepath
let g:python3_host_prog = trim(system('which python'))
let g:loaded_netrw       = 1
let g:loaded_netrwPlugin = 1
source ~/.config/vim/vimrc

set completeopt=menu,menuone,noselect
set guicursor=n-v-c-sm:block-blinkon500-blinkwait200,i-ci-ve:ver25-blinkon500,r-cr-o:hor20-blinkon500
let g:CommandTPreferredImplementation='lua'
let g:vimwiki_global_ext = 0
let g:vimwiki_list = [{'path': '~/vimwiki/',
            \ 'syntax': 'markdown', 'ext': '.md'}]

packadd! command-t
packadd! markdown-preview.nvim
packadd! nvim-cmp
packadd! nvim-dap
packadd! nvim-lspconfig
packadd! nvim-tree.lua
packadd! nvim-treesitter
packadd! cmp-nvim-lsp
packadd! cmp-nvim-lua
packadd! cmp-path
packadd! cmp-buffer
packadd! gitsigns.nvim
packadd! playground
packadd! plenary.nvim
packadd! telescope.nvim
packadd! tmux.nvim
packadd! LuaSnip
packadd! cmp_luasnip
packadd! vimwiki

set foldmethod=expr
set foldexpr=nvim_treesitter#foldexpr()
