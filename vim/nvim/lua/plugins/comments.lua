-- comments.lua
-- Implements comment toggling with tcomment_vim

return {
    {
        'tcomment_vim',
        dir = '~/.config/nvim/pack/vendor/opt/tcomment_vim',
        keys = {
            { '<c-_>', ':TComment<cr>', silent = true },
            { '<c-_>', ':TCommentMaybeInline<cr>', mode = 'v', silent = true },
        },
        init = function()
            vim.g.tcomment_maps = 0
            vim.g.tcomment_opleader = ''
        end,
    },
}
