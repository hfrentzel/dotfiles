-- treesitter.lua
-- Initialize and configure treesitter for syntax highlighting, indents, folds
-- and selections

return {
    { 'nvim-treesitter', dir='~/.config/nvim/pack/vendor/opt/nvim-treesitter',
        event='VeryLazy',
        config = function()
            local treesitter = require('nvim-treesitter.configs')
            treesitter.setup {
                parser_install_dir = vim.fn.stdpath('data')..'/site',
                ensure_installed = {'lua', 'python', 'vim'},
                auto_installed = {'lua', 'python', 'vim'},

                highlight = {
                    enable = true,
                    additional_vim_regex_highlighting = false
                },

                incremental_selection = {
                    enable = true,
                    keymaps = {
                        init_selection = 'gnn',
                        node_incremental = 'gk',
                        node_decremental = 'gj'
                    }
                },

                indent = {
                    enable = true
                }
            }

            vim.o.foldmethod = 'expr'
            vim.o.foldexpr = 'nvim_treesitter#foldexpr()'
            vim.keymap.set('n', '<leader>x', '<cmd>lua print(require"nvim-treesitter.ts_utils".get_node_at_cursor():type())<CR>')
        end
    }
}
