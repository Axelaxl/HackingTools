#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    sw_vers

    git clone --depth 1 https://github.com/yyuu/pyenv.git ~/.pyenv
    PYENV_ROOT="$HOME/.pyenv"
    PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    pyenv install $PYTHON_VERSION
    pyenv global $PYTHON_VERSION
    pyenv rehash

    pip install --user --upgrade pip
    pip install --user virtualenv
    python -m virtualenv ~/.venv
    source ~/.venv/bin/activate
fi

pip install -r requirements-dev.txt
