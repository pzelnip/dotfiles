#!/bin/sh

# This script requires two dependencies be installed:

# gem install lolcat
# pip install Pygments

if [ $# -eq 0 ]; then
    lolcat
else
    TYPE=$(pygmentize -N $1)

    if [ $TYPE = "text" ]; then
        lolcat "$1"
    elif [ $TYPE = "resource" ]; then
        lolcat "$1"
    else
        pygmentize "$1"
    fi
fi
