#!/bin/sh

if [ $# -eq 0 ]; then
    lolcat
else
    TYPE=$(pygmentize -N $1)

    if [ $TYPE = "text" ]; then
        lolcat $1
    else
        pygmentize $1
    fi
fi
