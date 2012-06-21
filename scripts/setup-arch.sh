#!/bin/bash

set -o errexit
set -o nounset

sudo pacman -Sy --noconfirm python2 python-imaging python2-pip

sudo easy_install-2.7 httplib2 oauth2 python-twitter simplejson

