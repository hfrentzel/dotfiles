vim.o.packpath = vim.o.runtimepath
vim.g.python3_host_prog = vim.fn.trim(vim.fn.system('which python'))
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
vim.cmd.source('~/.config/vim/vimrc')

vim.o.completeopt='menu,menuone,noselect'
vim.o.guicursor='n-v-c-sm:block-blinkon500-blinkwait200,i-ci-ve:ver25-blinkon500,r-cr-o:hor20-blinkon500'

vim.g.CommandTPreferredImplementation='lua'
vim.g.vimwiki_global_ext = 0
vim.g.vimwiki_list = {{path = '~/vimwiki/', syntax = 'markdown', ext = '.md'}}

vim.o.foldmethod = 'expr'
vim.o.foldexpr = 'nvim_treesitter#foldexpr()'

local lazypath = '~/.config/nvim/pack/vendor/opt/lazy.nvim'
vim.opt.rtp:prepend(lazypath)

local function build_list(packages)
    local result = {}
    for _, package in ipairs(packages) do
        table.insert(result, {package, dir = '~/.config/nvim/pack/vendor/opt/'..package})
    end
    return result
end

require('lazy').setup(build_list{
'command-t',
'markdown-preview.nvim',
'nvim-cmp',
'nvim-dap',
'nvim-lspconfig',
'nvim-tree.lua',
'nvim-treesitter',
'cmp-nvim-lsp',
'cmp-nvim-lua',
'cmp-path',
'cmp-buffer',
'gitsigns.nvim',
'playground',
'plenary.nvim',
'telescope.nvim',
'tmux.nvim',
'LuaSnip',
'cmp_luasnip',
'vimwiki',

'CamelCaseMotion',
'base16-vim',
'fugitive',
'eunuch',
'vim-slime',
'vim-surround',
'vim-visual-multi',

'pinnacle',
'tcomment_vim',
})
