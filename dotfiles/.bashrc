# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of `ignorespace'.
HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# some more ls aliases
alias ls='ls -Fl'

# adam's aliases
alias grep='grep --color=auto'
alias md='mkdir'
alias cls='clear'
alias vi='mvim'
alias rd='rmdir'
alias bashrc='\vim ~/.bashrc && source ~/.bashrc'
alias dusort='du -d 1 -h | sortdu.pl'

alias gitk='gitk --all'

alias dos2unix="perl -pe 's/\r\n|\n|\r/\n/g'"

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

#function parse_git_dirty {
#  git diff --quiet HEAD &>/dev/null
#  [[ $? == 1 ]] && echo "⚡"
#}
#function parse_git_branch {
#  local branch=$(__git_ps1 "%s")
#  [[ $branch ]] && echo "[$branch$(parse_git_dirty)]"
#} 
#
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

function proml {
  local        BLACK="\[\033[0;30m\]"
  local         GRAY="\[\033[1;30m\]"
  local          RED="\[\033[0;31m\]"
  local    LIGHT_RED="\[\033[1;31m\]"
  local        GREEN="\[\033[0;32m\]"
  local  LIGHT_GREEN="\[\033[1;32m\]"
  local        BROWN="\[\033[0;33m\]"
  local       YELLOW="\[\033[1;33m\]"
  local         BLUE="\[\033[0;34m\]"
  local   LIGHT_BLUE="\[\033[1;34m\]"
  local       PURPLE="\[\033[0;35m\]"
  local LIGHT_PURPLE="\[\033[1;35m\]"
  local         CYAN="\[\033[0;36m\]"
  local   LIGHT_CYAN="\[\033[1;36m\]"
  local   LIGHT_GRAY="\[\033[0;37m\]"
  local        WHITE="\[\033[1;37m\]"
  case $TERM in
    xterm*)
    TITLEBAR='\[\033]0;\u@\h:\w \D{%a %b %d %Y %l:%M%p (%Z%z)}\007\]'
    ;;
    *)
    TITLEBAR=""
    ;;
  esac

PCOLOR="\[\033[\$(promptcol)\]"

# note that in the following prompt the error code item (\$?) must be the 
# first item in the prompt.  Otherwise it'll show the errorcode for the last 
# command executed in producing the prompt.
PS1="${TITLEBAR}\
$BLUE [$GREEN[\$?] [\D{%a %b %d %Y %l:%M%p (%Z%z)}] [Up: \$(uptimeinfo)] $BROWN\u@\h:\w $LIGHT_GRAY\$(__git_ps1)\
$LIGHT_RED\$(dirty.sh)$BLUE]\
\n$WHITE\$(spotify status | iconv -f utf-8 -t ascii//translit)$PCOLOR λ $LIGHT_GRAY"
PS2='> '
PS4='+ '
}
proml

export WORKON_HOME=~/.envs
source /usr/local/bin/virtualenvwrapper.sh

source ~/bin/git-completion.bash
source ~/bin/hg_bash_completion.bash

export PATH=/usr/local/bin:$PATH:/Applications/Xcode.app/Contents/Developer/usr/bin
#:Applications/Postgres.app/Contents/Versions/9.3/bin
export PATH=$PATH:~/bin

alias truecrypt='/Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text'
alias mountusb='/Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text --mount /Volumes/NO\ NAME/mainData.tc /Volumes/usbarchive'

mounttc() {
    /Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text --mount $1 /Volumes/$1
}

alias md5sum='md5 -r'

alias cat='cat.sh'

#JAVA_HOME="/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home/"
#JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_45.jdk/Contents/Home"
JAVA_HOME=$(/usr/libexec/java_home)
export JAVA_HOME

STASH_HOME="${HOME}/Downloads/stash/stash-home"
export STASH_HOME

SONAR_RUNNER_HOME="${HOME}/Downloads/sonar/sonarrunner"
export SONAR_RUNNER_HOME 
export PATH=$PATH:$SONAR_RUNNER_HOME/bin

#SLACK_WEBHOOK_URL="https://pzelnip.slack.com/services/hooks/incoming-webhook?token=Ta4BRUMStaB5ahT4Y76eT1Hi"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"

export SLACK_WEBHOOK_URL

# source some env vars that I don't want in version control
source ~/.passwords

# base64 encode a string & copy to clipboard
# use like: echo "encode this string" | b64 
# taken from: https://coderwall.com/p/tgmdia
function b64() {
   base64 | pbcopy
}

PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting

# cd to the git root directory (ie if in /myproject/src/main/java/com/foobar/baz
# a cd-gitroot will return you to /myproject)
# https://coderwall.com/p/zro3qg
alias cd-gitroot='cd $(git rev-parse --show-toplevel)'

alias vimdiff='mvim -d'
alias git-copybranch="git branch | grep '*' | tr -d ' *\n' | pbcopy"


# start youtube on my chromecast, taken from:
# https://coderwall.com/p/jvuzdg
# http://fiquett.com/2013/07/chromecast-traffic-sniffing/
function ccytplay {
  curl -H "Content-Type: application/json" \
    http://192.168.1.149:8008/apps/YouTube \
    -X POST \
    -d "v=$1";
}

# quit Youtube on the chromecast
function ccytquit {
  curl -H "Content-Type: application/json" \
    http://192.168.1.149:8008/apps/YouTube \
    -X DELETE;
}

function ccytstatus {
curl -H "Content-Type: application/json" http://192.168.1.149:8008/apps/YouTube -X GET
}

# search Youtube for a query string on the command line
function ytsearch() {
  curl -s https://www.youtube.com/results\?search_query\=$@ | \
    grep -o 'watch?v=[^"]*"[^>]*title="[^"]*' | \
    sed -e 's/^watch\?v=\([^"]*\)".*title="\(.*\)/\1 \2/g'
}

function ccinfo {
  curl http://192.168.1.149:8008/ssdp/device-desc.xml
}

function ccinfodetail {
  curl http://192.168.1.149:8008/setup/eureka_info?options=detail | python -mjson.tool
}



### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"
export PATH="/opt/chefdk/bin:$PATH"

export SLACK_WEBHOOK_URL

# Vagrant tab completion, install first with:
#
# brew tap homebrew/completions
# brew install vagrant-completion
#
# See: https://kura.io/vagrant-bash-completion/#os-x
if [ -f `brew --prefix`/etc/bash_completion.d/vagrant ]; then
    source `brew --prefix`/etc/bash_completion.d/vagrant
fi

# Workaround for boot2docker, because it's dumb
# See: https://github.com/docker/machine/issues/531 for context
alias dockerm="docker --tlsverify=false"

# setting up Go via homebrew
export GOPATH=$HOME/golang
export GOROOT=/usr/local/opt/go/libexec
export PATH=$PATH:$GOPATH/bin
export PATH=$PATH:$GOROOT/bin

#ssh host completion, see http://www.commandlinefu.com/commands/view/8562/enable-tab-completion-for-known-ssh-hosts
complete -W "$(echo `cat ~/.ssh/known_hosts | cut -f 1 -d ' ' | sed -e s/,.*//g | uniq | grep -v "\["`;)" ssh

# bash: Place this in .bashrc.
function iterm2_print_user_vars() {
  iterm2_set_user_var gitBranch $((git branch 2> /dev/null) | grep \* | cut -c3-)
}
