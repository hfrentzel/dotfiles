vim.o.packpath = vim.o.runtimepath
vim.g.python3_host_prog = vim.fn.trim(vim.fn.system('which python'))
vim.g.loaded_ruby_provider = 0
vim.g.loaded_node_provider = 0
vim.g.loaded_perl_provider = 0
vim.g.rust_recommended_style = 0
vim.o.guicursor =
    'n-v-c-sm:block-blinkon500-blinkwait200,i-ci-ve:ver25-blinkon500,r-cr-o:hor20-blinkon500'

local confpath = ''
if vim.loop.os_uname().sysname == 'Linux' then
    confpath = '~/.config'
else
    confpath = '~/AppData/Local'
end
vim.cmd.source(confpath .. '/vim/vimrc')
vim.opt.rtp:prepend(confpath .. '/nvim/pack/lazy.nvim')

local function build_list(packages)
    local result = {}
    for _, package in ipairs(packages) do
        table.insert(result, { package, dev = true })
    end
    table.insert(result, { import = 'plugins' })
    return result
end

require('lazy').setup(
    build_list({
        'nvim-dap',
    }),
    {
        dev = {
            path = confpath .. '/nvim/pack',
        },
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

local localrc = vim.fn.expand('~/.config/vim/local.init.lua')
if vim.fn.filereadable(localrc) == 1 then
    vim.cmd.source(localrc)
end
