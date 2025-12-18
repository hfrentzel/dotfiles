-- notes.lua
--
-- Uses obsidian.nvim to provide a notetaking system

return {
    {
        'obsidian.nvim',
        dev = true,
        ft = { 'markdown' },
        keys = {
            {
                '<leader>ww',
                function()
                    vim.cmd.edit('~/notes/index.md')
                end,
            },
        },
        opts = {
            legacy_commands = false,
            checkbox = { create_new = false },
            workspaces = {
                {
                    name = 'notes',
                    path = '~/notes',
                },
            },
            callbacks = {
                post_setup = function()
                    vim.wo.conceallevel = 2
                end,
                enter_note = function()
                    vim.wo.conceallevel = 2
                    vim.keymap.set(
                        'v',
                        '<cr>',
                        ':Obsidian link_new<cr>',
                        { buffer = true, silent = true }
                    )
                end,
                leave_note = function()
                    vim.wo.conceallevel = 0
                end,
            },
            note_id_func = function(title)
                return title
            end,
            frontmatter = {
                enabled = false,
            },
        },
    },
}
