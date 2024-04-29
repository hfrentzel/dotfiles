-- folds.lua
-- A custom foldtext function that shows the first line in the fold and the
-- number of lines inside

_G.foldtext = function()
    local line = vim.fn.getline(vim.v.foldstart)
    local fold_size = (vim.v.foldend - vim.v.foldstart + 1) .. ' lines'
    local width = vim.fn.winwidth(0)
        - vim.fn.getwininfo(vim.fn.win_getid())[1].textoff
        - string.len(fold_size)

    if string.len(line) > width then
        line = string.sub(line, 1, width)
    elseif string.len(line) < width then
        line = line .. string.rep('·', width - string.len(line))
    end

    return line .. fold_size
end

vim.opt.foldtext = 'v:lua.foldtext()'
