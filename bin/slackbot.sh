#!/bin/bash

# defaults
CHANNEL=testtest

# see the Slackbot integration for details on getting your Slackbot URL
WEBURL=$SLACKBOT_WEB_URL

for i in "$@"
do
case $i in
    -c=*|--channel=*)
    CHANNEL="${i#*=}"

    ;;

    -m=*|--message=*)
    MESSAGE="${i#*=}"

    ;;

    -w=*|--weburl=*)
    WEBURL="${i#*=}"

    ;;

    --default)
    DEFAULT=YES
    ;;
    *)
    echo "Unknown option"
    exit
            # unknown option
    ;;
esac
done
echo CHANNEL = ${CHANNEL}
echo WEBURL = ${WEBURL}
echo MESSAGE = ${MESSAGE}

curl --data "${MESSAGE}" "${WEBURL}&channel=%23${CHANNEL}"

