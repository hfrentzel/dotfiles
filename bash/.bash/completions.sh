
test -f ~/.test_configs && complete -W "$(jq -r 'keys[]' ~/.test_configs)" tests

if [[ -x $(which aws) && -x $(which aws_completer) ]]; then
    complete -C "aws_completer" aws
fi

if [[ -x $(which jira) ]]; then
    source <(jira completion bash)
fi

if [[ -x $(which gh) ]]; then
    eval "$(gh completion -s bash)"
fi

command -v kubectl &> /dev/null && source <(kubectl completion bash) \
    && complete -o default -F __start_kubectl kb
