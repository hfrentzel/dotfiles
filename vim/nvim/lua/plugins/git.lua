-- git.lua
-- Git integrations using fugitive and gitsigns.nvim

-- https://github.com/tpope/vim-fugitive/issues/1474
local blame_toggle = function()
    local found = 0
    for _, winnr in pairs(vim.fn.range(1, vim.fn.winnr('$'))) do
        if vim.fn.getbufvar(vim.fn.winbufnr(winnr), '&filetype') == 'fugitiveblame' then
            vim.cmd.close({ count = winnr })
            found = 1
        end
    end
    if found == 0 then
        vim.cmd('Git blame')
    end
end

return {
    {
        'fugitive',
        dir = '~/.config/nvim/pack/vendor/opt/fugitive/',
        ft = 'gitcommit',
        cmd = { 'G', 'Git', 'Gvdiffsplit', 'Resolve' },
        keys = { '<c-b>' },
        config = function()
            vim.api.nvim_create_user_command(
                'Resolve',
                require('my_lua.merge_conflicts').setup_resolver,
                {}
            )
            vim.keymap.set('n', '<c-b>', blame_toggle)
        end,
    },
    {
        'gitsigns.nvim',
        dir = '~/.config/nvim/pack/vendor/opt/gitsigns.nvim/',
        event = { 'BufReadPost', 'BufNewFile' },
        opts = {
            signs = {
                add = {
                    hl = 'GitSignsAdd',
                    text = '+',
                    numhl = 'GitSignsAddNr',
                    linehl = 'GitSignsAddLn',
                },
                change = {
                    hl = 'GitSignsChange',
                    text = '~',
                    numhl = 'GitSignsChangeNr',
                    linehl = 'GitSignsChangeLn',
                },
                delete = {
                    hl = 'GitSignsDelete',
                    text = '-',
                    numhl = 'GitSignsDeleteNr',
                    linehl = 'GitSignsDeleteLn',
                },
            },
            _signs_staged_enable = true,
            on_attach = function(bufnr)
                local gs = package.loaded.gitsigns

                vim.keymap.set('n', ']c', function()
                    if vim.wo.diff then
                        return ']c'
                    end
                    vim.schedule(function()
                        gs.nav_hunk('next')
                    end)
                    return '<Ignore>'
                end, { buffer = bufnr, expr = true })

                vim.keymap.set('n', '[c', function()
                    if vim.wo.diff then
                        return '[c'
                    end
                    vim.schedule(function()
                        gs.nav_hunk('prev')
                    end)
                    return '<Ignore>'
                end, { buffer = bufnr, expr = true })

                vim.keymap.set('n', 'gh', gs.preview_hunk)
                vim.keymap.set('n', '<leader>v', function()
                    gs.blame_line({ full = true })
                end)
                vim.keymap.set('n', '<leader>c', gs.blame_line)
            end,
        },
    },
}
