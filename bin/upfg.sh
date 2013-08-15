#!/bin/bash
#the script updates MacPorts and Fink packages;

if [ "$(whoami)" != 'root' ]; then
  echo "You have no permission to run $0 as non-root user."
  exit 1
fi

port selfupdate
port -d sync
portindex
port upgrade installed
