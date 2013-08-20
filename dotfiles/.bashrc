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
alias dusort='du --max-depth=1 -h | perl /home/aparkin/bin/sortdu.pl'

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
$WHITE\$(nowplaying)\n$PCOLOR λ $LIGHT_GRAY"
PS2='> '
PS4='+ '
}
proml

export WORKON_HOME=~/.envs
source /usr/local/bin/virtualenvwrapper.sh

source /usr/local/git/contrib/completion/git-completion.bash

export PATH=$PATH:/Applications/Xcode.app/Contents/Developer/usr/bin
export PATH=$PATH:/Users/aparkin/bin

alias truecrypt='/Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text'
alias mountusb='/Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text --mount /Volumes/NO\ NAME/mainData.tc /Volumes/usbarchive'

alias md5sum='md5 -r'

alias mount-ydrive='dir="/Volumes/ydrive"; if [ ! -d ${dir} ]; then mkdir ${dir}; fi; sudo mount -t nfs -o proto=tcp 192.168.47.20:/PUBLIC ${dir}; unset dir;'
alias mount-netfile='dir="/Volumes/netfile"; if [ ! -d ${dir} ]; then mkdir ${dir}; fi; sudo mount -t nfs -o proto=tcp,vers=4 192.168.40.42:/ ${dir}; unset dir;'

alias cat='lolcat'

JAVA_HOME="/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home/"
export JAVA_HOME

HUBOT_IRC_NICK="space-core"
export HUBOT_IRC_NICK
HUBOT_IRC_ROOMS="#seeker,#hubot"
export HUBOT_IRC_ROOMS
HUBOT_IRC_SERVER="irc.seekersolutions.com"
export HUBOT_IRC_SERVER

STASH_HOME="/Users/aparkin/Downloads/stash/stash-home"
export STASH_HOME

SONAR_RUNNER_HOME="/Users/aparkin/Downloads/sonar/sonarrunner"
export SONAR_RUNNER_HOME 
export PATH=$PATH:$SONAR_RUNNER_HOME/bin

# source some env vars that I don't want in version control
source ~/.passwords

# base64 encode a string & copy to clipboard
# use like: echo "encode this string" | b64 
# taken from: https://coderwall.com/p/tgmdia
function b64() {
   base64 | pbcopy
}
