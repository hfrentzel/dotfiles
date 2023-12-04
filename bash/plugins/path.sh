add_to_path() {
    new_dir=$1
    PATH=${PATH//":$new_dir:"/:}
    PATH=${PATH/#"$new_dir:"/}
    PATH=${PATH/%":$new_dir"/}
    PATH="$new_dir${PATH:+:$PATH}"
}

add_to_path "$HOME/.local/bin"
add_to_path "$HOME/.local/share/cargo/bin"

export GOBIN="$HOME/.local/bin"
export GOMODCACHE="$HOME/.cache/go/mod"
export GOPATH="$HOME/.local/share/go"

if command -v $HOME/.local/go/bin/go &> /dev/null; then
    export GOROOT="$HOME/.local/go"
else
    export GOROOT="usr/local/go"
fi

add_to_path "$GOROOT/bin"
