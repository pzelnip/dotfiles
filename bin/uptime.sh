#!/bin/sh

echo "[`uptime | perl -ne 'if(/\d\s+up(.*),\s+\d+\s+users/) { $s = $1; $s =~ s/^\s+|\s+$//g; print $s; }'`]"
