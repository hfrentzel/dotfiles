if exists("b:current_syntax")
  finish
endif

runtime! syntax/confini.vim
unlet b:current_syntax

syn match awsSecret /\S\+/ contained conceal cchar=x

syn region secretLine oneline matchgroup=awsAccessKey start=/\(aws_access_key_id\|aws_secret_access_key\) = / skip=/\s*=\s*/ matchgroup=awsSeret end=/\n/ contains=awsSecret

hi def link awsSecret Type

let b:current_syntax = "aws"
