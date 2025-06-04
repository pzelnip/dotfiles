#!/bin/sh
set -e

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi

cd ~/temp/sandbox
git clone $1
