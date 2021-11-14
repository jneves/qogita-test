#! /bin/bash

set -e

ARGS=""
if [ "$1" == "--upgrade" ]; then
    ARGS="-U"
fi

pip-compile ${ARGS} -o dev_requirements.txt requirements.in dev_requirements.in
cp dev_requirements.txt requirements.txt
pip-compile -o requirements.txt requirements.in
