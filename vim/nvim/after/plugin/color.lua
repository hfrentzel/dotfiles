-- color.lua
-- This is a custom implementation of a colorscheme based on the base16
-- system and themes provided from https://github.com/tinted-theming/schemes.
-- The schemes provide 16 colors labeled 00 to 0F with the following purposes:
-- 00: default background
-- 01: lighter background (Statuses, line numbers)
-- 02: ligtherer background
-- 03: Comments
-- 04: Dark text color
-- 05: Default text color
-- 06: lighter text color
-- 07: lightest text color
-- 08: (Red) Variables
-- 09: (Orange) Numbers, Booleans, Constants
-- 0A: (Yellow) Classes, Tags
-- 0B: (Green) Strings
-- 0C: (Cyan) Regular Expressions, Info
-- 0D: (Blue) Functions, Methods
-- 0E: (Magenta) Keywords, Builtins
-- 0F: Deprecated
local scheme_dir = vim.fn.expand('~/dotfiles/appearance/schemes/base16/')

local function hi(group, args)
    local command = string.format(
        'highlight %s guifg=%s guibg=%s gui=%s guisp=%s',
        group,
        args.fg or 'NONE',
        args.bg or 'NONE',
        args.attr or 'NONE',
        args.sp or 'NONE'
    )
    vim.cmd(command)
end

