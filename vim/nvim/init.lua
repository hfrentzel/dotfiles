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

vim.cmd.packadd({'command-t', bang = true})
vim.cmd.packadd({'markdown-preview.nvim', bang = true})
vim.cmd.packadd({'nvim-cmp', bang = true})
vim.cmd.packadd({'nvim-dap', bang = true})
vim.cmd.packadd({'nvim-lspconfig', bang = true})
vim.cmd.packadd({'nvim-tree.lua', bang = true})
vim.cmd.packadd({'nvim-treesitter', bang = true})
vim.cmd.packadd({'cmp-nvim-lsp', bang = true})
vim.cmd.packadd({'cmp-nvim-lua', bang = true})
vim.cmd.packadd({'cmp-path', bang = true})
vim.cmd.packadd({'cmp-buffer', bang = true})
vim.cmd.packadd({'gitsigns.nvim', bang = true})
vim.cmd.packadd({'playground', bang = true})
vim.cmd.packadd({'plenary.nvim', bang = true})
vim.cmd.packadd({'telescope.nvim', bang = true})
vim.cmd.packadd({'tmux.nvim', bang = true})
vim.cmd.packadd({'LuaSnip', bang = true})
vim.cmd.packadd({'cmp_luasnip', bang = true})
vim.cmd.packadd({'vimwiki', bang = true})

vim.o.foldmethod = 'expr'
vim.o.foldexpr = 'nvim_treesitter#foldexpr()'
-- local lazypath = '/home/htfrentzel/.config/nvim/pack/vendor/opt/lazy.nvim'
-- vim.opt.rtp:prepend(lazypath)
--
-- require('lazy').setup('plugins', { defaults = {lazy=true }})
