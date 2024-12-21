-- notes.lua
--
-- Uses obsidian.nvim to provide a notetaking system

return {
    {
        'obsidian.nvim',
        dir = '~/.config/nvim/pack/vendor/opt/obsidian.nvim',
        ft = { 'markdown' },
        keys = {
            {
                '<leader>ww',
                function()
                    vim.cmd.edit('~/vimwiki/index.md')
                end,
            },

        },
        opts = {
            workspaces = {
                {
                    name = 'notes',
                    path = '~/vimwiki',
                },
            },
            callbacks = {
                post_setup = function()
                    vim.wo.conceallevel = 2
                end,
                enter_note = function()
                    vim.wo.conceallevel = 2
                end,
                leave_note = function()
                    vim.wo.conceallevel = 0
                end,
            },
            mappings = {
                ["<cr>"] = {
                    action = function()
                        return require("obsidian").util.smart_action()
                    end,
                    opts = { buffer = true, expr = true }
                }
            },
            note_id_func = function(title)
                return title
            end,
            note_frontmatter_func = function()
                return {}
            end
        },
    },
}
