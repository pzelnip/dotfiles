#!/bin/sh

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi

echo "Linking $1 to bin"
ln -s ~/dotfiles/bin/$1 ~/bin
