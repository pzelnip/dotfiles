#!/bin/sh

cd ~/dotfiles
if ! git diff-index --quiet HEAD --; then
    echo " [ ~/dotfiles directory dirty, please commit changes ]"
fi
