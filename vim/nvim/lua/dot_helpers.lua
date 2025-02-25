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

return functions
