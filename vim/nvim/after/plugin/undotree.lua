vim.cmd.packadd('nvim.undotree')
vim.api.nvim_create_user_command('Undotree', function()
    require('undotree').open({ command = 'leftabove 30vnew' })
end, {})
