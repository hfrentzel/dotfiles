-- treesitter.lua
-- Initialize and configure treesitter for syntax highlighting, indents, folds
-- and selections

return {
    {
        'nvim-treesitter',
        dir = '~/.config/nvim/pack/vendor/opt/nvim-treesitter',
        event = { 'BufReadPost', 'BufNewFile' },
        cmd = { 'TSUpdate', 'TSUpdateSync' },
        dependencies = {
            {
                'nvim-treesitter-textobjects',
                dir = '~/.config/nvim/pack/vendor/opt/nvim-treesitter-textobjects',
            },
        },
        config = function()
            local treesitter = require('nvim-treesitter.configs')
            treesitter.setup({
                parser_install_dir = vim.fn.stdpath('data') .. '/site',
                ensure_installed = { 'lua', 'python', 'vim' },
                auto_installed = { 'lua', 'python', 'vim' },

                highlight = {
                    enable = true,
                    additional_vim_regex_highlighting = false,
                },

                incremental_selection = {
                    enable = true,
                    keymaps = {
                        init_selection = 'gnn',
                        node_incremental = 'gk',
                        node_decremental = 'gj',
                    },
                },

                indent = {
                    enable = true,
                },

                textobjects = {
                    select = {
                        enable = true,
                        keymaps = {
                            ['af'] = '@function.outer',
                            ['if'] = '@function.inner',
                            ['aif'] = '@conditional.outer',
                            ['iif'] = '@conditional.inner',
                        },
                    },
                    move = {
                        enable = true,
                        goto_next_start = {
                            [']f'] = '@function.outer',
                        },
                        goto_previous_start = {
                            ['[f'] = '@function.outer',
                        },
                    },
                },
            })

            vim.o.foldmethod = 'expr'
            vim.o.foldexpr = 'nvim_treesitter#foldexpr()'
            vim.keymap.set(
                'n',
                '<leader>x',
                '<cmd>lua print(require"nvim-treesitter.ts_utils".get_node_at_cursor():type())<CR>'
            )
        end,
    },
}
