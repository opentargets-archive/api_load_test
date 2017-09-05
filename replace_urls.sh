#!/usr/bin/env bash

url_old=$1
url_new=$2

files=$(ls -1 *.txt)

for f in $files; do
    echo rewriting old url $url_old by new url $url_new for file $f
    pattern="s#${url_old}#${url_new}#g"
    sed -i $pattern $f
done
