local M = {}

M.before_init = function(_, config)
    local helpers = require('dot_helpers')
    local has_path, util = pcall (require, 'lspconfig/util')

    if not has_path then
        return
    end
    local path = util.path

    local jedi_args = {} -- object
    local mypy_args = {"--namespace-packages"} -- array
    local pylint_args = {} -- array

    local venv_cfg = vim.fn.glob(path.join(config.root_dir, '*', 'pyvenv.cfg'))
    if venv_cfg ~= '' then
        local venv_dir = path.dirname(venv_cfg)
        jedi_args.environment = venv_dir
        table.insert(mypy_args, "--python-executable")
        table.insert(mypy_args, path.join(venv_dir, 'bin', 'python'))

        local version = helpers.get_python_major_version(venv_cfg)
        table.insert(mypy_args, "--python-version")
        table.insert(mypy_args, version)
        table.insert(pylint_args, '--py-version='..version)

        local site_pkg_dir = vim.fn.glob(path.join(venv_dir, 'lib/*/site-packages/'))
        if site_pkg_dir ~= '' then
            table.insert(pylint_args, "--init-hook=\"import sys; sys.path.extend(['"
                ..site_pkg_dir.."', '"..config.root_dir.."'])\"")
        elseif config.root_dir then
            table.insert(pylint_args, "--init-hook=\"import sys; sys.path.append('"
                ..config.root_dir.."')\"")
        end
    end

    table.insert(mypy_args, true) -- default args should also be passed in
    if next(jedi_args) ~= nil then
        config.settings.pylsp.plugins.jedi = jedi_args
    end
    config.settings.pylsp.plugins.pylint.args = pylint_args
    config.settings.pylsp.plugins.pylsp_mypy.overrides = mypy_args
end


return M
