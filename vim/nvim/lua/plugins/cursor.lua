-- cursor.lua
-- Implement multi-cursor with vim-visual-multi

return {
    { 'vim-visual-multi', dir='~/.config/nvim/pack/vendor/opt/vim-visual-multi',
        keys = {{'<C-n>', mode = {'v', 'n'}}, '<C-Up>', '<C-Down>',
            '\\\\A', '\\\\\\'}
    }
}
