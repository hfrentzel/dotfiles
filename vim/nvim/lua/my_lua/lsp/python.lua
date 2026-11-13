local M = {}

M.before_init = function(_, config)
    local helpers = require('dot_helpers')

    local jedi_args = {} -- object
    local mypy_args = { '--namespace-packages' } -- array

    local venv_cfg = vim.fn.glob(vim.fs.joinpath(config.root_dir, '*', 'pyvenv.cfg'))
    if venv_cfg ~= '' then
        local venv_dir = vim.fs.dirname(venv_cfg)
        jedi_args.environment = venv_dir
        table.insert(mypy_args, '--python-executable')
        table.insert(mypy_args, vim.fs.joinpath(venv_dir, 'bin', 'python'))

        local version = helpers.get_python_major_version(venv_cfg)
        table.insert(mypy_args, '--python-version')
        table.insert(mypy_args, version)
    end

    table.insert(mypy_args, true) -- default args should also be passed in
    if next(jedi_args) ~= nil then
        config.settings.pylsp.plugins.jedi = jedi_args
    end
    config.settings.pylsp.plugins.pylsp_mypy.overrides = mypy_args
end

return M
