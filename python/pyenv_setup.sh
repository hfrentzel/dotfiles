DESIRED_VERSIONS=('3.10' '3.9' '3.8' '2.7') 

if [ ! -d $HOME/.pyenv ]; then
    curl https://pyenv.run | bash
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
fi
SET_GLOBAL="pyenv global"

ALL_VERSIONS=$(pyenv install --list)
INSTALLED_VERSIONS=$(pyenv versions)
for i in "${DESIRED_VERSIONS[@]}"; do
    MOST_RECENT_VERSION=$(echo "$ALL_VERSIONS" | grep "^  $i" | tail -n 1 | sed 's/ *//g')
    if [ -z "$(echo "$INSTALLED_VERSIONS" | grep "$MOST_RECENT_VERSION")" ]; then
        echo "Installing Python $MOST_RECENT_VERSION"
        pyenv install $MOST_RECENT_VERSION
    fi
    SET_GLOBAL="$SET_GLOBAL $MOST_RECENT_VERSION"
done

eval "$SET_GLOBAL"

