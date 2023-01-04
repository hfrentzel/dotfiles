has_nvim_tree, api = pcall(require, 'nvim-tree.api')
if not has_nvim_tree then
    return
end

-- Open an NvimTree window replacing the current buffer
vinegar_open = function()
    local core = require'nvim-tree.core'
    local view = require"nvim-tree.view"
    vim.g.curr_file = vim.fn.expand('%')
    if vim.api.nvim_buf_get_name(vim.api.nvim_get_current_buf()) == '' then
        -- based off of nvim-tree.open_replacing_current_buffer but can
        -- be used when current buffer is unnamed
        cwd = vim.fn.fnamemodify('', ':p:h')
        if not core.get_explorer() or cwd ~= core.get_cwd() then
           core.init(cwd)
        end
        view.open_in_current_win({
            hijack_current_buf = false, resize = false
        })
        require"nvim-tree.renderer".draw()
    else
        require"nvim-tree".open_replacing_current_buffer()
    end
    vim.b.curr_file = vim.g.curr_file
end

-- Close a NvimTree buffer that had been opened with vinegar_open
-- and go back to previous buffer
close_tree = function()
    if vim.b.curr_file ~= '' then
        require("nvim-tree.actions.node.open-file").fn(
            "edit_in_place", vim.b.curr_file)
    elseif vim.b.curr_file == '' then 
        vim.api.nvim_feedkeys(
            vim.api.nvim_replace_termcodes('<c-6>', true, true, true),
            'n', true
        )
    else
        api.tree.close()
    end
end

-- Open the file and replace the NvimTree buffer if opened with
-- vinegar_open, otherwise just open normally
open_or_replace = function()
    if vim.b.curr_file then
        api.node.open.replace_tree_buffer()
    else
        api.node.open.edit()
    end
end
    
require('nvim-tree').setup({
    actions = {
        open_file = {
            -- quit_on_open = true
        }
    },
    filters = {
        dotfiles = false
    },
    renderer =  {
        icons = {
            glyphs = {
                folder = {
                    arrow_closed = '▸',
                    arrow_open = '▾'
                }
            },
            show = {
                file = false,
                folder = false
            }
        },
    },
    view = {
        mappings = {
            list = {
                { key = '-', action='xx', action_cb=close_tree},
                { key = '<cr>', action='xxx', action_cb=open_or_replace},
                { key = 'u', action='dir_up'},
            }
        }
    }
})
vim.keymap.set('n', '<leader>1', ':NvimTreeFocus<CR>', {silent = true})
vim.keymap.set('n', '-', '<cmd>lua vinegar_open()<CR>', {silent = true})