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
brew install direnv
brew install scc
brew install ctop
brew install gping
brew install lazygit
brew install fzf
brew install asdf
brew install bat
brew install rg
brew install ghorg
brew install imagemagick

# https://docs.gitlab.com/editor_extensions/gitlab_cli/
brew install glab

# https://github.com/ankitpokhrel/jira-cli
brew install jira-cli

# pipx is a special case
# I only want to run ensurepath if it's being installed now
echo "Checking if pipx is installed"
if ! type "pipx" > /dev/null 2>&1; then
    echo "Installing pipx"
    brew install pipx
    pipx ensurepath
fi
# this seems silly, but want to do this to check for update
brew install pipx

# Now check if current arch is an M1 or not.
CPU=`sysctl -n machdep.cpu.brand_string`
echo "CPU is $CPU"
if [[ $CPU == *"Apple M1"* ]]; then
    echo "CPU is an M1, aborting..."
    exit
fi

# Rest are the currently not M1-ready packages
echo "Continuing"

# no non-m1 packages anymore, probably should delete the above check.
