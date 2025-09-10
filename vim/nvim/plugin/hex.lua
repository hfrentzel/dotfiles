-- https://vim.fandom.com/wiki/Convert_between_hex_and_decimal
vim.api.nvim_create_user_command('Hex2dec', function(args)
    if args.args == "" then
        local cmd
        if vim.startswith(vim.fn.histget(':', -1), "^'<,'>") and vim.fn.visualmode() == 'V' then
            cmd = 's/%V0x\\x+/=submatch(0)+0/g'
        else
            cmd = 's/0x\\x\\+/\\=submatch(0)+0/g'
        end
        vim.fn.execute(args.line1..','..args.line2..cmd)
    else
        if vim.startswith(args.args, '0x') then
            print(args.args + 0)
        else
            print(('0x' .. args.args) + 0)
        end
    end
end, { range = true, nargs = '?' })
