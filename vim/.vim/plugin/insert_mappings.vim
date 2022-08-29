" Navigate while in insert mode
inoremap <c-h> <left>
inoremap <c-j> <down>
inoremap <c-k> <up>
inoremap <c-l> <right>


" Mappings to handle auto brackets
let s:bracket_pairs = {'{': '}', '[': ']', '(': ')'}

function! ConditionalPairMap(open, close) abort
    let line = getline('.')
    let col = col('.')
    if col < col('$') && index(values(s:bracket_pairs), strpart(line, col-1, 1)) < 0
        return a:open
    else
        return a:open . a:close . "\<left>"
    endif
endfunction

for [open, close] in items(s:bracket_pairs)
    " Add closing bracket after open bracket when EOL or inside bracket pair
    execute "inoremap <expr> ".open." ConditionalPairMap('".open."', '".close."')"

    " Add closing bracket on new line after open bracket + <CR>
    execute "inoremap ".open."<cr> "open."<cr>".close."<esc>O"

    " Jump over existing closing bracket when typing closing bracket 
    execute "inoremap <expr> ".close." strpart(getline('.'), col('.')-1, 1)
                \ == '".close."' ? '\<Right>' : '".close."'"
endfor

"Remove pair when backspacing inside empty pair
function BracketBS()
    let pair = getline('.')[col('.')-2 : col('.') -1]
    return stridx('()[]{}', pair) % 2 == 0 ? "\<del>\<c-h>" : "\<bs>"
endfunction

inoremap <silent> <BS> <C-R>=BracketBS()<CR>

