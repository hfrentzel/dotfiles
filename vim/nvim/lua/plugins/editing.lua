-- editing.lua
-- Shortcuts and features designed to speed up text editing and manipulation
-- Currently includes vim-surround and CamelCaseMotion

return {
    {'vim-sleuth', dir='~/.config/nvim/pack/vendor/opt/vim-sleuth'},
    {'vim-surround', dir='~/.config/nvim/pack/vendor/opt/vim-surround',
        event='VeryLazy'},
    {'CamelCaseMotion', dir='~/.config/nvim/pack/vendor/opt/CamelCaseMotion',
        keys = {
            {'i<leader>w' , '<Plug>CamelCaseMotion_iw', mode={'o', 'x'}}
        }
    }
}
