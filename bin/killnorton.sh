#!/bin/bash

pid=`ps ax | grep SymAutoProtect | grep -v grep | awk '{ print $1 }'`

echo $pid
