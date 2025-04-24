
test -f ~/.test_configs && complete -W "$(jq -r 'keys[]' ~/.test_configs)" tests
