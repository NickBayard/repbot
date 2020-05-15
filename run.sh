#!/usr/bin/env bash

pushd $HOME/dev/repbot/

export PYTHONPATH=$(pwd)/repbot/

pipenv run python repbot/main.py --db repfit.db &>> log

popd
