#!/bin/bash

set -o errexit
set -o nounset

sudo pacman -Sy python-imaging

readonly INSTALL='sudo easy_install-2.7'

sudo easy_install-2.7 httplib2 oauth2 python-twitter simplejson

