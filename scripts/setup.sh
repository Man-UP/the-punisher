#!/bin/bash
set -o errexit
set -o nounset

sudo apt-get --assume-yes install \
    git \
    python-setuptools

# libfoxxy
sudo easy_install https://github.com/dj-foxxy/libfoxxy/zipball/master

# simplejson
sudo easy_install https://github.com/simplejson/simplejson/zipball/master

# httplib2
sudo easy_install http://httplib2.googlecode.com/files/httplib2-0.7.2.tar.gz

# oauth
sudo easy_install https://github.com/simplegeo/python-oauth2/tarball/master

# Python twitter
sudo easy_install http://python-twitter.googlecode.com/files/python-twitter-0.8.2.tar.gz

# pyutmp
cd /tmp
git clone git://github.com/bmc/pyutmp.git
cd pyutmp
sudo python setup.py install

