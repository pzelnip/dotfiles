#!/bin/bash

pid=`ps ax | grep SymAutoProtect | grep -v grep | awk '{ print $1 }'`

if [[ -z "$pid" ]]; then
   echo "not running"
else
   echo "running as $pid, killing..."
   sudo kill $pid
fi
