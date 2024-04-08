local M = {}

local git_state = function()
    vim.g.merge_type = nil
    local git_path = vim.b.git_root .. '/.git/'
    if vim.fn.filereadable(git_path..'MERGE_HEAD') ~= 0 then
        vim.g.merge_type = 'MERGING'

        vim.g.merging_branch = vim.fn.matchstr(vim.fn.readfile(
            git_path..'MERGE_MSG')[1], "Merge branch '\\zs.*\\ze'")
        vim.g.merge_head = vim.b.git_branch
    elseif vim.fn.isdirectory(git_path..'rebase-merge') ~= 0 or
        vim.fn.isdirectory(git_path..'rebase-apply') then
        vim.g.merge_type = 'REBASING'
    end
    return vim.g.merge_type
end

local clear_git_state = function()
    vim.g.merge_type = nil
    vim.g.merging_branch = nil
    vim.g.merge_head = nil
end

vim.api.nvim_create_augroup('MergeResolve', {clear = true})
vim.api.nvim_create_autocmd('BufReadPost', {
    group = 'MergeResolve',
    pattern = 'fugitive:///*//[23]/*',
    callback = function() vim.bo.modifiable = false end
})

local conflict_regex = '^\\(@@ .* @@\\|[<=>|]\\{7}[<=>|]\\@!\\)'
local next_conflict_marker = function() vim.fn.search(conflict_regex) end
local prev_conflict_marker = function() vim.fn.search(conflict_regex, 'b') end

local teardown_resolver = function()
    local buf = vim.g.merging_buffer
    vim.keymap.del({'n', 'x', 'o'}, ']n', {buffer = buf})
    vim.keymap.del({'n', 'x', 'o'}, '[n', {buffer = buf})
    vim.keymap.del('n', 'dh', {buffer = true})
    vim.keymap.del('n', 'dl', {buffer = true})
    vim.api.nvim_del_user_command('Finish')
    vim.bo[buf].readonly = false
    for _, winid in pairs(vim.api.nvim_list_wins()) do
        local filename = vim.api.nvim_buf_get_name(vim.api.nvim_win_get_buf(winid))
        if vim.fn.match(filename, '^fugitive://') ~= -1 then
            vim.api.nvim_win_close(winid, false)
        end
    end
    vim.g.merging_buffer = nil
    clear_git_state()
    vim.api.nvim_buf_call(buf, function() vim.cmd.write() end)

    if vim.g.opened_with_mt == 1 then
        vim.cmd.quit()
    end
end

M.setup_resolver = function()
    if git_state() == nil then
        print('No rebase or merge in progress')
        return
    end
    vim.g.merging_buffer = vim.fn.bufnr()
    vim.bo.readonly = true
    vim.cmd(':Gvdiffsplit!')
    vim.keymap.set({'n', 'x', 'o'}, '[n', prev_conflict_marker, {buffer = true})
    vim.keymap.set({'n', 'x', 'o'}, ']n', next_conflict_marker, {buffer = true})
    vim.keymap.set('n', 'dh', ':diffget //2<CR>', {buffer = true})
    vim.keymap.set('n', 'dl', ':diffget //3<CR>', {buffer = true})
    vim.api.nvim_create_user_command('Finish', teardown_resolver, {})
end

return M
