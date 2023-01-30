local mappings = {
    {'e', 'f' },
    {'E', 'F' },
    {'r', 'p' },
    {'R', 'P' },
    {'t', 'g' },
    {'T', 'G' },
    {'y', 'j' },
    {'Y', 'J' },
    {'u', 'l' },
    {'U', 'L' },
    {'i', 'u' },
    {'I', 'U' },
    {'o', 'y' },
    {'O', 'Y' },
    {'p', ';' },
    {'P', ':' },
    {'s', 'r' },
    {'S', 'R' },
    {'d', 's' },
    {'D', 'S' },
    {'f', 't' },
    {'F', 'T' },
    {'g', 'd' },
    {'G', 'D' },
    {'j', 'n' },
    {'J', 'N' },
    {'k', 'e' },
    {'K', 'E' },
    {'l', 'i' },
    {'L', 'I' },
    {';', 'o' },
    {':', 'O' },
    {'n', 'k' },
    {'N', 'K' }
}

function set_colemak()
    for _, mapping in ipairs(mappings) do
        vim.keymap.set({'i', 'c'}, mapping[1], mapping[2])
    end
end

function unset_colemak()
    for _, mapping in ipairs(mappings) do
        vim.keymap.del({'i', 'c'}, mapping[1])
    end
end

-- set_colemak()
vim.api.nvim_create_user_command('SetColemak', 'lua set_colemak()<cr>', {})
vim.api.nvim_create_user_command('UnsetColemak', 'lua unset_colemak()<cr>', {})
