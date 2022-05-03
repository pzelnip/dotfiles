#!/bin/sh
set -e

brew install git
brew install git-extras
brew install bash-completion
brew install starship
brew install python3
brew install watch
brew install the_silver_searcher
brew install htop
brew install cloc
brew install autoenv

# pipx is a special case, I want it installed before pyenv, and
# I only want to run ensurepath if it's being installed now
echo "Checking if pipx is installed"
if ! type "pipx" > /dev/null 2>&1; then
    echo "Installing pipx"
    brew install pipx
    pipx ensurepath
fi
# this seems silly, but want to do this to check for update
brew install pipx

brew install pyenv
brew install pyenv-virtualenv
brew install pyenv-virtualenvwrapper

# Now check if current arch is an M1 or not.
CPU=`sysctl -n machdep.cpu.brand_string`
echo "CPU is $CPU"
if [[ $CPU == *"Apple M1"* ]]; then
    echo "CPU is an M1, aborting..."
    exit
fi

# Rest are the currently not M1-ready packages
echo "Continuing"

brew install hadolint
