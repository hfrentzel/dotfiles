local statusline = {}

statusline.diagnostics = function()
    local b = vim.b
    local tree = require('nvim-treesitter.parsers').has_parser() and '🌳' or '🪓'
    local output = ''
    local no_problems = true
    if b.diags_ready ~= true then
        return tree
    end
    local counts = vim.diagnostic.count(vim.fn.winbufnr(0))
    if counts[1] ~= nil then
        output = string.format('%%1*E %s', counts[1])
        no_problems = false
    end
    if counts[2] ~= nil then
        output = string.format('%s %%2*W %s', output, counts[2])
        no_problems = false
    end
    if no_problems then
        return string.format('✓ %s', tree)
    else
        return string.format('%s%%* %s', output, tree)
    end
end

statusline.modified = function()
    local padding = vim.fn.getwininfo(vim.fn.win_getid())[1].textoff
    return (vim.bo.modified and '%4*' or '%5*') .. (' '):rep(padding) .. '%*'
end

statusline.status_rhs = function()
    return string.format('%s/%s, %s', vim.fn.line('.'), vim.fn.line('$'), vim.fn.col('.'))
end

statusline.determine_side = function()
    if vim.regex('//2'):match_str(vim.fn.expand('%')) then
        if vim.g.merge_type == 'MERGING' then
            return string.format("Branch '%s' being merged onto", vim.g.merge_head)
        else
            return 'New Parent commit'
        end
    else
        if vim.g.merge_type == 'MERGING' then
            return string.format("Branch '%s' trying to be merged", vim.g.merging_branch)
        else
            return 'Commit being rebased'
        end
    end
end

return statusline
