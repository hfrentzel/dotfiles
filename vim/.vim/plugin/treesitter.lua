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
            node_incremental = 'gk',
            node_decremental = 'gj'
        }
    },

    indent = {
        enable = true
    },

    playground = {
        enable = true,
        persist_queries = false,
        updatetime = 25,
    }
}

vim.keymap.set('n', '<leader>x', '<cmd>lua print(require"nvim-treesitter.ts_utils".get_node_at_cursor():type())<CR>')
