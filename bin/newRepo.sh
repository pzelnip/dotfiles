#!/bin/sh
set -e

# copy vscode template tasks.json to .vscode
mkdir -p .vscode
cp ~/dotfiles/.vscode-templates/tasks.json .vscode/tasks.json

# simlink prepare-commit hook to .git/hooks
ln -s ~/dotfiles/.git-templates/hooks/prepare-commit-msg .git/hooks/prepare-commit-msg
