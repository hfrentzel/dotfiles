-- search.lua
-- Implements File and Text Search using nvim-telescope and commant-t

-- https://github.com/nvim-telescope/telescope.nvim/issues/1923
local function getVisualSelection()
    vim.cmd('noau normal! "vy"')
    local text = vim.fn.getreg('v')
    vim.fn.setreg('v', {})

    text = string.gsub(text, "\n", "")
    return (#text > 0) and text or ''
end

return {
    {'command-t', dir = '~/.config/nvim/pack/vendor/opt/command-t',
        keys = {
            { "<leader>t", '<Plug>(CommandTRipgrep)' },
            { '<leader>h', '<Plug>(CommandTHelp)'},
            { '<leader>b', '<Plug>(CommandTBuffer)'},
        },
        init = function()
            vim.g.CommandTPreferredImplementation='lua'
        end,
        config = function()
            vim.g.CommandTCancelMap = { '<Esc>', '<C-c>'}

            require('wincent.commandt').setup({
                always_show_dot_files = true,
                height = 30,
                mappings = {
                    i = {
                        ['<C-\\>'] = 'open_vsplit',
                    }
                }
            })
        end
    },

    {'telescope', dir = '~/.config/nvim/pack/vendor/opt/telescope.nvim',
        keys = {
            { '<leader>g', mode={'n', 'v'}},
            'gu'
        },
        config = function()
            require('telescope').setup({
                defaults = {
                    dynamic_preview_title = true,
                    mappings = {
                        i = {
                            ["<c-j>"] = "move_selection_next",
                            ["<c-k>"] = "move_selection_previous",
                            ["<c-\\>"] = "select_vertical",
                            ["<c-s>"] = "select_horizontal",
                        }
                    },
                    path_display = {truncate = 50},
                    -- Default includes --smart-case, I don't want that
                    vimgrep_arguments = {
                        "rg", "--color=never", "--no-heading", "--with-filename",
                        "--line-number", "--column"
                    },
                },
                pickers = {
                    live_grep = {
                        disable_coordinates = true,
                        prompt_title = 'Search in Files',
                        theme = "dropdown",
                        layout_config = {
                            anchor = 'N',
                            prompt_position = 'top',
                            width = 0.8,
                        }
                    },
                    lsp_references = {
                        theme = "dropdown",
                        layout_config = {
                            anchor = 'N',
                            prompt_position = 'top',
                            width = 0.8,
                        }
                    }
                }
            })
            local builtin = require('telescope.builtin')
            vim.keymap.set('n', '<leader>g', builtin.live_grep)
            vim.keymap.set('n', 'gu', builtin.lsp_references)
            vim.keymap.set('v', '<leader>g', function()
                local text = getVisualSelection()
                builtin.live_grep({default_text = text})
            end)
        end}
}
