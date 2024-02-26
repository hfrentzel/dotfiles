statusline = {}

statusline.diagnostics = function()
    local b = vim.b
    local output = ""
    local no_problems = true
    if b.diagnostic_counts == nil then
        return ""
    end
    if b.diagnostic_counts.error > 0 then
        output = string.format("%%1*E %s", b.diagnostic_counts.error)
        no_problems = false
    end
    if b.diagnostic_counts.warning > 0 then
        output = string.format("%s %%2*W %s", output, b.diagnostic_counts.warning)
        no_problems = false
    end
    if no_problems then
        return "✓"
    else
        return string.format('%s%%*', output)
    end
end

statusline.status_rhs = function()
    return string.format('%s/%s, %s', vim.fn.line('.'), vim.fn.line('$'),
        vim.fn.col('.'))
end

statusline.determine_side = function()
    if vim.regex('//2'):match_str(vim.fn.expand('%')) then
        return string.format("Branch '%s' being merged onto", vim.g.merge_head)
    else
        return string.format("Branch '%s' trying to be merged", vim.g.merging_branch)
    end
end

return statusline
