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
                        ':ObsidianLinkNew<cr>',
                        { buffer = true, silent = true }
                    )
                end,
                leave_note = function()
                    vim.wo.conceallevel = 0
                end,
            },
            mappings = {
                ['<cr>'] = {
                    action = function()
                        return require('obsidian').util.smart_action()
                    end,
                    opts = { buffer = true, expr = true },
                },
            },
            note_id_func = function(title)
                return title
            end,
            note_frontmatter_func = function()
                return {}
            end,
        },
    },
}
