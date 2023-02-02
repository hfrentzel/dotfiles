has_gitsigns, gitsigns = pcall(require, 'gitsigns')
if not has_gitsigns then
    return
end

gitsigns.setup{
    signs = {
        add = {hl = 'GitSignsAdd', text = '+', numhl='GitSignsAddNr',
               linehl='GitSignsAddLn'},
        change = {hl = 'GitSignsChange', text = '~', numhl='GitSignsChangeNr',
                  linehl='GitSignsChangeLn'},
        delete = {hl = 'GitSignsDelete', text = '-', numhl='GitSignsDeleteNr',
                  linehl='GitSignsDeleteLn'}
    },
    _signs_staged_enable = true,
    on_attach = function(bufnr)
        local gs = package.loaded.gitsigns

        vim.keymap.set('n', ']c', function()
            if vim.wo.diff then return ']c' end
            vim.schedule(function() gs.next_hunk() end)
            return '<Ignore>'
        end, {buffer = bufnr, expr=true})

        vim.keymap.set('n', '[c', function()
            if vim.wo.diff then return '[c' end
            vim.schedule(function() gs.prev_hunk() end)
            return '<Ignore>'
        end, {buffer = bufnr, expr=true})

        vim.keymap.set('n', 'gh', gs.preview_hunk)
        vim.keymap.set('n', '<leader>v', function() gs.blame_line({full=true}) end)
        vim.keymap.set('n', '<leader>c', gs.blame_line)

    end
}
