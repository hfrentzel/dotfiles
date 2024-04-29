-- notes.lua
--
-- Uses vimwiki to provide a notetaking system

return {
    {
        'vimwiki',
        dir = '~/.config/nvim/pack/vendor/opt/vimwiki',
        keys = { '<leader>ww' },
        ft = { 'vimwiki', 'markdown' },
        init = function()
            vim.g.vimwiki_global_ext = 0
            vim.g.vimwiki_list = { { path = '~/vimwiki/', syntax = 'markdown', ext = '.md' } }
        end,
    },
}
