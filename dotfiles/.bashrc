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

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ls='ls -Fl'

# adam's aliases
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
PS1="${TITLEBAR}\
$BLUE [ $BROWN\u@\h:\w -- \D{%a %b %d %Y %l:%M%p (%Z%z)}$LIGHT_GRAY\$(__git_ps1)\
$LIGHT_RED\$(dirty.sh)$BLUE]\
$WHITE \$(nowplaying)\n$LIGHT_GRAY λ $LIGHT_GRAY"
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

function b64() {
  openssl base64 -in $1 | tr -d "\n" | pbcopy;
}