local function setColor(scheme)
    if scheme == nil then
        local color_file = vim.fn.expand('~/.local/share/mysetup/base16')
        if vim.fn.filereadable(color_file) == 0 then
            return
        end

        scheme = vim.fn.readfile(color_file, '', 1)[1]
    end
    local scheme_file = scheme_dir .. scheme .. '.yaml'
    if vim.fn.filereadable(scheme_file) == 0 then
        vim.api.nvim_err_writeln('Bad scheme ' .. scheme)
    end

    local colors = {}
    for line in io.lines(scheme_file) do
        if line:find('  base', 1, true) == 1 then
            colors[string.sub(line, 7, 8)] = string.sub(line, 12, 18)
        end
    end
    hi('Comment', { fg = colors['03'], attr = 'italic' })

    hi('Operator', { fg = colors['05'] })

    hi('Identifier', { fg = colors['08'] })
    hi('Statement', { fg = colors['08'] })
    hi('@variable', { fg = colors['08'] })

    hi('Constant', { fg = colors['09'] })

    hi('Label', { fg = colors['0A'] })
    hi('PreProc', { fg = colors['0A'] })
    hi('Repeat', { fg = colors['0A'] })
    hi('Tag', { fg = colors['0A'] })
    hi('Type', { fg = colors['0A'] })

    hi('String', { fg = colors['0B'] })

    hi('Special', { fg = colors['0C'] })

    hi('Function', { fg = colors['0D'] })
    hi('Include', { fg = colors['0D'] })

    hi('Conditional', { fg = colors['0E'] })
    hi('Define', { fg = colors['0E'] })
    hi('Keyword', { fg = colors['0E'] })
    hi('Structure', { fg = colors['0E'] })

    hi('Delimiter', { fg = colors['0F'] })
    hi('SpecialChar', { fg = colors['0F'] })

    hi('Todo', { fg = colors['0A'], bg = colors['01'] })

    hi('Normal', { fg = colors['05'], bg = colors['00'] })
    hi('Bold', { attr = 'bold' })
    hi('Debug', { fg = colors['08'] })
    hi('Directory', { fg = colors['0D'] })
    hi('Error', { fg = colors['00'], bg = colors['08'] })
    hi('ErrorMsg', { fg = colors['08'], bg = colors['00'] })
    hi('Exception', { fg = colors['08'] })
    hi('FoldColumn', { fg = colors['0C'], bg = colors['01'] })
    hi('Folded', { fg = colors['03'], bg = colors['01'] })
    hi('IncSearch', { fg = colors['01'], bg = colors['09'], attr = 'none' })
    hi('Italic', { attr = 'italic' })
    hi('Macro', { fg = colors['08'] })
    hi('MatchParen', { bg = colors['03'] })
    hi('ModeMsg', { fg = colors['0B'] })
    hi('MoreMsg', { fg = colors['0B'] })
    hi('Question', { fg = colors['0D'] })
    hi('Search', { fg = colors['01'], bg = colors['0A'] })
    hi('Substitute', { fg = colors['01'], bg = colors['0A'] })
    hi('SpecialKey', { fg = colors['03'] })
    hi('TooLong', { fg = colors['08'] })
    hi('Underlined', { attr = 'underline' })
    hi('Visual', { bg = colors['02'] })
    hi('VisualNOS', { fg = colors['08'] })
    hi('WarningMsg', { fg = colors['08'] })
    hi('WildMenu', { fg = colors['08'], bg = colors['0A'] })
    hi('Title', { fg = colors['0D'] })
    hi('Conceal', { fg = colors['0D'], bg = colors['00'] })
    hi('Cursor', { fg = colors['00'], bg = colors['05'] })
    hi('NonText', { fg = colors['03'] })
    hi('LineNr', { fg = colors['03'], bg = colors['01'] })
    hi('SignColumn', { fg = colors['03'], bg = colors['01'] })
    hi('StatusLine', { fg = colors['04'], bg = colors['02'] })
    hi('StatusLineNC', { fg = colors['03'], bg = colors['01'] })
    hi('VertSplit', { fg = colors['03'], bg = colors['01'] })
    hi('ColorColumn', { bg = colors['01'] })
    hi('CursorColumn', { bg = colors['01'] })
    hi('CursorLine', { bg = colors['01'] })
    hi('CursorLineNr', { fg = colors['04'], bg = colors['01'] })
    hi('QuickFixLine', { bg = colors['01'] })
    hi('PMenu', { fg = colors['05'], bg = colors['01'], attr = 'none' })
    hi('PMenuSel', { fg = colors['01'], bg = colors['05'] })
    hi('TabLine', { fg = colors['03'], bg = colors['01'], attr = 'none' })
    hi('TabLineFill', { fg = colors['03'], bg = colors['01'], attr = 'none' })
    hi('TabLineSel', { fg = colors['0B'], bg = colors['01'], attr = 'none' })
    hi('NormalFloat', { bg = colors['01'] })

    hi('Added', { fg = colors['0B'], bg = colors['01'] })
    hi('Changed', { fg = colors['0D'], bg = colors['01'] })
    hi('Removed', { fg = colors['08'], bg = colors['01'] })
    hi('DiffFile', { fg = colors['08'], bg = colors['00'] })
    hi('DiffAdd', { fg = colors['01'], bg = colors['0B'] })
    hi('DiffAdded', { fg = colors['0B'], bg = colors['00'] })
    hi('DiffNewFile', { fg = colors['0B'], bg = colors['00'] })
    hi('DiffChange', { fg = colors['03'], bg = colors['01'] })
    hi('DiffDelete', { fg = colors['08'], bg = colors['01'] })
    hi('DiffRemoved', { fg = colors['08'], bg = colors['00'] })
    hi('DiffText', { fg = colors['0D'], bg = colors['01'] })
    hi('DiffLine', { fg = colors['0D'], bg = colors['00'] })

    hi('DiagnosticError', { fg = colors['08'] })
    hi('DiagnosticHint', { fg = colors['0D'] })
    hi('DiagnosticInfo', { fg = colors['0C'] })
    hi('DiagnosticOk', { fg = colors['0B'] })
    hi('DiagnosticWarn', { fg = colors['0A'] }) -- Was 0E

    hi('User1', { fg = colors['08'], bg = colors['02'] })
    hi('User2', { fg = colors['0A'], bg = colors['02'] })
    hi('User3', { fg = colors['04'], bg = colors['02'], attr = 'bold' })
    hi('User4', { bg = colors['08'] })
    hi('User5', { bg = colors['0B'] })
end

local function colorschemeCompletion(prefix)
    local schemes = {}

    local d, dd = vim.loop.fs_scandir(scheme_dir)
    while true do
        local name, type = vim.loop.fs_scandir_next(d, dd)
        if name == nil then
            break
        end
        if name == 'README.md' then
            goto continue
        end

        if type == 'file' and string.find(name, prefix, 1) == 1 then
            local scheme = string.gsub(name, '.yaml', '')
            table.insert(schemes, scheme)
        end
        ::continue::
    end
    return schemes
end

vim.api.nvim_create_user_command('Color', function(args)
    setColor(args.args)
end, {
    nargs = 1,
    complete = colorschemeCompletion,
})
vim.api.nvim_create_augroup('TermColor', { clear = true })
vim.api.nvim_create_autocmd('FocusGained', {
    group = 'TermColor',
    pattern = '*',
    callback = function()
        setColor()
    end,
})

setColor()
