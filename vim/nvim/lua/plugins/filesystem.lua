-- filesystem.lua
-- Commands for working with files, featuring vim-eunuch

return (
    {'eunuch', dir='~/.config/nvim/pack/vendor/opt/eunuch/',
        cmd = {'Copy', 'Duplicate', 'Mkdir', 'Move',
            'Rename', 'Remove', 'SudoWrite'}
    }
)
