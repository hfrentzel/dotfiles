-- search.lua
-- Implements File and Text Search using snacks.nvim

vim.api.nvim_set_hl(0, 'SnacksPicker', { link = 'Normal' })
vim.api.nvim_set_hl(0, 'SnacksPickerSearch', { link = 'NormalNC' })

local layout_no_preview = {
    backdrop = false,
    row = 1,
    width = 0.8,
    min_width = 80,
    height = 0.8,
    min_height = 30,
    box = 'vertical',
    {
        title = '{title} {flags}',
        border = 'rounded',
        box = 'vertical',
        { win = 'input', height = 1 },
        { win = 'list', border = 'top' },
    },
}

local layout = vim.deepcopy(layout_no_preview)
table.insert(layout, { win = 'preview', title = '{preview}', height = 0.6, border = 'rounded' })
layout.height = 0.95

local ignore_actions = {
    toggle_ignore_case = function(picker)
        picker.opts.ignore_case = not picker.opts.ignore_case
        picker:find()
    end,
    toggle_ignore = function(picker)
        picker.opts.ignore = not picker.opts.ignore
        picker:find()
    end,
}

local get_ignore_args = function(opts)
    local new_args = { '--hidden', '--case-sensitive' }
    if not opts.ignore then
        vim.list_extend(new_args, { '--no-ignore' })
    end
    if opts.ignore_case then
        vim.list_extend(new_args, { '--ignore-case' })
    end
    return new_args
end

return {
    {
        'snacks.nvim',
        dev = true,
        keys = {
            {
                '<leader>t',
                function()
                    if vim.fn.mode() == 'n' then
                        require('snacks').picker.files()
                    else
                        require('snacks').picker.files({
                            pattern = function(picker)
                                return picker:word()
                            end,
                        })
                    end
                end,
                mode = { 'n', 'v' },
            },
            {
                '<leader>g',
                function()
                    if vim.fn.mode() == 'n' then
                        require('snacks').picker.grep()
                    else
                        require('snacks').picker.grep({
                            search = function(picker)
                                return picker:word()
                            end,
                        })
                    end
                end,
                mode = { 'n', 'v' },
            },
            {
                '<leader>b',
                function()
                    require('snacks').picker.buffers()
                end,
            },
            {
                '<leader>h',
                function()
                    require('snacks').picker.help()
                end,
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
                    layout = layout,
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
                sources = {
                    buffers = {
                        layout = { layout = layout_no_preview },
                    },
                    help = {
                        layout = { layout = layout_no_preview },
                        sort = { fields = { 'score:desc', 'text' } },
                        matcher = {
                            sort_empty = true,
                        },
                    },
                    files = {
                        title = 'Find file',
                        ignore = true,
                        ignore_case = false,
                        layout = { layout = layout_no_preview },
                        toggles = {
                            ignore = { icon = '--no-ignore', value = false },
                            ignore_case = '--ignore-case',
                        },
                        finder = function(opts, ctx)
                            opts.args = get_ignore_args(opts)
                            return require('snacks.picker.source.files').files(opts, ctx)
                        end,
                        actions = ignore_actions,
                    },
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
                            opts.args = get_ignore_args(opts)
                            return require('snacks.picker.source.grep').grep(opts, ctx)
                        end,
                        actions = ignore_actions,
                    },
                },
            },
        },
    },
}
