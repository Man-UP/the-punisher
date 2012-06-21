#!/bin/bash

set -o errexit
set -o nounset

sudo pacman -Sy python-imaging

sudo easy_install-2.7 httplib2 oauth2 python-twitter simplejson

