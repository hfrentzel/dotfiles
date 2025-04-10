-- cursor.lua
-- Implement multi-cursor with vim-visual-multi

return {
    {
        'vim-visual-multi',
        dev = true,
        keys = { { '<C-n>', mode = { 'v', 'n' } }, '<C-Up>', '<C-Down>', '\\\\A', '\\\\\\' },
    },
}
