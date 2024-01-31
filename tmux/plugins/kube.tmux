#!/usr/bin/env bash
if ! command -v kubectl ; then
    exit
fi

CONTEXT="$(kubectl config current-context 2>/dev/null)"
NAMESPACE="$(kubectl config view --minify --output 'jsonpath={..namespace}' 2>/dev/null)"
NAMESPACE="${NAMESPACE:-default}"

local MSG
MSG+="#[fg=black]$(echo $'\u2388 ')"
MSG+="#[fg=black]$CONTEXT:$NAMESPACE"

echo "$MSG"
