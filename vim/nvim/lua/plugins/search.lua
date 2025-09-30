-- search.lua
-- Implements File and Text Search using snacks.nvim and command-t

vim.api.nvim_set_hl(0, 'SnacksPicker', { link = 'Normal' })
vim.api.nvim_set_hl(0, 'SnacksPickerSearch', { link = 'NormalNC' })

return {
    {
        'command-t',
        dev = true,
        keys = {
            { '<leader>t', '<Plug>(CommandTRipgrep)' },
            { '<leader>h', '<Plug>(CommandTHelp)' },
            { '<leader>b', '<Plug>(CommandTBuffer)' },
        },
        init = function()
            vim.g.CommandTPreferredImplementation = 'lua'
        end,
        config = function()
            vim.g.CommandTCancelMap = { '<Esc>', '<C-c>' }

            require('wincent.commandt').setup({
                always_show_dot_files = true,
                height = 30,
                match_listing = { border = 'rounded' },
                prompt = { border = 'rounded' },
                traverse = 'pwd',
                mappings = {
                    i = {
                        ['<C-\\>'] = 'open_vsplit',
                    },
                },
            })
        end,
    },
    {
        'snacks.nvim',
        dev = true,
        keys = {
            {
                '<leader>g',
                function()
                    require('snacks').picker.grep()
                end,
                mode = 'n',
            },
            {
                '<leader>g',
                function()
                    require('snacks').picker.grep({
                        search = function(picker)
                            return picker:word()
                        end,
                    })
                end,
                mode = 'v',
            },
            {
                'gu',
                function()
                    require('snacks').picker.lsp_references()
                end,
            },
            {
                'gd',
                function()
                    require('snacks').picker.lsp_definitions()
                end,
            },
        },
        opts = {
            picker = {
                prompt = '',
                icons = {
                    files = { enabled = false },
                },
                layout = {
                    layout = {
                        backdrop = false,
                        row = 1,
                        width = 0.8,
                        min_width = 80,
                        height = 0.95,
                        min_height = 30,
                        box = 'vertical',
                        {
                            title = '{title} {flags}',
                            border = 'rounded',
                            box = 'vertical',
                            { win = 'input', height = 1 },
                            { win = 'list', border = 'top' },
                        },
                        { win = 'preview', title = '{preview}', height = 0.6, border = 'rounded' },
                    },
                },
                sources = {
                    grep = {
                        title = 'Search in files',
                        ignore = true,
                        ignore_case = false,
                        live = true,
                        toggles = {
                            ignore = { icon = '--no-ignore', value = false },
                            ignore_case = '--ignore-case',
                        },
                        finder = function(opts, ctx)
                            local new_args = { '--case-sensitive' }
                            if not opts.ignore then
                                vim.list_extend(new_args, { '--no-ignore' })
                            end
                            if opts.ignore_case then
                                vim.list_extend(new_args, { '--ignore-case' })
                            end
                            opts.args = new_args
                            return require('snacks.picker.source.grep').grep(opts, ctx)
                        end,
                        actions = {
                            toggle_ignore_case = function(picker)
                                picker.opts.ignore_case = not picker.opts.ignore_case
                                picker:find()
                            end,
                            toggle_ignore = function(picker)
                                picker.opts.ignore = not picker.opts.ignore
                                picker:find()
                            end,
                        },
                        win = {
                            input = {
                                keys = {
                                    ['<M-i>'] = { 'toggle_ignore', mode = { 'i', 'n' } },
                                    ['<M-s>'] = { 'toggle_ignore_case', mode = { 'i', 'n' } },
                                    ['<C-j>'] = { 'list_down', mode = { 'i', 'n' } },
                                    ['<C-k>'] = { 'list_up', mode = { 'i', 'n' } },
                                    ['<C-\\>'] = { 'edit_vsplit', mode = { 'i', 'n' } },
                                    ['<C-s>'] = { 'edit_split', mode = { 'i', 'n' } },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
