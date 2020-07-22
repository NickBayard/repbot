#!/usr/bin/env bash

pushd $HOME/dev/repbot/ 1> /dev/null

source $HOME/.virtualenvs/repbot-aB2DAUvq/bin/activate
export PYTHONPATH=$(pwd)/repbot/

echo "$(date)" &>> log
python repbot/main.py --db repfit.db --notify --user-info my_info.yaml &>> log

deactivate

popd 1> /dev/null
