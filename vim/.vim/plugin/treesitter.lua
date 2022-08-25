require 'nvim-treesitter.configs'.setup {
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
            node_incremental = 'K',
            node_decremental = 'J'
        }
    },

    indent = {
        enable = true
    },

    playground = {
        enable = true,
        updatetime = 25,
        persist_queries = false,
    }
}

vim.keymap.set('n', '<leader>x', '<cmd>lua print(require"nvim-treesitter.ts_utils".get_node_at_cursor():type())<CR>')
