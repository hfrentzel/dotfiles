vim.o.packpath = vim.o.runtimepath
vim.g.python3_host_prog = vim.fn.trim(vim.fn.system('which python'))
vim.g.loaded_ruby_provider = 0
vim.g.loaded_node_provider = 0
vim.g.loaded_perl_provider = 0
vim.g.rust_recommended_style = 0
vim.cmd.source('~/.config/vim/vimrc')

vim.o.guicursor =
    'n-v-c-sm:block-blinkon500-blinkwait200,i-ci-ve:ver25-blinkon500,r-cr-o:hor20-blinkon500'

local lazypath = '~/.config/nvim/pack/vendor/opt/lazy.nvim'
vim.opt.rtp:prepend(lazypath)

local function build_list(packages)
    local result = {}
    for _, package in ipairs(packages) do
        table.insert(result, { package, dir = '~/.config/nvim/pack/vendor/opt/' .. package })
    end
    table.insert(result, { import = 'plugins' })
    return result
end

require('lazy').setup(
    build_list({
        'nvim-dap',
    }),
    {
        performance = {
            rtp = {
                disabled_plugins = {
                    'matchit',
                    'matchparen',
                    'netrwPlugin',
                    'rplugin',
                    'tutor',
                    'tohtml',
                },
            },
        },
    }
)

local localrc = vim.fn.expand("~/.config/vim/local.init.lua")
if vim.fn.filereadable(localrc) == 1 then
    vim.cmd.source(localrc)
end
