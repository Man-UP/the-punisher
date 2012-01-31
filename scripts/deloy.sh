#!/bin/bash
set -o errexit
set -o nounset

repo="$(readlink -f -- "$(dirname -- "${0}")/..")"
dest="${HOME}/public"

rm -fr -- "${dest}/punisher"
cp -r -- "${repo}/src/punisher" "${dest}"

# Compile the Python source to byte code.
cd -- "${dest}"
python -c '
__import__("compileall").compile_dir(
    "/home/S08/suttonp8/public/punisher",
    force=True)
'

find "${dest}/punisher" -type f -exec chmod 644 {} \;
find "${dest}/punisher" -type d -exec chmod 755 {} \;
cd -- "${HOME}"
chmod 711 . .local .local/lib .local/lib/python2.7
find .local/lib/python2.7/site-packages -type f -exec chmod 644 {} \;
find .local/lib/python2.7/site-packages -type d -exec chmod 755 {} \;

