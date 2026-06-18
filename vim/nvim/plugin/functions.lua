vim.api.nvim_create_user_command('Hex2dec', function(args)
    require('my_lua.transformers').hex2dec(args)
end, { range = true, nargs = '?' })

vim.api.nvim_create_user_command('UrlEncode', function()
    require('my_lua.transformers').urlencode()
end, { range = true })

vim.api.nvim_create_user_command('Insort', function()
    require('my_lua.transformers').insort()
end, {})

vim.ui.select = function(...)
    require('my_lua.ui_select').select(...)
end
