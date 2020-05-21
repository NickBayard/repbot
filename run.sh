#!/usr/bin/env bash

pushd $HOME/dev/repbot/ 1> /dev/null

source $HOME/.virtualenvs/repbot-aB2DAUvq/bin/activate
export PYTHONPATH=$(pwd)/repbot/

python repbot/main.py --db repfit.db &>> log

deactivate

popd 1> /dev/null
