local split_and_alternate = function()
    local alt_file = vim.fn.expand('#')
    local this_file = vim.fn.expand('%')
    if alt_file == '' or this_file == alt_file then
        print('No alternate file available')
        return
    end
    vim.api.nvim_feedkeys(
        vim.api.nvim_replace_termcodes(
            ':vsplit ' .. this_file .. '<cr><c-w>h:e ' .. alt_file .. '<cr>',
            true,
            true,
            true
        ),
        'nt',
        true
    )
end

vim.keymap.set('n', '<c-s>', split_and_alternate)
