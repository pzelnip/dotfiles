# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of `ignorespace'.
HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoreboth

# include timestamps in the output of the history command
HISTTIMEFORMAT="%d/%m/%y %T "

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
export HISTFILESIZE=50000
export HISTSIZE=10000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# some more ls aliases
alias ls='ls -Fl'
alias python='python3'

# adam's aliases
alias grep='grep --color=auto'
alias md='mkdir'
alias cls='clear'
alias rd='rmdir'
alias bashrc='\vim ~/.bashrc && time source ~/.bashrc'
alias dusort='du -d 1 -h | sortdu.pl'

alias pipup="pip install --upgrade pip"
alias dos2unix="perl -pe 's/\r\n|\n|\r/\n/g'"

alias kill_stopped_docker_containers='docker ps -aq --no-trunc | xargs docker rm'
alias kill_untagged_docker_images='docker images --format "{{.ID}}\t{{.Tag}}" | grep "<none>" | awk "{ print \$1}" | xargs docker rmi'
alias kill_all_docker_images='docker rmi -f $(docker images -a -q)'

alias shell_into_first_docker_container='docker exec -it $(docker ps | sed -n 2p | cut -d" "  -f 1) /bin/sh'

alias sloc=scc

# inspired by https://stackoverflow.com/a/68390/808804
alias topcommands="history | tr -s ' ' | cut -d ' ' -f 5 | sort | uniq -c | sort -nr | head"

alias subl="/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl"

alias cloc=scc

alias dcd='docker compose down'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

function parse_git_dirty {
 git diff --quiet HEAD &>/dev/null
 [[ $? == 1 ]] && echo "⚡"
}
function parse_git_branch {
 local branch=$(__git_ps1 "%s")
 [[ $branch ]] && echo "[$branch$(parse_git_dirty)]"
}

# Show asterisk in git status in prompt if uncommitted changes
export GIT_PS1_SHOWDIRTYSTATE=1

function promptcol {
# return red if root, white otherwise
    if [ ${UID} -eq 0 ]; then
        echo '1;31m'
    else
        echo '0;37m'
    fi
}

function uptimeinfo {
    uptime | perl -ne 'if(/\d\s+up(.*),\s+\d+\s+users/) { $s = $1; $s =~ s/^\s+|\s+$//g; print $s; }'
}

export AWS_DEFAULT_REGION='ca-central-1'

export PATH=$PATH:~/bin:/opt/homebrew/bin

alias md5sum='md5 -r'

alias cat='cat.sh'

# start a simple Python server, see https://stackoverflow.com/a/46595749/808804
alias serve="python -m $(python -c 'import sys; print("http.server" if sys.version_info[:2] > (2,7) else "SimpleHTTPServer")')"

# source some env vars that I don't want in version control
source ~/.passwords

# base64 encode a string & copy to clipboard
# use like: echo "encode this string" | b64
# taken from: https://coderwall.com/p/tgmdia
function b64() {
   base64 | pbcopy
}

# cd to the git root directory (ie if in /myproject/src/main/java/com/foobar/baz
# a cd-gitroot will return you to /myproject)
# https://coderwall.com/p/zro3qg
alias cd-gitroot='cd $(git rev-parse --show-toplevel)'

alias git-copybranch="git branch | grep '*' | tr -d ' *\n' | pbcopy"

# Vagrant tab completion, install first with:
#
# brew tap homebrew/completions
# brew install vagrant-completion
#
# See: https://kura.io/vagrant-bash-completion/#os-x
if [ -f `brew --prefix`/etc/bash_completion.d/vagrant ]; then
    source `brew --prefix`/etc/bash_completion.d/vagrant
fi

# docker tab completion, on OSX simlink to the completion scripts with:
#
# find /Applications/Docker.app \
# -type f -name "*.bash-completion" \
# -exec ln -s "{}" "$(brew --prefix)/etc/bash_completion.d/" \;
#
# see: https://stackoverflow.com/a/38421283/808804
if [ -f $(brew --prefix)/etc/bash_completion ]; then
. $(brew --prefix)/etc/bash_completion
fi

# ssh host completion, see http://www.commandlinefu.com/commands/view/8562/enable-tab-completion-for-known-ssh-hosts
complete -W "$(echo `\cat ~/.ssh/known_hosts | cut -f 1 -d ' ' | sed -e s/,.*//g | uniq | grep -v "\["`;)" ssh

# bash: Place this in .bashrc.
function iterm2_print_user_vars() {
  iterm2_set_user_var gitBranch $((git branch 2> /dev/null) | grep \* | cut -c3-);
  iterm2_set_user_var pythonVersion $(python -c "import platform; print(platform.python_version())");
}

function makevenv() {
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip pylint
}

function joke { curl -s -H "Accept: application/json" https://icanhazdadjoke.com/ | jq ".joke"; }

export PATH=$PATH:/Users/adamparkin/.local/bin

export WORKON_HOME=~/.envs

# set up asdf with virtualenvwrapper, requires the virtualenvwrapper package to be installed
# to the python interpreter that asdf is using.
VIRTUALENVWRAPPER_PYTHON=/Users/adamparkin/.asdf/shims/python
# FULLPYTHONPATH=`asdf which python`
# PYTHONPATH=`dirname $FULLPYTHONPATH`
PYTHONPATH=$(dirname $(asdf which python))
source $PYTHONPATH/virtualenvwrapper.sh
export PATH=$PYTHONPATH:$PATH

eval "$(starship init bash)"

# set up direnv (install via brew)
eval "$(direnv hook bash)"

# source some items that are specific to this machine (ie not in dotfiles repo)
source ~/.machine_specific

. /opt/homebrew/opt/asdf/libexec/asdf.sh
