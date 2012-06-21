#!/bin/bash

set -o errexit
set -o nounset

readonly REPO="$(readlink -f -- "$(dirname -- "${0}")/..")"
cd -- "${REPO}"

export PYTHONPATH='src/'

python2 src/punisher/gui.py "${@}"

