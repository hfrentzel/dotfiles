
complete -W "$(jq -r 'keys[]' ~/.test_configs)" tests

if [[ -x $(which aws) && -x $(which aws_completer) ]]; then
    complete -C "aws_completer" aws
fi

if [[ -x $(which jira) ]]; then
    source <(jira completion bash)
fi
