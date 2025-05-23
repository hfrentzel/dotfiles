-- filesystem.lua
-- Commands for working with files and the filesystem, featuring vim-eunuch
-- and nvim-tree.lua

-- Open an NvimTree window replacing the current buffer
local vinegar_open = function()
    vim.g.curr_file = vim.fn.expand('%')
    require('nvim-tree.api').tree.open({
        current_window = true,
        find_file = true,
        path = vim.fn.expand('%:h'),
    })
    vim.b.curr_file = vim.g.curr_file
end

return {
    {
        'eunuch',
        dev = true,
        cmd = { 'Copy', 'Duplicate', 'Mkdir', 'Move', 'Rename', 'Remove', 'SudoWrite' },
    },
    {
        'nvim-tree.lua',
        dev = true,
        keys = {
            { '<leader>1', ':NvimTreeFocus<CR>' },
            { '-', vinegar_open },
        },
        init = function()
            vim.g.loaded_netrw = 1
            vim.g.loaded_netrwPlugin = 1
        end,
        config = function()
            local api = require('nvim-tree.api')

            -- Close a NvimTree buffer that had been opened with vinegar_open
            -- and go back to previous buffer
            local close_tree = function()
                if vim.b.curr_file ~= '' then
                    require('nvim-tree.actions.node.open-file').fn('edit_in_place', vim.b.curr_file)
                elseif vim.b.curr_file == '' then
                    vim.api.nvim_feedkeys(
                        vim.api.nvim_replace_termcodes('<c-6>', true, true, true),
                        'n',
                        true
                    )
                else
                    api.tree.close()
                end
            end

            -- Open the file and replace the NvimTree buffer if opened with
            -- vinegar_open, otherwise just open normally
            local open_or_replace = function()
                if vim.b.curr_file then
                    api.node.open.replace_tree_buffer()
                else
                    api.node.open.edit()
                end
            end

            local on_attach = function(bufnr)
                local opts = { buffer = bufnr, noremap = true, silent = true, nowait = true }

                vim.keymap.set('n', '-', close_tree, opts)
                vim.keymap.set('n', '<c-\\>', api.node.open.vertical, opts)
                vim.keymap.set('n', '<c-s>', api.node.open.horizontal, opts)
                vim.keymap.set('n', '<cr>', open_or_replace, opts)
                vim.keymap.set('n', 'u', api.tree.change_root_to_parent, opts)
            end

            require('nvim-tree').setup({
                actions = {
                    open_file = {
                        -- quit_on_open = true
                    },
                    change_dir = {
                        enable = false,
                    },
                },
                filters = {
                    dotfiles = false,
                },
                renderer = {
                    icons = {
                        glyphs = {
                            folder = {
                                arrow_closed = '▸',
                                arrow_open = '▾',
                            },
                        },
                        show = {
                            file = false,
                            folder = false,
                        },
                    },
                },
                on_attach = on_attach,
            })
        end,
    },
}
