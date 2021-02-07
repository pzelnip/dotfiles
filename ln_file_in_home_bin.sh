#!/bin/sh

# Creates a symbolic link between a script in bin to ~/bin
# I use this for the "Symbolic link current file to ~/bin"
# VS Code task in .vscode/tasks.json

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi

echo "Linking $1 to bin"
ln -s ~/dotfiles/bin/$1 ~/bin
