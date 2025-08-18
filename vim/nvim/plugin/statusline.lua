local StandardStatusLine = function()
    return table.concat({
        "%{%v:lua.require('my_lua.statusline').modified()%}",
        '%{get(b:,"adjusted_path","")}',
        '%3*%t%* %y', -- filename and filetype
        '%=',
        "%{%v:lua.require('my_lua.statusline').diagnostics()%}",
        ' (%{get(b:,"git_branch","")}) ',
        "%{v:lua.require('my_lua.statusline').status_rhs()}",
    })
end

local FugitiveStatusLine = function()
    return table.concat({
        '%3*%t%* %y ', -- filename and filetype
        "%{v:lua.require('my_lua.statusline').determine_side()}",
        '%=',
        "%{v:lua.require('my_lua.statusline').status_rhs()}",
    })
end

local get_git_data = function()
    local run = function(cmd)
        return vim.fn.trim(vim.fn.system(cmd))
    end
    local file_parent = vim.fn.expand('%:p:h')
    local git_prefix = string.format('git -C "%s"', file_parent)

    local root_path = nil
    local root_name = nil
    if vim.b.workspace ~= nil then
        root_path = vim.b.workspace
        root_name = '~' .. vim.g.workspaces[vim.b.workspace] .. '~'
    end

    local is_git_dir = run(git_prefix .. ' rev-parse --is-inside-work-tree')
    if is_git_dir == 'true' then
        vim.b.git_branch = run(git_prefix .. ' branch --show-current')

        if root_path == nil then
            root_path = run(git_prefix .. ' rev-parse --show-toplevel')
            vim.b.git_root = root_path
            local path_parts = vim.fn.split(root_path, '/')
            root_name = '~' .. path_parts[#path_parts] .. '~'
        end
    end

    if root_path ~= nil then
        local final_slash = '/'
        if vim.fn.has('macunix') ~= 1 then
            final_slash = '\\'
            root_path = string.gsub(root_path, '/', '\\\\')
        end
        vim.b.adjusted_path = root_name
            .. vim.fn.matchstr(file_parent, root_path .. '\\zs.*\\ze')
            .. final_slash
    else
        vim.b.adjusted_path = file_parent .. '/'
    end
end

vim.api.nvim_create_augroup('StatusLineData', { clear = true })
vim.api.nvim_create_autocmd({ 'BufEnter', 'FocusGained', 'BufWritePost' }, {
    group = 'StatusLineData',
    pattern = '*',
    callback = get_git_data,
})

vim.api.nvim_create_augroup('FileTypes', { clear = true })
vim.api.nvim_create_autocmd('filetype', {
    group = 'FileTypes',
    pattern = '*',
    callback = function()
        vim.o.laststatus = 2
        if vim.regex('fugitive:///.*//[23]/.*'):match_str(vim.fn.expand('%')) then
            vim.wo.statusline = FugitiveStatusLine()
        else
            vim.wo.statusline = StandardStatusLine()
        end
    end,
})
