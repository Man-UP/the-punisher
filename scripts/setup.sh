#!/bin/bash
set -o errexit
set -o nounset

# libfoxxy
easy_install --user \
    https://github.com/dj-foxxy/libfoxxy/zipball/master

# simplejson
easy_install --user \
    https://github.com/simplejson/simplejson/zipball/master

# httplib2
easy_install --user \
    http://httplib2.googlecode.com/files/httplib2-0.7.2.tar.gz

# oauth
easy_install --user \
    https://github.com/simplegeo/python-oauth2/tarball/master

# Python twitter
easy_install --user \
    http://python-twitter.googlecode.com/files/python-twitter-0.8.2.tar.gz

