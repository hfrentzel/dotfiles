local diagnostics = function()
    local output = ""
    local no_problems = true
    if vim.b.diagnostic_counts == nil then
        return ""
    end
    if vim.b.diagnostic_counts.error > 0 then
        output = string.format("%%1*E %s", vim.b.diagnostic_counts.error)
        no_problems = false
    end
    if vim.b.diagnostic_counts.warning > 0 then
        output = string.format("%s %%2*W %s", output, vim.b.diagnostic_counts.warning)
        no_problems = false
    end
    if no_problems then
        return "✓"
    else
        return string.format('%s%%*', output)
    end
end

local status_rhs = function()
    return string.format('%s/%s, %s', vim.fn.line('.'), vim.fn.line('$'),
        vim.fn.virtcol('.'))
end

StandardStatusLine = function()
    vim.o.laststatus = 2
    return table.concat {
        vim.b.adjusted_path,
        "%3*%t%* %y",  -- filename and filetype
        "%=",
        diagnostics(),
        vim.b.git_branch or "",
        status_rhs(),
    }
end

local get_git_data = function()
    local run = function(cmd) return vim.fn.trim(vim.fn.system(cmd)) end
    local file_parent = vim.fn.expand('%:p:h')
    local git_prefix = string.format('git -C "%s"', file_parent)

    local root_path = nil
    local root_name = nil
    if vim.b.workspace ~= nil then
        root_path = vim.b.workspace
        root_name = '~'..vim.g.workspaces[vim.b.workspace]..'~'
    end

    local is_git_dir = run(git_prefix .. ' rev-parse --is-inside-work-tree')
    if is_git_dir == 'true' then
        local branch = run(git_prefix .. ' branch --show-current')
        vim.b.git_branch = string.format(' (%s) ', branch)

        if root_path == nil then
            root_path = run(git_prefix .. ' rev-parse --show-toplevel')
            local path_parts = vim.fn.split(root_path, '/')
            root_name = '~' .. path_parts[#path_parts] .. '~'
        end
    end

    if root_path ~= nil then
        vim.b.adjusted_path = root_name .. vim.fn.matchstr(
            file_parent, root_path..'\\zs.*\\ze')..'/'
    else
        vim.b.adjusted_path = file_parent..'/'
    end
end

vim.api.nvim_create_augroup('StatusLineData', {clear = true})
vim.api.nvim_create_autocmd({'BufEnter', 'FocusGained', 'BufWritePost'}, {
    group = 'StatusLineData',
    pattern = '*',
    callback = get_git_data
})

vim.api.nvim_create_augroup('FileTypes', {clear = true})
vim.api.nvim_create_autocmd('filetype', {
    group = 'FileTypes',
    pattern = '*',
    callback = function() vim.wo.statusline = string.format('%%!v:lua.StandardStatusLine()') end
})

