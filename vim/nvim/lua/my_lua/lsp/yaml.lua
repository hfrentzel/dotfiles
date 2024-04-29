local M = {}

M.before_init = function(_, config)
    local filename = vim.fn.expand('~/.config/vim/schemas.json')
    if vim.fn.filereadable(filename) == 0 then
        return
    end
    local schema_file = io.open(filename)
    local schema_overrides = vim.fn.json_decode(schema_file:read('*a'))
    schema_file:close()

    config.settings.yaml.schemas = schema_overrides.all
    for dir, schemas in pairs(schema_overrides) do
        if dir == config.root_dir then
            config.settings.yaml.schemas =
                vim.tbl_extend('force', config.settings.yaml.schemas, schemas)
        end
    end
end

return M
