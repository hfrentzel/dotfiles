local functions = {}

functions.get_python_major_version = function(pyvenv_file)
    for line in io.lines(pyvenv_file) do
        local version = vim.fn.matchstr(line, 'version = \\zs\\d.\\d')
        if version ~= '' then
            return version
        end
    end
    return nil
end

functions.get_git_root = function()
    local git_prefix = 'git -C ' .. vim.fn.expand('%:p:h')
    if vim.fn.system(git_prefix .. ' rev-parse  --is-inside-work-tree') then
        return vim.fn.substitute(
            vim.fn.system(git_prefix .. ' rev-parse --show-toplevel'),
            '\n',
            '',
            'g'
        )
    end
end

return functions
