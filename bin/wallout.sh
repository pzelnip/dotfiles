#!/bin/bash

uptime | awk '{sub(/[0-9]|user\,|users\,|load/, "", $6); sub(/mins,|min,/, "min", $6); sub(/user\,|users\,/, "", $5); sub(",", "min", $5); sub(":", "h ", $5); sub(/[0-9]/, "", $4); sub(/day,/, " day ", $4); sub(/days,/, " days ", $4); sub(/mins,|min,/, "min", $4); sub("hrs,", "h", $4); sub(":", "h ", $3); sub(",", "min", $3); print "Uptime: " $3$4$5$6}'
ifconfig en0 | grep -E "inet|ether"| perl -pe 's/^\s+//'

