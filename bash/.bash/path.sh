add_to_path() {
    new_dir=$1
    PATH=${PATH//":$new_dir:"/:}
    PATH=${PATH/#"$new_dir:"/}
    PATH=${PATH/%":$new_dir"/}
    PATH="$new_dir${PATH:+:$PATH}"
}

add_to_path "$HOME/.local/bin"
add_to_path "$HOME/.bin"
add_to_path "$HOME/.cargo/bin"

export GOROOT=/usr/local/go
export GOPATH=$HOME/go

add_to_path "$GOPATH/bin:$GOROOT/bin"

