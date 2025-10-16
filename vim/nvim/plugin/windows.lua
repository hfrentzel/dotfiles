local split_and_alternate = function()
    local alt_file = vim.fn.expand('#')
    local this_file = vim.fn.expand('%')
    if alt_file == '' or this_file == alt_file then
        print('No alternate file available')
        return
    end
    vim.api.nvim_feedkeys(
        vim.api.nvim_replace_termcodes(':leftabove vsplit #<cr>', true, true, true),
        'nt',
        false
    )
end

vim.keymap.set('n', '<c-s>', split_and_alternate)

vim.keymap.set('n', '<leader>==', '<C-W>=')
vim.keymap.set('n', '<leader>=h', ':horizontal wincmd =<cr>', { silent = true })
vim.keymap.set('n', '<leader>=v', ':vertical wincmd =<cr>', { silent = true })
